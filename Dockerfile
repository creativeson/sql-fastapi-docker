FROM python:3.7
WORKDIR /code/app
COPY . /code
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
EXPOSE 80

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]

