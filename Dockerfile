FROM python:3.12-slim

RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*


RUN useradd -m qauser

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chown -R qauser:qauser /app

USER qauser

CMD ["pytest", "tests/test_bdd_voz.py", "--alluredir=allure-results"]