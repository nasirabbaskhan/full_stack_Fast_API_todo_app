FROM python:3.12

RUN pip install poetry

WORKDIR /code

COPY . /code/

RUN poetry install

CMD [ "poetry", "run", "dev" ]