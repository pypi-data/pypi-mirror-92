FROM registry.gitlab.com/ftrotta/python3.6-ubuntu18.04:develop-01

ADD requirements/ requirements/

RUN pip install --upgrade pip setuptools twine &&\
    pip install -r requirements/requirements.txt &&\
    rm -fr requirements/
