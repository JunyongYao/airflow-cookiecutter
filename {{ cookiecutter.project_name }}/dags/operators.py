"""
Code that goes along with the Airflow located at:
http://airflow.readthedocs.org/en/latest/tutorial.html
"""
import os

from airflow.operators.bash_operator import BashOperator
from datetime import datetime

import json
import requests

DATA_ROOT_DIR = os.getenv("DATA_PATH")
CODE_ROOT_PATH = os.getenv("CODE_ROOT_PATH")
jupyter_root_dir = os.path.join(CODE_ROOT_PATH, "jupyter")

DEFAULT_CONTRACTOR = "{{ cookiecutter.author_phone }}"
task_owner_map = {}

md_template = """
# 调试 {notebook_name}

1. 打开 notebook 的时候，请确保对其有编辑权限，以防后面无法保存，白忙一场
2. 保存 notebook 会自动更新对应的 py 文件，然后可以手动触发对应的 task rerun 即可
3. <font color='red'>人人为我，我为人人。</font> 请多提建议！

点击[**这里**]({notebook_url}) 打开对应 notebook 调试~ 

            """


def send_dingding_info(data):
    raise NotImplementedError("Please add access_token below")
    web_hook = "https://oapi.dingtalk.com/robot/send?access_token="
    headers = {'content-type': 'application/json'}  # 请求头
    r = requests.post(web_hook, headers=headers, data=json.dumps(data))
    r.encoding = 'utf-8'
    print(r.text)


def task_failure_callback(context):
    fail_task = context['task_instance'].task_id
    global task_owner_map
    if fail_task in task_owner_map.keys():
        contractor = task_owner_map[fail_task]
    else:
        contractor = DEFAULT_CONTRACTOR

    data = {
        "msgtype": "text",
        "text": {
            "content": "airflow alert: \n"
                       "Task: '{}' failed!\n"
                       "Reason: {}\n".format(fail_task, context['exception'])
        },
        "at": {
            "atMobiles": [contractor],
            "isAtAll": False
        }
    }
    print(f"Need to send info to {contractor} for failed task {fail_task}")
    if contractor:
        send_dingding_info(data)


def generate_task_operator(dag, task_file, owner_phone):
    # 这个路径和 dag 的实例相关，每个实例开始运行的时间，即为 latest_execution_date，但 rerun 会有问题
    if dag.latest_execution_date:
        time_str = dag.latest_execution_date.strftime("%Y-%m-%d_%H%M%S")
    else:
        time_str = datetime.now().strftime("%Y-%m-%d_%H%M%S")

    last_dag_output = os.path.join(DATA_ROOT_DIR, "output", time_str)
    if not os.path.exists(last_dag_output):
        os.makedirs(last_dag_output)

    task_file_full_path = os.path.join(jupyter_root_dir, task_file)
    file_url = task_file_full_path.replace(os.getenv("JUPYTER_ROOT_PATH"), "/notebook/notebooks/")
    task_id = task_file.split(".")[0]
    global task_owner_map
    task_owner_map[task_id] = owner_phone
    base_task = BashOperator(
        task_id=task_id,
        bash_command='python {} --data_location={}'.format(task_file_full_path, last_dag_output),
        on_failure_callback=task_failure_callback,
        dag=dag)
    base_task.doc_md = md_template.format(notebook_url=file_url,
                                          notebook_name=os.path.basename(task_file))
    return base_task


def dag_success():
    data = {
        "msgtype": "text",
        "text": {
            "content": f"airflow info: Dags finished at {datetime.now()}"
        },
        "at": {
            "atMobiles": [DEFAULT_CONTRACTOR]
        }
    }

    send_dingding_info(data)
