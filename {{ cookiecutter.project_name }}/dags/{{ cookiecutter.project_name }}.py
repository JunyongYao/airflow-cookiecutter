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
code_root_dir = os.path.join(CODE_ROOT_PATH, "{}/notebooks".format("{{cookiecutter.project_name}}"))

{{cookiecutter.project_name}}_output_root = os.path.join(DATA_ROOT_DIR, "output_".format(datetime.now()))


task_0_1_1 = BashOperator(
    task_id='0_1_1_{{cookiecutter.project_name}}_raw_data_combine',
    bash_command='python {}/0_1_1_{{cookiecutter.project_name}}_raw_data_combine.py --data_location={}'.format(
        code_root_dir, {{cookiecutter.project_name}}_output_root),
    dag=dag,
)

task_1_1_1 = BashOperator(
    task_id='1_1_1_{{cookiecutter.project_name}}_data_clean',
    bash_command='python {}/1_1_1_{{cookiecutter.project_name}}_data_clean.py --data_location={}'.format(
        code_root_dir, {{cookiecutter.project_name}}_output_root),
    dag=dag,
)

task_2_1_1 = BashOperator(
    task_id='2_1_1_{{cookiecutter.project_name}}_feature_engineer',
    bash_command='python {}/2_1_1_{{cookiecutter.project_name}}_feature_engineer.py --data_location={}'.format(
        code_root_dir, {{cookiecutter.project_name}}_output_root),
    dag=dag,
)

task_3_1_1 = BashOperator(
    task_id='3_1_1_{{cookiecutter.project_name}}_model',
    bash_command='python {}/3_1_1_{{cookiecutter.project_name}}_model.py --data_location={}'.format(
        code_root_dir, {{cookiecutter.project_name}}_output_root),
    dag=dag,
)

task_4_1_1 = BashOperator(
    task_id='4_1_1_{{cookiecutter.project_name}}_raw_data_combine',
    bash_command='python {}/4_1_1_{{cookiecutter.project_name}}_raw_data_combine.py --data_location={}'.format(
        code_root_dir, {{cookiecutter.project_name}}_output_root),
    dag=dag,
)

task_5_1_1 = BashOperator(
    task_id='5_1_1_{{cookiecutter.project_name}}_project_output',
    bash_command='python {}/5_1_1_{{cookiecutter.project_name}}_project_output.py --data_location={}'.format(
        code_root_dir, {{cookiecutter.project_name}}_output_root),
    dag=dag,
)

task_0_1_1 >> task_1_1_1 >> task_2_1_1 >> task_3_1_1 >> task_4_1_1 >> task_5_1_1



