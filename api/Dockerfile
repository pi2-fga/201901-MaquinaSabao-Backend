FROM python:3.7
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
RUN pip install --upgrade --no-deps git+git://github.com/Theano/Theano.git
ADD . /code/
CMD python3 manage.py runserver 0.0.0.0:8000

