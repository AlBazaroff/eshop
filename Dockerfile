FROM python:3.13.7
LABEL maintainer="bazaroffalex@gmail.com"

# set variables of environment
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# WORK DIRECTORY
WORKDIR /code

# SET DEPENDENTS
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

# COPY PROJECT
COPY . /code/