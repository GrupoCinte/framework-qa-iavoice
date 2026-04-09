# 🎙️ Auditoría de IA - Voice-QA Enterprise Suite

Framework de automatización de pruebas BDD (Behavior-Driven Development) diseñado para evaluar la calidad, latencia y seguridad de asistentes virtuales de voz (Voicebots).
Esta solución implementa un enfoque de auditoría multimodal: utiliza **Pytest-BDD** para la orquestación de escenarios, **OpenAI Whisper** para evaluar la dicción (WER), y **Sentence Transformers** para validar el entendimiento semántico de la IA.

Diseñado para integrarse en pipelines y asegurar la resiliencia del Voicebot ante ruido ambiental y ataques de ciberseguridad.

## Tech Stack

* **Lenguaje:** Python 3.12
* **Build Tool/Runner:** Pytest + Pytest-BDD
* **NLP Core (Transcripción):** OpenAI Whisper (Modelo Base)
* **NLP Core (Semántica):** Sentence Transformers (MiniLM)
* **Audio Processing:** Pydub + FFmpeg
* **Mock Server:** Flask + gTTS
* **Reporting:** Allure Framework

## Estructura del Proyecto

```text
voice-qa-suite/
├── datasets/
│   └── [archivos .mp3]               # Audios de prueba del usuario y pistas de ruido
├── features/
│   └── evaluacion_voz.feature        # Escenarios Gherkin para la evaluación de la IA
├── tests/
│   ├── test_demo.py                  # Prueba matriz inicial
│   └── test_bdd_voz.py               # ⚡ MOTOR BDD: Evaluador de Voz, Ruido y Semántica
├── mock_bot.py                       # 🤖 MOCK API: Servidor Flask que simula al Bot Financiero
├── ejecutar_pruebas.py               # Orquestador que lanza la suite y construye el Dashboard
├── config.json                       # Configuración de URLs y Umbrales de Calidad (Cinte)
├── requirements.txt                  # Dependencias de Python
├── Dockerfile                        # Imagen aislada para ejecución sin dependencias locales
└── README.md                         # Documentación del proyecto

##  Requisitos Previos
* **Python 3.12+** instalado y configurado en el PATH.

* **FFmpeg** instalado (Obligatorio para que Whisper y Pydub puedan procesar los MP3).
*


* **Google Chrome** instalado (para ejecución local).

* Acceso a la red/VPN donde reside el ambiente de QA de Orbit.