# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.2'
#       jupytext_version: 1.0.3
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
# # 3_1_1_{{ cookiecutter.project_name }}_model
#
# ## 输入
# 运行 Notebook 依赖的外部数据
#  * 文件1 ： 简单说明
#  * 文件2 ： 简单说明
#  * ...
#
#
# ## 处理逻辑
# 本 notebook 的大致处理逻辑说明    
#
#  1. XXXXXX
#  2. XXXXXX
#  3. ....
#
#
# ## 输出
# 输出默认在 data_location/X_X_X
# * 输出文件的 key : 输出内容的简单描述

# %%
import numpy as np
import pandas as pd

import os
from pathlib import Path
import sys
import json
import logging

import argparse

from IPython.core.display import display

pd.options.display.max_columns = 200
pd.options.display.max_colwidth = 200
pd.options.display.max_rows = 200

# %%
# 通过 logger 的设置，使用 logging.XXX 输出比 print 更合适的 信息
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
# 此处 filename/lineno 的显示在 jupyter 里面运行时没有意义，但在通过 airflow 调用时，可以提供合理的文件名与
#  log 所在行数，比较有意义，故需要保留
formatter = logging.Formatter('%(asctime)s - %(filename)s:%(lineno)d - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger.handlers = [handler]

# %%
# %load_ext autoreload
# %autoreload 2

# %%
sys.path.append(os.getenv("CODE_ROOT_PATH"))
from src.template_util import transform_args_data, get_output_folder

# %% [markdown]
# # 外部数据的输入
# 后面的所有执行使用的外部环境变量通过这里设置，未来直接调用 python 文件的时候，通过 python script.py --args="abc" 来设置
# 而对于 jupyter notebook 的调试，可以通过设置的 default 值，来设置 jupyter container 下的路径
# 由于 airflow 和 jupyter 是两个不同的 container，它们的路径不通用（故意的，以防导入文件出错）

# %%
script_input_parser = argparse.ArgumentParser(description='设置 flow参数')

# 如果通过外部调用，使用如下命令行    
#  python XXXXX.py  --data_location=to_save_output_location
# 在 notebook 里面 default 就是 None 吧，会自动设置为 data_location/X_X_X/ 目录下输出
script_input_parser.add_argument('--data_location', type=str, default=None)
script_input_parser.add_argument('--file_a', type=str, default="1_1_1:file_a")
script_input_parser.add_argument('--file_b', type=str, default="1_2_1:file_b.txt")

# %% [markdown]
# workflow 如果需要调试，替换路径的话，为了减少对基于 Notebook 下的工作的影响，可以在这里设置

# %%
from IPython.core.display import Javascript
from IPython.display import display as idisplay

idisplay(Javascript('IPython.notebook.kernel.execute("theNotebook = " + \
    "\'"+IPython.notebook.notebook_name+"\'");'))

# %%
if 'theNotebook' in globals():
    cur_name = theNotebook
else:
    cur_name = os.path.basename(__file__)

# %%
# 使用这个来忽律系统额外传过来的参数
args, _ = script_input_parser.parse_known_args()
args.data_location = get_output_folder(args.data_location)

# 如果需要调试 airflow，请在这里更改赋值路径，比如 args.file_a = "XXXXX"
#

for arg in vars(args):
    got_file_path = getattr(args, arg)
    # 把类似于 X_X_X:file_name 转换为真实的文件路径
    setattr(args, arg, transform_args_data(got_file_path, args.data_location, cur_name))

cur_task_output_folder = os.path.join(args.data_location, cur_name)
if not os.path.exists(cur_task_output_folder):
    os.makedirs(cur_task_output_folder)

# %% [markdown]
# # Your Show Time
# 请开始你的表演

# %%
logging.info('hi')

