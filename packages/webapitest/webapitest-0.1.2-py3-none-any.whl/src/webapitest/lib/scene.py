import re
import os
import requests
import importlib
import json
from collections import OrderedDict
from .base import *
from .case import Header
from .utils import read_csv, logger


@dataclass
class EnvironParam(DataClassMixin):
    key: str
    value: str
    description: Optional[str] = None

    def to_dict(self) -> dict:
        return {'key': self.key, 'value': self.value}


@dataclass
class Scene(DataClassMixin, FileLoaderMixin):
    """
        场景
        一个场景下可以有一个或多个测试用例
        对应标准测试用例的一个文件夹或一个文件（当只有一个测试用例时）
    """
    name: str
    url: str
    user: Optional[str]
    method: Optional[str]#MethodEnum
    cases: List[Case]
    header: List[Header] = None
    desc: Optional[str] = None

    @property
    def envs(self):
        return self._envs

    def set_envs(self, envs):
        self._envs = envs   # [EnvironParam()]

    def get_env(self, k):
        for i in self._envs:
            if i.key == k:
                return i.value
        raise Exception("target %s not in envs" % k)

    @property
    def user_cookie(self):
        return self._user_cookie

    def _get_host_port(self):
        # url = self.url
        # for s in ['http://', 'https://']:
        #     if url.startswith(s):
        #         url = url[len(s):]
        #         break
        # return url.split('/')[0]

        pattern = re.compile('[http|https]*://(.*?)/.*$')
        return pattern.match(self.url).groups()[0]

    def get_host(self):
        return self._get_host_port().split(':')[0]

    def get_port(self):
        if ':' in self._get_host_port():
            return self._get_host_port().split(':')[1]
        return None

    def get_path(self):
        url = self.url
        for s in ['http://', 'https://']:
            if url.startswith(s):
                url = url[len(s):]
                break
        path = '/'.join(url.split('/')[1:])
        return path.split('?')[0]

        # pattern = re.compile('[http|https]*://.*/(.*?)?.*$')
        # return pattern.match(self.url).groups()[0]

    def set_user_cookie(self, user_cookie):
        self._user_cookie = user_cookie # "session=xxx"

    def set_project(self, project):
        self.project = project
        self.set_envs(project.envs)
        if project.cookie_users and project.default_user and not self.user:
            self.user = project.default_user
        if self.user:
            self.set_user_cookie(project.cookie_users[self.user])

    def get_module_path(self):
        path = self._path.replace('.json', '')
        join_str = os.path.join('a','a').replace('a','')
        _path = os.path.join(self.project.root, self.project.case_root)
        _path = _path + join_str
        relative_path = path.replace(_path, '')
        return relative_path.replace(join_str, '.')

    @staticmethod
    def from_dict(obj: Any) -> 'Scene':
        name = from_str(obj.get("name"))
        url = from_str(obj.get("url"))
        user = obj.get("user", None)
        # method = MethodEnum(obj.get('method'))
        method = obj.get('method')
        cases = from_list(Case.from_dict, obj.get('cases'))
        desc = obj.get('desc')
        return Scene(name, url, user, method, cases, desc=desc)

    def to_dict(self) -> dict:
        result = {}
        result['name'] = self.name
        result['url'] = self.url
        result['method'] = self.method# to_enum(MethodEnum, self.method)
        result['cases'] = from_list(lambda x: to_class(Case, x), self.cases)
        result['desc'] = self.desc
        return {k: result[k] for k in result if k in self.get_changed_keys()}

    def to_csv(self):
        """
            csv format:

        """
        res = [
            ['场景名', self.name],
            ['URL', self.url],
        ]
        if self.user:
            res.append(['用户', self.user])
        cases_data = []
        max_key_count = 0
        for case in self.cases:
            line = [case.name]
            max_key_count = max(max_key_count, len(case.params))
            for k, v in case.params.items():
                line.extend([k, v])
            cases_data.append(line)
        res.append(['CASE名'] + ['K', 'V'] * max_key_count)
        res.extend(cases_data)
        return res

    @staticmethod
    def load_from_csv(path):
        dirpath, filename = os.path.split(path)
        json_path = os.path.join(dirpath, filename.replace('.csv', '.json'))
        scene = Scene.load_from_file(json_path)
        if path.endswith('.json'):
            return scene
        l = read_csv(path)
        scene_attrs = {
            '场景名': 'name',
            'URL': 'url',
            '用户': 'user',
        }
        for index, line in enumerate(l):
            if line[0] in scene_attrs:
                setattr(scene, scene_attrs[line[0]], line[1])
            elif line[0] == 'CASE名':
                break
        cases = []
        for line in l[index:]:
            case_name = line[0]
            case_params = {}
            for _index, i in enumerate(line[1:]):
                if _index % 2 == 0:
                    case_params[i] = line[_index + 1]
            cases.append(Case(
                name=case_name,
                params=case_params
            ))
        scene.cases = cases
        return scene

    @staticmethod
    def gen_by_post_man_items(post_man_items):
        res = []
        for _index, pcase in enumerate(post_man_items):
            line = pcase.name.split('-', 1)
            if len(line) == 1:
                line = [line[0], 'case%s' % _index]
            res.append(line)
        assert len(set([i[0] for i in res])) > 1    #scene的名称不能冲突
        cases = []
        for index, (_scene_name, case_name) in enumerate(res):
            pcase = post_man_items[index]
            case = Case(
                name=case_name,
                params=pcase.get_params_dict()
            )
            cases.append(case)
        s = Scene(
            name=res[0][0],
            url=post_man_items[0].request.url.get_standard_url(),
            metmod=post_man_items[0].request.url.method,# MethodEnum(post_man_items[0].request.url.method),
            cases=cases
        )
        return s

    def gen_postman_url(self, case):
        from ..postman import URLClass, QueryParam
        return URLClass(
            host=self.get_host(),
            path=self.get_path(),
            hash=None,
            port=self.get_port(),
            protocol="https" if 'https:' in self.url else 'http',
            query=[QueryParam(description=None, disabled=None, key=k, value=v) for k, v in case.params.items()]
        )

    def gen_postman_requests(self):
        # todo 完善参数
        from ..postman import RequestClass
        res = []
        for case in self.cases:
            req = RequestClass(
                description=case.desc,
                header=self.get_postman_headers(),
                url=self.gen_postman_url(case),
                auth=None,
                body=None,
                certificate=None,
                method=self.method,
                proxy=None
            )
            res.append(req)
        return res

    @staticmethod
    def gen_by_post_man_collection(post_man_collection):
        return

    def get_cookie(self):
        if self.user:
            jar = requests.cookies.RequestsCookieJar()
            jar.set(self.project.cookie_key, self.project.cookie_users[self.user])
            return jar

    def get_headers(self) -> dict:
        # if self.user:
        #     h = Header(description='Cookie', key='Cookie', value= self.user_cookie)
        #     if self.header:
        #         self.header.append(h)
        #     else:
        #         self.header = [h]
        return {i.key: i.value for i in self.header} if self.header else {}

    def get_postman_headers(self):
        return self.header

    def parse_var(self, s):
        if type(s) in [list, dict]:
            _s = json.dumps(s)
            return json.loads(self.parse_var(_s))
        elif type(s) is not str:
            return s
        for p in re.findall('{{([a-zA-Z0-9_]+)}}', s):
            s = s.replace('{{%s}}' % p, self.get_env(p))
        for p in re.findall('{{(.*?)}}', s):
            try:
                func = self.get_func(p)
                v = func(self.project, self)
            except Exception as e0:
                raise Exception("变量转化方法<%s>执行失败，请检查 message: %s" % (p, str(e0)))
            if v is None:
                raise Exception("变量转化方法<%s>执行无法取得值，请检查" % (p,))
            s = s.replace('{{%s}}' % p, v)
        return s

    def get_func(self, p):
        if "func." in p:
            func_name = p.split('.')[-1:][0]
            module_name = '.'.join(p.split('.')[:-1])
            module = importlib.import_module(module_name)
            func = getattr(module, func_name)
        elif "func_this." in p:
            module_name = 'func.' + self.get_module_path()
            func_name = p.split('.')[-1:][0]
            module = importlib.import_module(module_name)
            func = getattr(module, func_name)
        else:
            raise Exception('parse {{%s}} error' % p)
        return func

    def get_response(self) -> dict:

        res = {}
        url = self.url
        headers = self.get_headers()
        url = self.parse_var(url)
        headers = {k: self.parse_var(v) for k, v in headers.items()}

        for case in self.cases:
            data = case.get_payload()
            data = {k: self.parse_var(v) for k, v in data.items()}
            method = 'GET' if self.method in [None, "GET"] else self.method
            logger.info('执行(%s)请求,URL为%s' % (method, url))
            if method == 'GET':
                resp = requests.get(url, params=data, headers=headers, cookies=self.get_cookie())
            elif method == "POST":
                resp = requests.request("POST", url, headers=headers, cookies=self.get_cookie(), json=data)
            else:
                resp = requests.request(method, url, headers=headers, cookies=self.get_cookie(), json=data)
            res[case.name] = {
                "resp": resp,
                "url": url,
                "callback": case.callback,
                "expect": case.expect
            }
        return res

    def run(self):
        try:
            responses = self.get_response()
            for case_name, response in responses.items():
                try:
                    resp = response['resp']
                    logger.info('run case <%s>, get status %s, content: %s' %
                                (self.name + case_name, resp.status_code, resp.content))
                    if response['callback']:
                        for f in response['callback']:
                            try:
                                func = self.get_func(f)
                                func(self.project, self, resp)
                            except Exception as e0:
                                raise Exception("callback方法<%s>执行失败，请检查 message: %s" % (f, str(e0)))

                    if not response['expect']:
                        validators = ['validator.check_status_200']
                    else:
                        validators = response['expect']
                    success = False
                    for validator_str in validators:
                        if self.validate(validator_str, self.project, self, case_name, resp):
                            success = True
                            self.project.result['success'] += 1
                            # break
                        else:
                            self.project.result['failed'] += 1
                            self.project.result['errlist'].append({"case_name": case_name, "path": response['url'],
                                                                   "message": "", "resp": resp.content})
                    if success:
                        self.project.cache_responses[case_name] = json.loads(resp.content)
                except Exception as e2:
                    self.project.result['failed'] += 1
                    self.project.result['errlist'].append({
                        "case_name": case_name,
                        "path": response['url'],
                        "message": str(e2),
                        "resp": resp.content
                    })
                    logger.error('case-' + case_name + ' run error:' + str(e2))

        except Exception as e1:
            self.project.result['failed'] += 1
            self.project.result['errlist'].append({
                "scene_name": self.name,
                "path": self.url,
                "message": str(e1)
            })
            logger.error('scene-' + self.name + ' run error:' + str(e1))

    def validate(self, validator_line, project, scene, case_name, resp):
        # if "&&" in validator_line or "||" in validator_line:

        validator_items = re.split('\|\||\&\&', validator_line)
        res_items = OrderedDict([])
        for validator_str in validator_items:
            validator_str = validator_str.strip()
            if validator_str.startswith("validator."):
                module = importlib.import_module("webapitest.validator")
                func = getattr(module, validator_str.replace("validator.", ""))
            else:
                func = self.get_func(validator_str)
            v = func(project, scene, case_name, resp)
            res_items[validator_str] = bool(v)
        for k, v in res_items.items():
            validator_line = validator_line.replace(k, str(v), 1)
        validator_line = validator_line.replace("||", "or")
        validator_line = validator_line.replace("&&", "and")

        try:
            return eval(validator_line)
        except Exception as e:
            raise e

