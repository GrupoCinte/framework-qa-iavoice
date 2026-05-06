FROM python:3.12-slim

RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/* \
    && useradd -m qauser

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --only-binary :all: --no-binary openai-whisper -r requirements.txt

COPY --chown=qauser:qauser . .

USER qauser

CMD ["pytest", "tests/test_bdd_voz.py", "--alluredir=allure-results"]