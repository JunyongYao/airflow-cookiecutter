# 统一一个版本，后续好操作, 该版本在 2018-10-25 官网更新
# https://github.com/puckel/docker-airflow/blob/master/Dockerfile
FROM  puckel/docker-airflow:1.10.4
MAINTAINER Junyong Yao <ruskeeyao@gmail.com>

USER root
COPY pip.conf /root/.pip/pip.conf
RUN pip install --upgrade pip

RUN pip install lightgbm==2.2.2
RUN pip install xgboost==0.81
RUN pip install scikit-learn==0.20.3
RUN pip install bdranalytics==0.3

RUN pip install pandas==0.25.* && \
    pip install numpy==1.15.4 && \
    pip install MLFeatureSelection==0.0.8.2 && \
    pip install hyperopt==0.1.1

RUN pip install xlrd==1.2.0 && \
    pip install logger==1.4

RUN pip install openpyxl==2.5.12
RUN pip install pyarrow==0.11.1
RUN pip install ipython==7.3.0

RUN pip install gensim==3.7.1

RUN pip install tsfresh==0.14.*
RUN pip install rgf-python==3.5.0

USER airflow
ADD airflow.cfg .
ENV PYTHONPATH=/usr/local/airflow/jupyter:/usr/local/airflow/submodules:/usr/local/airflow/submodules/gaia:/usr/local/airflow/tmp_data
