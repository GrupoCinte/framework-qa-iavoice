FROM python:3.12-slim

RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/* \
    && useradd -m qauser

WORKDIR /app

# Instalar pipenv
RUN pip install --no-cache-dir pipenv

COPY Pipfile Pipfile.lock ./


RUN pipenv install --system --deploy


COPY --chown=qauser:qauser . .

USER qauser


CMD ["pytest", "tests/test_bdd_voz.py", "--alluredir=allure-results"]