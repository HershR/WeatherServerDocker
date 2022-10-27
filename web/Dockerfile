FROM python:3.8
ENV PYTHONNUMBUFFERED 1

RUN mkdir /code
WORKDIR /code

COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt
 COPY . /code/
EXPOSE 5000
CMD python run.py
#CMD gunicorn --bind 0.0.0.0:5000 -w 3 run:app