FROM python:3.8.8-buster

# ------------------------------------------------------
ARG ENVIRONMENT=production
ENV FLASK_ENV=${ENVIRONMENT}

COPY . /app


#  Dependencias de python
# ------------------------------------------------------
WORKDIR /app
RUN pip3 install -r requirements.txt
ENV FLASK_APP=run.py
CMD flask run --host=0.0.0.0 --port=80
