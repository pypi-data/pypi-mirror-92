import json
from ._typing import *
from .utils import logger

__all__ = (
    'json', 'Enum', 'dataclass', 'Any', 'Optional', 'List', 'Union', 'Dict', 'TypeVar', 'Callable', 'Type', 'cast', 'T', 'EnumT',
    'from_str', 'from_none', 'from_union', 'to_enum', 'from_list', 'to_class', 'from_bool', 'from_int', 'from_dict',
    'from_float', 'to_float', 'DataClassMixin', 'FileLoaderMixin', 'Case'
)


class DataClassMixin:
    def get_changed_keys(self):
        res = []
        for key in self.__class__.__dict__['__annotations__']:
            if hasattr(self.__class__, key):
                if getattr(self.__class__, key) is not getattr(self, key):
                    res.append(key)
            else:
                res.append(key)
        return res


class FileLoaderMixin:
    _path = None

    @classmethod
    def load_from_file(cls, path):
        logger.info('load scene from file %s' % path)
        f = open(path, encoding="utf-8")
        s = f.read()
        f.close()
        try:
            obj = cls.from_dict(json.loads(s))
            obj._path = path
            return obj
        except Exception as e:
            logger.info(
                "load_file error: %s, message: %s" % (path, str(e))
            )
            raise e


@dataclass
class Case(DataClassMixin):
    name: str
    params: dict
    desc: str = None
    response: list = None
    callback: list = None
    expect: list = None

    @staticmethod
    def from_dict(obj: Any) -> 'Case':
        name = from_str(obj.get("name"))
        params = dict(obj.get('params'))
        desc = obj.get('desc')
        response = obj.get('response')
        callback = obj.get('callback')
        expect = obj.get('expect')
        return Case(name, params, desc, response, callback, expect)

    def to_dict(self) -> dict:
        result = {}
        result['name'] = self.name
        result['params'] = self.params
        result['desc'] = self.desc
        result['response'] = self.response
        result['desc'] = self.desc
        result['callback'] = self.callback
        result['expect'] = self.expect
        return {k: result[k] for k in result if k in self.get_changed_keys()}

    def get_payload(self):
        return self.params

    def get_postman_desc_text(self):
        """
            将callback expect 字段放进postman的description字段，以完成用例互转
        :return:
        """
        res = {}
        if self.callback:
            res['callback'] = self.callback
        if self.expect:
            res['expect'] = self.expect
        if not res:
            return self.desc
        res["desc"] = self.desc
        return json.dumps(res)
