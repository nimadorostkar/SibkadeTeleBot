FROM python:3.10-slim-buster

WORKDIR /bot_panel_back

COPY /requirements.txt /bot_panel_back/requirements/

RUN pip install --upgrade pip

RUN apt-get update && apt-get upgrade -y

RUN pip install -r requirements/requirements.txt

COPY . /bot_panel_back

EXPOSE 8000 9000