# 统一一个版本，后续好操作, 该版本在 2018-10-03 官网更新
FROM  jupyter/tensorflow-notebook:1145fb1198b2
LABEL maintainer="Junyong Yao <ruskeeyao@gmail.com>"
ENV VERSION=1.1

USER root
COPY pip.conf /etc/pip.conf
COPY sources.list /etc/apt/sources.list

RUN apt-get -qq update && \
    apt-get install -y python-dev && \
    apt-get install -y default-libmysqlclient-dev && \
    apt-get install -y libgomp1

RUN conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
RUN conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
RUN conda config --set show_channel_urls yes
RUN conda install -y python=3.7

USER $NB_UID
RUN pip install --upgrade pip
RUN pip install jupyter_contrib_nbextensions
RUN jupyter contrib nbextension install --user

RUN pip install xgboost==0.81 && \
    pip install lightgbm==2.2.2 && \
    pip install catboost==0.12.1 && \
    pip install mysqlclient==1.3.14 && \
    pip install SQLAlchemy==1.2.12 && \
    pip install pyarrow==0.11.1 && \
    pip install tqdm==4.28.1 && \
    pip install mlxtend==0.14.0 && \
    pip install pyecharts==1.*

RUN pip install pandas-profiling==1.4.1 && \
    pip install jupyterthemes==0.20.0 && \
    pip install autopep8==1.4.3

RUN pip install fbprophet==0.4

RUN pip install jupyter-tensorboard==0.1.8 && \
    pip install pydot==1.4.1 && \
    pip install pydot-ng==2.0.0 && \
    pip install graphviz==0.10.1

RUN pip install hyperopt==0.1.1 && \
    pip install eli5==0.8.1 && \
    pip install openpyxl==2.5.12

RUN pip install bdranalytics==0.3 && \
    pip install MLFeatureSelection==0.0.8.2

RUN pip install cookiecutter==1.6.0

RUN pip install line-profiler==2.1.2 && \
    pip install psutil==5.4.8 && \
    pip install memory_profiler==0.55.0

# 更新一些配置文件
RUN ipython profile create
ADD extensions/line_profiler_ext.py  .ipython/extensions/
ADD profile/ipython_config.py .ipython/profile_default/

#RUN jt -t grade3 -fs 95 -tfs 11 -nfs 115 -cellw 88% -T

# 开启一些需要的 extentions
RUN jupyter serverextension enable jupyter_tensorboard --user && \
    jupyter nbextension enable jupyter_tensorboard/tree --user && \
    jupyter nbextension enable execute_time/ExecuteTime --user && \
    jupyter nbextension enable toc2/main --user

RUN pip install jupytext==1.0.3
ADD profile/jupyter_notebook_config.py .jupyter/
ADD profile/custom.js .jupyter/custom/

RUN pip install gensim==3.7.1
RUN pip install pandas==0.24.1

# 初始化：用户、路径
ENV PYTHONPATH=/home/jovyan/submodules:/home/jovyan/submodules/gaia:/home/jovyan/work
