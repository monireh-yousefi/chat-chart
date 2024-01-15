FROM python:3.11-alpine

WORKDIR /app/

# Install python dependencies.
RUN pip install poetry
COPY ./pyproject.toml ./poetry.lock /app/
RUN poetry config virtualenvs.create false \
  && poetry install --no-dev --no-interaction --no-ansi

# Copy source files.
COPY . /app/

# Run the command.
WORKDIR /app/src/
CMD python main.py
