FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg && rm -rf /var/lib/apt/lists/* \
    && useradd -m qauser

WORKDIR /app

RUN python -c \
    "import subprocess; subprocess.run([ \
    'pip', 'install', '--no-cache-dir', \
    '--only-binary', ':all:', 'pipenv==2024.0.1' \
    ], check=True)"

COPY Pipfile Pipfile.lock ./


RUN pipenv sync --system


COPY tests/ tests/
COPY features/ features/
COPY datasets/ datasets/
COPY *.py config.json ./

RUN mkdir -p allure-results && chown -R qauser:qauser /app

USER qauser


CMD ["pytest", "tests/test_bdd_voz.py", "--alluredir=allure-results"]