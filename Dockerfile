FROM python:3.8
WORKDIR /code
COPY . /code
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8000"]
