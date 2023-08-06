FROM python:3.9

ARG SETUPTOOLS_SCM_PRETEND_VERSION

ENV PIP_NO_CACHE_DIR 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN pip install -e .

ENTRYPOINT ["dbnomics-validate"]
