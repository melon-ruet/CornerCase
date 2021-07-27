FROM python:3.9

RUN pip install --upgrade pip
COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt

RUN mkdir -p /var/app
COPY lunch_selector /var/app

EXPOSE 8000

WORKDIR /var/app

ENTRYPOINT ["bash", "/var/app/entrypoint.sh"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]