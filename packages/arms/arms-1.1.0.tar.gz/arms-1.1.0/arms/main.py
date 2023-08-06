from typing import Dict
import os
from lesscli import Application
import re
import json
import random
from arms.utils.wordstyle import replace_dict, replace_all, WordStyle, WordSeed
from arms.utils.common import dump_file_name
from pathlib import Path

PY2 = (type(b'') == str)


def makedir(real_path):
    from pathlib import Path
    Path(real_path).mkdir(parents=True, exist_ok=True)


def print_help():
    text = """

    arms init [git_url]         : 项目初始化（直接覆盖）
    arms patch [git_url]        : 项目补丁（保留重名文件）
    arms -h                     : show help information
    arms -v                     : show version


    """
    print(text)


def print_version():
    """
    显示版本
    """
    from arms import __version__
    text = """
    arms version: {}

    """.format(__version__)
    print(text)


def run_process(git_url, is_patch=False):
    """
    项目初始化工具
    """
    # [1/7]判断本地有.git目录
    if not os.path.isdir('.git'):
        print('Please change workdir to top! or run "git init" first.')
        exit(1)
    # [2/7]拉取模版项目
    os.system('rm -rf .arms_tpl && git clone %s .arms_tpl' % git_url)
    # [3/7]生成替换字典
    json_path = Path('.arms_tpl/.arms.json')
    if not json_path.is_file():
        print('No .arms.json found in source project!')
        exit(1)
    index_json = {}
    try:
        index_json.update(json.loads(json_path.open().read()))
    except Exception as e:
        print('.arms.json is not valid JSON format!')
        exit(1)
    if '__name__' not in index_json:
        print('.arms.json错误: __name__未定义!')
        exit(1)
    if '__only__' in index_json:
        if '__except__' in index_json:
            print('.arms.json错误: __only__和__except__不能同时定义!')
            exit(1)
        if '__rename__' in index_json:
            print('.arms.json错误: __only__和__rename__不能同时定义!')
            exit(1)
    if '__rename__' in index_json:
        if any(rule.count(':') != 1 for rule in index_json['__rename__']):
            print('.arms.json错误: __rename__不符合规范!')
            exit(1)
    old_proj_name = index_json['__name__']
    new_proj_name = input('请输入项目代号：')
    # [4/7]删除无用路径
    if index_json.get('__only__'):
        only_paths = [rule.split(':')[-1] for rule in index_json['__only__']]
        rename_rules = [rule for rule in index_json['__only__'] if ':' in rule]
    else:
        only_paths = ['.']
        rename_rules = index_json.get('__rename__', [])
    except_paths = index_json.get('__except__', [])
    tar_cmd = 'tar %s -czf ../.arms_tpl.tgz --exclude .git %s' % (
        ' '.join(f'--exclude {p}' for p in except_paths), ' '.join(only_paths))
    print(tar_cmd)
    os.system(' && '.join([
        'cd .arms_tpl',
        tar_cmd,
        'cd ..',
        'rm -rf .arms_tpl',
        'mkdir .arms_tpl',
        'cd .arms_tpl',
        'tar -zxf ../.arms_tpl.tgz',
        'rm -f ../.arms_tpl.tgz'
    ]))
    # [5/7]文件重命名
    repl_dict = replace_dict(old_proj_name, new_proj_name)
    # renames = index_json.get('__rename__', [])
    out_abs_path = os.path.abspath('.')
    os.chdir('.arms_tpl')  # 变换工作目录
    for item in rename_rules:
        to_path, from_path = item.split(':', 1)
        if Path(from_path).exists():  # 前面的重命名可能会影响后面的重命名
            os.rename(from_path, to_path)  # os.rename非常强大
    curpath = Path('.')
    for i in range(20):  # 替换路径中的项目代号，最大循环20轮
        touched = False
        renames = []
        for p in curpath.rglob('*'):
            full_path = str(p)
            new_path = replace_all(full_path, repl_dict)
            if new_path != full_path:
                renames.append(f'{new_path}:{full_path}')
        for item in renames:
            to_path, from_path = item.split(':', 1)
            if Path(from_path).exists():  # 前面的重命名可能会影响后面的重命名
                os.rename(from_path, to_path)  # os.rename非常强大
                touched = True
        if not touched:  # 若一轮操作没有产生重命名则退出
            break
    if is_patch:  # 通过重命名，保留重名文件
        midname = str(WordSeed(WordStyle.lower_snake, WordSeed.of(new_proj_name).tokens))
        out_path = Path('..')
        for p in curpath.rglob('*'):
            if p.is_file() and (out_path / p).is_file():
                new_file_name = dump_file_name(p.parts[-1], project=midname)
                p.rename('/'.join(p.parts[:-1] + (new_file_name,)))
    # [6/7]文本替换
    for p in curpath.rglob('*'):
        if p.is_dir() or str(p).startswith(('.git/', '.idea/', 'node_modules/')):
            continue
        try:
            text = p.open().read()
            new_text = replace_all(text, repl_dict)
            if new_text != text:
                with p.open('w') as f:
                    f.write(new_text)
        except Exception as e:
            pass
    # [7/7]git add
    os.system('tar -czvf ../.arms_tpl.tgz .')
    os.chdir(out_abs_path)  # 变换工作目录
    os.system(' && '.join([
        'rm -rf .arms_tpl',
        'tar -zxf .arms_tpl.tgz',
        'rm -f .arms_tpl.tgz'
    ]))
    os.system('git add .')
    if is_patch:
        print('---- arms patch succeed :) ----')
    else:
        print('---- arms init succeed :) ----')


def run_init(*args):
    """
    项目初始化工具
    arms init [git_url]
    """
    if len(args) != 1:
        print("请输入命令完成项目初始化：arms init [git_url]")
        exit(1)
    try:
        run_process(git_url=args[0], is_patch=False)
    finally:
        os.system('rm -rf .arms_tpl')
        os.system('rm -f .arms_tpl.tgz')


def run_patch(*args):
    """
    项目补丁工具
    arms patch [git_url]
    """
    if len(args) != 1:
        print("请输入命令完成项目补丁：arms patch [git_url]")
        exit(1)
    try:
        run_process(git_url=args[0], is_patch=True)
    finally:
        os.system('rm -rf .arms_tpl')


def entrypoint():
    if PY2:
        print('arms已不再支持python2，请安装python3.5+')
        exit(1)
    Application('armstrong')\
        .add('version', print_version)\
        .add('init', run_init) \
        .add('patch', run_patch) \
        .run()
