import os
import re
import json
from builtins import NotImplementedError
from collections import OrderedDict
from .lib.scene import Scene, EnvironParam
from .lib.utils import write_csv, logger


class Project:
    """
        功能集成对外接口
    """
    env: dict = {}
    path: str
    cookie_key: str = 'session'
    cookie_file_path: str
    cookie_users = {}
    scenes = []
    scene_structure = {}
    login_url = ''
    default_user = None


    def __init__(self, **kwargs):
        self.cache_data = {}  # 用户设定需要缓存的解析数据，以便取用
        self.cache_responses = OrderedDict([])  # 缓存最新的响应，为避免占用内存过多，仅缓存20条。
        self.result = {"success": 0, "failed": 0, "errlist": []} # {"case_name":"", "path":"", "message":""}
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.default_user = self.env.get('default_user') or self.default_user

    @property
    def envs(self):
        return [EnvironParam(
            key=k, value=v
        ) for k, v in self.env.items()]

    @property
    def case_root(self):
        if self.path == 'default':
            return 'cases'
        return self.relative_path.split('/')[0]

    def load_cookie(self):
        """
            使用flask-login的cookie设置与解析，如网站使用其它方式设置cookie，可重写此方法。
        :return:
        """
        cookie_file_path = self.cookie_file_path
        if not self.cookie_file_path.startswith('/'):
            current_dir = os.getcwd()
            cookie_file_path = os.path.join(current_dir, self.cookie_file_path)

        scene = Scene.load_from_file(cookie_file_path)
        scene.set_project(self)
        response_dict = scene.get_response()
        pattern = re.compile('^' + self.cookie_key + '=(.*?);.*$')
        for user, response in response_dict.items():
            try:
                resp = response['resp']
                set_cookie_line = resp.headers._store['set-cookie'][1]
                self.cookie_users[user] = pattern.match(set_cookie_line).groups()[0]  # 没记录过期时间
                logger.info('成功登陆用户 %s，后续场景中可切换此用户。' % user)
            except Exception as e:
                logger.info('登陆用户 %s 失败，后续场景使用此用户等同于未登录。' % user)

    def callback_only_read(self, path, structure):
        """
            重写本方法，以修改获得场景后的默认行为
        :param path:
        :return:
        """
        scene = Scene.load_from_file(path)
        scene.set_project(self)
        self.scenes.append(scene)
        if scene.name not in structure:
            structure[scene.name] = scene

    def callback(project, scene, structure, path, **kwargs):
        """
            重写本方法，可以修改获得场景后的默认行为

        :param scene: 获得的场景对象
        :param structure: 场景的组织结构字典
        :param path: 当前文件路径
        :param kwargs: 额外参数
        :return:
        """
        scene.run()

    def go_through_all(self, path, structure, target='json', callback=None, kwargs={}):
        # print(self, path, structure, callback)
        if target == 'json':
            scene = Scene.load_from_file(path)
        elif target == 'csv':
            scene = Scene.load_from_csv(path)
        else:
            raise Exception('error target')
        scene.set_project(self)
        self.scenes.append(scene)
        if scene.name not in structure:
            structure[scene.name] = scene
        if callback:
            # print('now', self, scene, structure, path, kwargs)
            callback(self, scene, structure, path, **kwargs)

    def load_scene(self, go_through_all=go_through_all, target='json', callback_method=None, kwargs={}):
        """
            识别路径下所有json文件，载入场景，执行回调
            也支持识别csv文件
        :return:
        """
        if self.path.endswith('.json'):
            go_through_all(self, self.path, {}, target, callback_method, kwargs=kwargs)
            return

        self.scene_structure = {}

        def search(root, target, go_through_all=go_through_all, current_data={}):
            items = os.listdir(root)
            items = sorted(items)
            for item in items:
                path = os.path.join(root, item)
                if item.startswith('.'):
                    # 忽略隐藏文件
                    continue
                elif os.path.isdir(path):
                    if item not in current_data:
                        current_data[item] = {}
                    logger.info('scan dir ' + path)
                    search(path, target, go_through_all=go_through_all, current_data=current_data[item])
                elif path.split('/')[-1].split('.')[-1] == target:
                    logger.info('load file ' + path)
                    go_through_all(self, path, current_data, target, callback_method, kwargs=kwargs)

        search(self.path, target, go_through_all=go_through_all, current_data=self.scene_structure)

    def output_result(self):
        logger.info('已完成测试，共有%s个用例执行成功，%s个用例失败，失败用例详情如下：' % (self.result['success'],
                                                             self.result['failed']))
        for res in self.result['errlist']:
            try:
                res['resp'] = json.loads(res['resp'])
            except:
                res['resp'] = str(res.get('resp', ''))
            logger.info(json.dumps(res, indent=4, ensure_ascii=False))

    def run(self):
        self.load_scene(go_through_all=Project.go_through_all, callback_method=Project.callback)
        self.output_result()

    def get_scene_items(self):
        from .postman import Items

        def get_item(current_data):
            items = []
            for key, v in current_data.items():
                if type(v) is Scene:
                    for _index, case in enumerate(v.gen_postman_requests()):
                        item = Items(
                            description=v.cases[_index].get_postman_desc_text(),
                            request=case,
                            name=key + '-' + v.cases[_index].name,
                            protocol_profile_behavior=None
                        )
                        items.append(item)
                else:
                    item = Items(
                        description=v.get('desc'),
                        request=None,
                        name=key,
                        protocol_profile_behavior=None,
                        response=None,
                        variable=None,
                        item=get_item(v)
                    )
                    items.append(item)
            return items

        items = get_item(self.scene_structure)
        return items

    def create_scv(self):

        def _callback_create_csv(project, scene, structure, path, **kwargs):
            print('_callback_create_csv', project, scene, structure, path, kwargs)
            dirpath, filename = os.path.split(path)
            csv_path = os.path.join(dirpath, filename.replace('.json', '.csv'))
            write_csv(csv_path, scene.to_csv())
        self.load_scene(go_through_all=Project.go_through_all, target='json', callback_method=_callback_create_csv)

    def check_csv(self):
        self.load_scene(go_through_all=Project.go_through_all, target='csv', callback_method=None)

    def reset_json_by_csv(self):
        def _callback_reset_json_by_csv(project, scene, structure, path, **kwargs):
            dirpath, filename = os.path.split(path)
            csv_path = os.path.join(dirpath, filename.replace('.json', '.csv'))
            write_csv(csv_path, scene.to_csv())
        self.load_scene(go_through_all=Project.go_through_all, target='csv',
                        callback_method=_callback_reset_json_by_csv)

    @classmethod
    def gen(cls):
        """
            重写此方法，以生产你项目所需对象
        :return:
        """
        return cls()

    def clean_db(self):
        """重写方法完成清理数据库动作"""
        raise NotImplementedError

    def start_webserver(self):
        """重写方法完成启动网站服务动作"""
        raise NotImplementedError

    def init_db(self):
        """重写方法完成初始化数据库动作"""
        raise NotImplementedError
