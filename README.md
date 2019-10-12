# Cookiecutter Data Science

_A logical, reasonably standardized, but flexible project structure for doing and sharing data science work._


#### [Project homepage](http://drivendata.github.io/cookiecutter-data-science/)


### Requirements to use the cookiecutter template:
-----------
 - Python 2.7 or 3.5
 - [Cookiecutter Python package](http://cookiecutter.readthedocs.org/en/latest/installation.html) >= 1.4.0: This can be installed with pip by or conda depending on how you manage your Python packages:

``` bash
$ pip install cookiecutter
```

or

``` bash
$ conda config --add channels conda-forge
$ conda install cookiecutter
```


### To start a new project, run:
------------

    cookiecutter https://github.com/JunyongYao/airflow-cookiecutter


[![asciicast](https://asciinema.org/a/244658.svg)](https://asciinema.org/a/244658)


And then, you need to go to docker folder, build the docker images with 
```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d 
```

to start the containers. By default, all the default notebooks can be found there.   

Be careful about the volumn mapping in docker-compose.prod.yml or docker-compose.user.yml file. 

### The resulting directory structure
------------

The directory structure of your new project looks like this: 

```
├── LICENSE
├── Makefile           <- Makefile with commands like `make data` or `make train`
├── README.md          <- The top-level README for developers using this project.
├── dags               <- The airflow dags entry to define task's sequence
├── data
│   ├── output         <- Data generate by notebooks
│   └── raw            <- The original, immutable data dump.
│
├── docker             <- The docker file definition to run project
│   └── airflow        <- airflow docker definition if you want to run tasks auto
│   └── jupyter        <- jupyter docker definition if you want to debug
│   └── ngnix          <- interal proxy reverse server
│
├── docs               <- A default Sphinx project; see sphinx-doc.org for details
│
├── models             <- Trained and serialized models, model predictions, or model summaries
│
├── notebooks          <- Jupyter notebooks. Naming convention is a X_X_X number (for ordering),
│                         and a short `_` delimited description, e.g.
│                         `1_1_1_initial-data-exploration`.
│
├── references         <- Data dictionaries, manuals, and all other explanatory materials.
│
├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
│   └── figures        <- Generated graphics and figures to be used in reporting
│
├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
│                         generated with `pip freeze > requirements.txt`
│
├── src                <- Source code for use in this project.
│   ├── __init__.py    <- Makes src a Python module
│   ├── template_util.py   <- Some function used by notebook template
│   │
│   ├── data           <- Scripts to download or generate data
│   │   └── make_dataset.py
│   │
│   ├── features       <- Scripts to turn raw data into features for modeling
│   │   └── build_features.py
│   │
│   ├── models         <- Scripts to train models and then use trained models to make
│   │   │                 predictions
│   │   ├── predict_model.py
│   │   └── train_model.py
│   │
│   └── visualization  <- Scripts to create exploratory and results oriented visualizations
│       └── visualize.py
│
└── tox.ini            <- tox file with settings for running tox; see tox.testrun.org
```

### Installing development requirements
------------

    pip install -r requirements.txt

### Running the tests
------------

    py.test tests
