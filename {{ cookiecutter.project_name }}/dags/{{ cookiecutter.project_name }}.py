"""
Code that goes along with the Airflow located at:
http://airflow.readthedocs.org/en/latest/tutorial.html
"""
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
import os

import sys
CODE_ROOT_PATH = os.getenv("CODE_ROOT_PATH")
sys.path.append(CODE_ROOT_PATH)
from dags.operators import generate_task_operator, dag_success

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


task_0_1_1 = generate_task_operator(dag, "0_1_1_{{cookiecutter.project_name}}_raw_data_combine.py",
                                    "{{ cookiecutter.author_phone }}")
task_1_1_1 = generate_task_operator(dag, "1_1_1_{{cookiecutter.project_name}}_data_clean.py",
                                    "{{ cookiecutter.author_phone }}")
task_2_1_1 = generate_task_operator(dag, "2_1_1_{{cookiecutter.project_name}}_feature_engineer.py",
                                    "{{ cookiecutter.author_phone }}")
task_3_1_1 = generate_task_operator(dag, "3_1_1_{{cookiecutter.project_name}}_model.py.",
                                    "{{ cookiecutter.author_phone }}")
task_4_1_1 = generate_task_operator(dag, "4_1_1_{{cookiecutter.project_name}}_ensemble.py",
                                    "{{ cookiecutter.author_phone }}")
task_5_1_1 = generate_task_operator(dag, "5_1_1_{{cookiecutter.project_name}}_project_output.py",
                                    "{{ cookiecutter.author_phone }}")

task_0_1_1 >> task_1_1_1 >> task_2_1_1 >> task_3_1_1 >> task_4_1_1 >> task_5_1_1


dag_finish_info = PythonOperator(
    task_id='DagSuccessInfo',
    python_callable=dag_success,
    dag=dag
)

# 最后一个 task，即整个 dag 运行结束的通知，可以不执行，看情况
task_5_1_1 >> dag_finish_info
