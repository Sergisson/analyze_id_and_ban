FROM python:3.10-slim-bullseye

ENV POETRY_VERSION=1.3.1

WORKDIR /sanic

RUN pip install "poetry==$POETRY_VERSION"

ADD pyproject.toml ./pyproject.toml
ADD poetry.lock ./poetry.lock

RUN poetry config virtualenvs.create false
RUN poetry install --no-dev --no-root

ADD src /sanic/src

EXPOSE 8000

CMD ["python", "-m", "src"]