"""
    使用https://app.quicktype.io/#l=python 将post man collection.json转化为python类，再整理代码。
"""
import os
import time
from .lib.case import *
from .lib.utils import logger


@dataclass
class RequestClass(DataClassMixin):
    description: Union[Description, None, str] = None
    header: Union[List[Header], None, str] = None
    url: Union[URLClass, None, str] = None
    auth: Optional[Auth] = None
    body: Optional[Body] = None
    certificate: Optional[Certificate] = None
    method: Optional[str] = None
    proxy: Optional[ProxyConfig] = None

    @staticmethod
    def from_dict(obj: Any) -> 'RequestClass':
        assert isinstance(obj, dict)
        description = from_union([Description.from_dict, from_none, from_str], obj.get("description"))
        header = from_union([lambda x: from_list(Header.from_dict, x), from_str, from_none], obj.get("header"))
        url = from_union([URLClass.from_dict, from_str, from_none], obj.get("url"))
        auth = from_union([from_none, Auth.from_dict], obj.get("auth"))
        body = from_union([Body.from_dict, from_none], obj.get("body"))
        certificate = from_union([Certificate.from_dict, from_none], obj.get("certificate"))
        method = from_union([from_str, from_none], obj.get("method"))
        proxy = from_union([ProxyConfig.from_dict, from_none], obj.get("proxy"))
        return RequestClass(description, header, url, auth, body, certificate, method, proxy)

    def to_dict(self) -> dict:
        result: dict = {}
        result["description"] = from_union([lambda x: to_class(Description, x), from_none, from_str], self.description)
        result["header"] = from_union([lambda x: from_list(lambda x: to_class(Header, x), x), from_str, from_none],
                                      self.header)
        result["url"] = from_union([lambda x: to_class(URLClass, x), from_str, from_none], self.url)
        result["auth"] = from_union([from_none, lambda x: to_class(Auth, x)], self.auth)
        result["body"] = from_union([lambda x: to_class(Body, x), from_none], self.body)
        result["certificate"] = from_union([lambda x: to_class(Certificate, x), from_none], self.certificate)
        result["method"] = from_union([from_str, from_none], self.method)
        result["proxy"] = from_union([lambda x: to_class(ProxyConfig, x), from_none], self.proxy)
        return {k:result[k] for k in result if k in self.get_changed_keys()}

    def get_params(self):
        if self.url:
            return self.url.get_params()
        return {}

    def get_easy_url(self):
        if not self.method or self.method.upper() == 'GET':
            return self.url.get_easy_url()
        else:
            return self.url.get_url()


