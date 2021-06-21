# pull official base image
FROM python:3.8 AS build
# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update && apt-get install -y netcat

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

# copy app
COPY . /usr/src/app/

# Build stage test - run tests
FROM build AS test
RUN pip3 install pytest pytest-cov && rm -rf /root/.cache
RUN pytest planete_oui_app/tests/test_client.py --doctest-modules \
  --junitxml=xunit-reports/xunit-result-all.xml \
  --cov \
  --cov-report=xml:coverage-reports/coverage.xml \
  --cov-report=html:coverage-reports/

# run entrypoint.sh
FROM test AS final
ENTRYPOINT ["python","./run.py"]
