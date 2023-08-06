import os
import json
import click
from importlib import import_module
from .postman import Collection
from .project import Project
from .lib.case import Information
from .lib.utils import logger


def parse_postman_collection_to_casefile(path, casedir):
    obj = Collection.load_from_file(path)
    obj.gen_web_test_case_file(casedir)


def parse_casefile_to_postman_collection(path, to_file_path):
    name = path.split('/')[-1][0]
    project = Project(path=path)
    project.load_scene()
    c = Collection(
        info=Information(
            description='auto parsed from webapitest. https://gitee.com/wow_1/webapitest',
            name=name,
            postman_id=None,
            schema='https://schema.getpostman.com/json/collection/v2.1.0/collection.json',
            version=None
        ),
        item=project.get_scene_items(),
        auth=None,
        event=None,
        protocol_profile_behavior=None,
        variable=None
    )
    res = json.dumps(c.to_dict(), indent=4, ensure_ascii=False)
    f = open(to_file_path, 'w')
    f.write(res)
    f.close()
    return c


@click.group()
def cli():
    pass


@click.command(help="将Postman的用例文件转化为webapitest标准用例文件")
@click.argument('path')
# @click.option('--path', prompt='Postman用例文件路径地址', help='eg. Postman右键导出，生成文件deal.collection.json')
@click.option('--casedir', prompt='导出用例文件夹名', help='eg: cases 导出用例将放在当前位置的cases文件夹中')
def parse(path, casedir):
    current_dir = os.getcwd()
    if not path.startswith('/'):
        path = os.path.join(current_dir, path)
    if not casedir.startswith('/'):
        casedir = os.path.join(current_dir, casedir)
    parse_postman_collection_to_casefile(path, casedir)


@click.command(help="将Postman的用例文件转化为webapitest标准用例文件")
@click.argument('casedir')
@click.option('--postmanfile', prompt='导出Postman用例文件名', help='eg: deal.json')
def parse2postmanfile(casedir, postmanfile):
    current_dir = os.getcwd()
    if not casedir.startswith('/'):
        casedir = os.path.join(current_dir, casedir)
    if not postmanfile.startswith('/'):
        postmanfile = os.path.join(current_dir, postmanfile)
    parse_casefile_to_postman_collection(casedir, postmanfile)


def get_project_cls():
    settings = import_module('conf.settings')
    c = getattr(settings, 'current_project')
    return getattr(settings, c)


@click.command()
def cleandb():
    get_project().clean_db()


@click.command()
def startwebserver():
    get_project().start_webserver()


@click.command()
def initdb():
    logger.info("initdb")
    get_project().init_db()


def get_project(path):
    project_cls = get_project_cls()
    if path == 'default':
        p = project_cls.gen()
    else:
        if not path.startswith('/'):
            current_dir = os.getcwd()
            casedir = os.path.join(current_dir, path)
        p = get_project_cls().gen(path=casedir, relative_path=path)
    return p


@click.command(help='执行用例')
@click.argument('path', default='default')
def runcase(path):
    logger.info("runcase " + path)
    p = get_project(path)
    p.load_cookie()
    p.run()


@click.command()
@click.argument('casedir', default='default')
def createcsv(casedir):
    logger.info("createcsv " + casedir)
    get_project(casedir).create_scv()


@click.command()
@click.argument('casedir', default='default')
def checkcsv(casedir):
    logger.info("checkcsv " + casedir)
    get_project(casedir).check_csv()


@click.command()
@click.argument('casedir', default='default')
def resetjsonbycsv(casedir):
    logger.info('resetjsonbycsv ' + casedir)
    get_project(casedir).reset_json_by_csv()


@click.command()
def run():
    logger.info('run')


functions = [
    parse,
    parse2postmanfile,
    cleandb,
    runcase,
    initdb,
    createcsv,
    checkcsv,
    resetjsonbycsv,
]
for f in functions:
    cli.add_command(f)


if __name__ == '__main__':
    cli()
