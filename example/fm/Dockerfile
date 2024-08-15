FROM python:3.10
WORKDIR /aigear/fm/
COPY . /aigear/fm/
COPY requirements.txt /aigear/fm/requirements.txt

RUN python -m pip install --upgrade pip
RUN python -m pip install -r /aigear/fm/requirements.txt
RUN python -m pip install aigear-0.0.1-py3-none-any.whl

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONBUFFERED=1