@dataclass
class ResponseClass(DataClassMixin):
    header: Union[List[Union[Header, str]], None, str]
    original_request: Union[RequestClass, None, str]
    """The time taken by the request to complete. If a number, the unit is milliseconds. If the
    response is manually created, this can be set to `null`.
    """
    response_time: Union[float, None, str]
    """The raw text of the response."""
    body: Optional[str] = None
    """The numerical response code, example: 200, 201, 404, etc."""
    code: Optional[int] = None
    cookie: Optional[List[Cookie]] = None
    """A unique, user defined identifier that can  be used to refer to this response from
    requests.
    """
    id: Optional[str] = None
    """The response status, e.g: '200 OK'"""
    status: Optional[str] = None
    """Set of timing information related to request and response in milliseconds"""
    timings: Optional[Dict[str, Any]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'ResponseClass':
        assert isinstance(obj, dict)
        header = from_union(
            [lambda x: from_list(lambda x: from_union([Header.from_dict, from_str], x), x), from_none, from_str],
            obj.get("header"))
        original_request = from_union([RequestClass.from_dict, from_str, from_none], obj.get("originalRequest"))
        response_time = from_union([from_float, from_str, from_none], obj.get("responseTime"))
        body = from_union([from_none, from_str], obj.get("body"))
        code = from_union([from_int, from_none], obj.get("code"))
        cookie = from_union([lambda x: from_list(Cookie.from_dict, x), from_none], obj.get("cookie"))
        id = from_union([from_str, from_none], obj.get("id"))
        status = from_union([from_str, from_none], obj.get("status"))
        timings = from_union([lambda x: from_dict(lambda x: x, x), from_none], obj.get("timings"))
        return ResponseClass(header, original_request, response_time, body, code, cookie, id, status, timings)

    def to_dict(self) -> dict:
        result: dict = {}
        result["header"] = from_union(
            [lambda x: from_list(lambda x: from_union([lambda x: to_class(Header, x), from_str], x), x), from_none,
             from_str], self.header)
        result["originalRequest"] = from_union([lambda x: to_class(RequestClass, x), from_str, from_none],
                                               self.original_request)
        result["responseTime"] = from_union([to_float, from_str, from_none], self.response_time)
        result["body"] = from_union([from_none, from_str], self.body)
        result["code"] = from_union([from_int, from_none], self.code)
        result["cookie"] = from_union([lambda x: from_list(lambda x: to_class(Cookie, x), x), from_none], self.cookie)
        result["id"] = from_union([from_str, from_none], self.id)
        result["status"] = from_union([from_str, from_none], self.status)
        result["timings"] = from_union([lambda x: from_dict(lambda x: x, x), from_none], self.timings)
        return {k:result[k] for k in result if k in self.get_changed_keys()}


@dataclass
class Items(DataClassMixin):
    """Items are entities which contain an actual HTTP request, and sample responses attached to
    it.

    One of the primary goals of Postman is to organize the development of APIs. To this end,
    it is necessary to be able to group requests together. This can be achived using
    'Folders'. A folder just is an ordered set of requests.
    """
    description: Union[Description, None, str] = None
    request: Union[RequestClass, None, str] = None
    event: Optional[List[Event]] = None
    """A unique ID that is used to identify collections internally"""
    id: Optional[str] = None
    """A human readable identifier for the current item.

    A folder's friendly name is defined by this field. You would want to set this field to a
    value that would allow you to easily identify this folder.
    """
    name: Optional[str] = None
    protocol_profile_behavior: Optional[Dict[str, Any]] = None
    response: Optional[List[Union[List[Any], bool, ResponseClass, float, int, None, str]]] = None
    variable: Optional[List[Variable]] = None
    auth: Optional[Auth] = None
    """Items are entities which contain an actual HTTP request, and sample responses attached to
    it. Folders may contain many items.
    """
    item: Optional[List['Items']] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Items':
        assert isinstance(obj, dict)
        description = from_union([Description.from_dict, from_none, from_str], obj.get("description"))
        request = from_union([RequestClass.from_dict, from_str, from_none], obj.get("request"))
        event = from_union([lambda x: from_list(Event.from_dict, x), from_none], obj.get("event"))
        id = from_union([from_str, from_none], obj.get("id"))
        name = from_union([from_str, from_none], obj.get("name"))
        protocol_profile_behavior = from_union([lambda x: from_dict(lambda x: x, x), from_none],
                                               obj.get("protocolProfileBehavior"))
        response = from_union([lambda x: from_list(lambda x: from_union(
            [from_none, from_float, from_int, from_bool, from_str, lambda x: from_list(lambda x: x, x),
             ResponseClass.from_dict], x), x), from_none], obj.get("response"))
        variable = from_union([lambda x: from_list(Variable.from_dict, x), from_none], obj.get("variable"))
        auth = from_union([from_none, Auth.from_dict], obj.get("auth"))
        item = from_union([lambda x: from_list(Items.from_dict, x), from_none], obj.get("item"))
        return Items(description, request, event, id, name, protocol_profile_behavior, response, variable, auth, item)

    def to_dict(self) -> dict:
        result: dict = {}
        result["description"] = from_union([lambda x: to_class(Description, x), from_none, from_str], self.description)
        result["request"] = from_union([lambda x: to_class(RequestClass, x), from_str, from_none], self.request)
        result["event"] = from_union([lambda x: from_list(lambda x: to_class(Event, x), x), from_none], self.event)
        result["id"] = from_union([from_str, from_none], self.id)
        result["name"] = from_union([from_str, from_none], self.name)
        result["protocolProfileBehavior"] = from_union([lambda x: from_dict(lambda x: x, x), from_none],
                                                       self.protocol_profile_behavior)
        result["response"] = from_union([lambda x: from_list(lambda x: from_union(
            [from_none, to_float, from_int, from_bool, from_str, lambda x: from_list(lambda x: x, x),
             lambda x: to_class(ResponseClass, x)], x), x), from_none], self.response)
        result["variable"] = from_union([lambda x: from_list(lambda x: to_class(Variable, x), x), from_none],
                                        self.variable)
        result["item"] = from_union([lambda x: from_list(lambda x: to_class(Items, x), x), from_none], self.item)
        result["auth"] = from_union([from_none, lambda x: to_class(Auth, x)], self.auth)
        return {k:result[k] for k in result if k in self.get_changed_keys()}

    def get_url(self):
        return self.request.get_easy_url()

    def gen_file(self, current_dir_path, collection):
        if not os.path.exists(current_dir_path):
            os.mkdir(current_dir_path)
        if not self.request:
            for i in self.item:
                current_path = os.path.join(current_dir_path, self.name)
                i.gen_file(current_path, collection)
        else:
            current_path = os.path.join(current_dir_path, '%s.json' % self.name.split('-')[0])
            if os.path.exists(current_path):
                scene = collection.cache_sennes[current_path]
                if scene.url != self.get_url():
                    # 从postman来的用例，如果名称重复，则补时间为其命名以避免重名
                    self.name = self.name + "_" + str(time.time()).replace('.', '')
                    scene = self.gen_base_scene()
                    # raise Exception(" %s-%s, %s,%s不同url，不应该命名为同一个场景，请修正" %
                    #                 (scene.url, scene.name,  self.get_url(), self.name))
                else:
                    self.gen_base_scene(scene)
            else:
                scene = self.gen_base_scene()
            if scene:
                f = open(current_path, 'w', encoding='utf-8')
                dic = scene.to_dict()
                f.write(json.dumps(dic, indent=4, ensure_ascii=False))
                f.close()
                collection.cache_sennes[current_path] = scene

    def gen_base_scene(self, scene=None):
        """
            将多个用例整合到一个场景中，方便测试人员书写
        :return:
        """
        from webapitest.webapitest import Scene
        if not self.request:
            res = {}
            for i in self.item:
                res[i.name] = i.gen_base_case()
        else:
            case = Case(
                name='-'.join(self.name.split('-')[1:]),
                params=self.request.get_params(),
                desc=self.request.description if self.request.description else None
            )
            if self.description:
                try:
                    description = json.loads(self.description)
                    case.desc = description.get('desc')
                    case.callback = description.get('callback')
                    case.expect = description.get('expect')
                except:
                    case.desc = self.description
            else:
                case.desc = self.request.description if self.request.description else None
            if scene is None:
                scene = Scene(
                    name=self.name.split('-')[0],
                    url=self.request.get_easy_url(),
                    user=None,
                    method=self.request.method,
                    cases=[case],
                    header=self.request.header,
                    desc=self.request.description if self.request.description else None
                )
            else:
                scene.cases.append(case)
            return scene

    def gen_single_scene(self):
        """
            一个场景一个用例
        :return:
        """
        from webapitest.webapitest import Scene
        if not self.request:
            res = {}
            for i in self.item:
                res[i.name] = i.gen_base_case()
        else:
            case = Case(
                name=self.name,
                params=self.request.get_params()
            )
            scene = Scene(
                name=self.name,
                url=self.request.get_easy_url(),
                user=None,
                method=self.request.method,
                cases=[case],
                header=self.request.header
            )
            return scene


@dataclass
class Collection(DataClassMixin, FileLoaderMixin):
    info: Information
    """Items are the basic unit for a Postman collection. You can think of them as corresponding
    to a single API endpoint. Each Item has one request and may have multiple API responses
    associated with it.
    """
    item: List[Items]
    auth: Optional[Auth] = None
    event: Optional[List[Event]] = None
    protocol_profile_behavior: Optional[Dict[str, Any]] = None
    variable: Optional[List[Variable]] = None
    cache_sennes = {}

    @staticmethod
    def from_dict(obj: Any) -> 'Collection':
        assert isinstance(obj, dict)
        info = Information.from_dict(obj.get("info"))
        item = from_list(Items.from_dict, obj.get("item"))
        auth = from_union([from_none, Auth.from_dict], obj.get("auth"))
        event = from_union([lambda x: from_list(Event.from_dict, x), from_none], obj.get("event"))
        protocol_profile_behavior = from_union([lambda x: from_dict(lambda x: x, x), from_none],
                                               obj.get("protocolProfileBehavior"))
        variable = from_union([lambda x: from_list(Variable.from_dict, x), from_none], obj.get("variable"))
        return Collection(info, item, auth, event, protocol_profile_behavior, variable)

    def to_dict(self) -> dict:
        result: dict = {}
        result["info"] = to_class(Information, self.info)
        result["item"] = from_list(lambda x: to_class(Items, x), self.item)
        result["auth"] = from_union([from_none, lambda x: to_class(Auth, x)], self.auth)
        result["event"] = from_union([lambda x: from_list(lambda x: to_class(Event, x), x), from_none], self.event)
        result["protocolProfileBehavior"] = from_union([lambda x: from_dict(lambda x: x, x), from_none],
                                                       self.protocol_profile_behavior)
        result["variable"] = from_union([lambda x: from_list(lambda x: to_class(Variable, x), x), from_none],
                                        self.variable)
        return {k:result[k] for k in result if k in self.get_changed_keys()}

    def gen_web_test_case_file(self, root_cases_path):
        """
            生产webapitest的标准测试用例文件
        :return:
        """
        if root_cases_path in ['/', ""]:
            raise Exception("错误的路径,请确认生产用例目录文件位置。")
        if os.path.exists(root_cases_path):
            try:
                os.remove(root_cases_path)
            except Exception as e:
                logger.error("程序无权删除您的文件夹 %s，请手工执行操作" % root_cases_path)
                raise e
        os.mkdir(root_cases_path)
        for i in self.item:
            i.gen_file(root_cases_path, self)
