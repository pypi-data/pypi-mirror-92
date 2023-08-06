import json

class JsonDataValueValidator:
    """
        response 结果校验 主要是数据校验
    """
    def validate(self, value):
        return


class JsonDataFormatValidator:
    """
        response 结果校验 主要是格式校验
    """
    def validate(self, value):
        return


class StatusValidator:
    def validator(self, value):
        return


def check_status_200(project, scene, case_name, resp):
    res = 200 <= resp.status_code < 400
    if res:
        return True
    project.result['errlist'].append({
        "case_name": case_name,
        "scene_name": scene.name,
        "path": resp.request.url,
        "message": 'err status code: %s' % resp.status_code,
        "resp": resp.content
    })


def check_status_400(project, scene, case_name, resp):
    res = resp.status_code == 400
    if res:
        return True
    project.result['errlist'].append({
        "case_name": case_name,
        "scene_name": scene.name,
        "path": resp.request.url,
        "message": 'err status code: %s' % resp.status_code,
        "resp": resp.content
    })


def check_list_empty(project, scene, case_name, resp):
    content = json.loads(resp.content)
    return len(content['data']) == 0


def check_list_not_empty(project, scene, case_name, resp):
    content = json.loads(resp.content)
    return len(content['data']) > 0
