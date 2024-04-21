#FROM ghcr.io/osgeo/gdal:alpine-small-3.8.5
FROM python:3.9.6


ENV PYTHONUNBUFFERED=1

WORKDIR /code

RUN apt-get update && apt-get install --yes libgdal-dev

COPY requirements.txt .

RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install --trusted-host=pypi.org --trusted-host=files.pythonhosted.org  -r requirements.txt

COPY . .

EXPOSE 8000

CMD [ "python", "manage.py", "runserver" ]