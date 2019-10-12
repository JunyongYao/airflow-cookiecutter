"""
Code that goes along with the Airflow located at:
http://airflow.readthedocs.org/en/latest/tutorial.html
"""
import os

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime


default_args = {
    "owner": "{{ cookiecutter.author_name }}",
    "depends_on_past": True,  # 只要之前的有 fail，之后的都不执行
    "start_date": datetime(2018, 12, 29),  # 手动执行，所以，设置一个非常未来的值
    "catchup": False,
    "email": None,
    "email_on_failure": False,
    "email_on_retry": False,
}

dag = DAG("{{ cookiecutter.project_name }}", default_args=default_args, schedule_interval=None)
dag.doc_md = __doc__

DATA_ROOT_DIR = os.getenv("DATA_PATH")
CODE_ROOT_PATH = os.getenv("CODE_ROOT_PATH")
jupyter_root_dir = os.path.join(CODE_ROOT_PATH, "jupyter")


md_template = """
# 调试 {notebook_name}

1. 打开 notebook 的时候，请确保对其有编辑权限，以防后面无法保存，白忙一场
2. 保存 notebook 会自动更新对应的 py 文件，然后可以手动触发对应的 task rerun 即可
3. <font color='red'>人人为我，我为人人。</font> 请多提建议！
   
点击[**这里**]({notebook_url}) 打开对应 notebook 调试~ 

            """


def generate_task_operator(task_file):
    # 这个路径和 dag 的实例相关，每个实例开始运行的时间，即为 latest_execution_date，但 rerun 会有问题
    task_file_full_path = os.path.join(jupyter_root_dir, task_file)
    last_dag_output = os.path.join(
        DATA_ROOT_DIR, "output", dag.latest_execution_date.strftime("%Y-%m-%d_%H%M%S"))
    if not os.path.exists(last_dag_output):
        os.makedirs(last_dag_output)

    file_url = task_file_full_path.replace(os.getenv("JUPYTER_ROOT_PATH"), "/notebook/notebooks/")
    base_task = BashOperator(
        task_id=task_file.split(".")[0],
        bash_command='python {} --data_location={}'.format(task_file_full_path, last_dag_output),
        dag=dag)
    base_task.doc_md = md_template.format(notebook_url=file_url,
                                          notebook_name=os.path.basename(task_file))
    return base_task


task_0_1_1 = generate_task_operator("0_1_1_{{cookiecutter.project_name}}_raw_data_combine.py")
task_1_1_1 = generate_task_operator("1_1_1_{{cookiecutter.project_name}}_data_clean.py")
task_2_1_1 = generate_task_operator("2_1_1_{{cookiecutter.project_name}}_feature_engineer.py")
task_3_1_1 = generate_task_operator("3_1_1_{{cookiecutter.project_name}}_model.py.")
task_4_1_1 = generate_task_operator("4_1_1_{{cookiecutter.project_name}}_raw_data_combine.py")
task_5_1_1 = generate_task_operator("5_1_1_{{cookiecutter.project_name}}_project_output.py")

task_0_1_1 >> task_1_1_1 >> task_2_1_1 >> task_3_1_1 >> task_4_1_1 >> task_5_1_1



