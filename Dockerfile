FROM python:3.12-slim

RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/* \
    && useradd -m qauser

WORKDIR /app

# Instalar pipenv
RUN pip install --no-cache-dir --only-binary :all: pipenv==2024.0.1 # NOSONAR

COPY Pipfile Pipfile.lock ./


RUN pipenv sync --system


COPY --chown=qauser:qauser . .

USER qauser


CMD ["pytest", "tests/test_bdd_voz.py", "--alluredir=allure-results"]