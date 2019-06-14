# coding: utf-8
import json
from os import makedirs
from os.path import dirname, realpath, join, exists, expanduser
from shutil import copyfile

cur_dir = dirname(realpath(__file__))


def get_file_realpath(file):
    return join(cur_dir, file)


# 检查并创建文件
def check_and_create_file(absolute_file_path):
    if not  exists(absolute_file_path) :
        tmp_dir = dirname(absolute_file_path)
        if not exists(tmp_dir):
            makedirs(tmp_dir)
        with open(absolute_file_path, "w+") as f:
            pass


# 检查并创建目录
def check_and_create_dir(absolute_dir_path):
    if not  exists(absolute_dir_path) :
        makedirs(absolute_dir_path)


# 复制sqlite配置文件到用户个人目录
def check_and_create_sqlite_file(config_path):
    if not exists(config_path) :
        check_and_create_dir(dirname(config_path))
    copyfile(get_file_realpath("../data/data.db"), config_path)

    
def load_josn_config(project_name):
    config_file_path = join(expanduser("~"), ".config", project_name, "config.json")
    if not exists(config_file_path):
        return
    with open(config_file_path, "r", encoding="utf-8") as f:
        content = f.read().strip()
        if content != "":
            return json.loads(content)


def save_json_config(project_name, obj):
    config_file_path = join(expanduser("~"), ".config", project_name, "config.json")
    check_and_create_file(config_file_path)
    with open(config_file_path, "w", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False, indent=4))
    
