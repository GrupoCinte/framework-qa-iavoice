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
├── .github/
│   └── workflows/
│       └── voice-qa-pipeline.yml     # Pipeline de ejecución automática en la nube
├── datasets/
│   └── [archivos .mp3]               # Audios de prueba del usuario y pistas de ruido
├── docs/                             # Diagramas de arquitectura y flujos del framework
├── features/
│   └── evaluacion_voz.feature        # Escenarios Gherkin para la evaluación de la IA
├── tests/
│   ├── test_demo.py                  # Prueba matriz inicial
│   └── test_bdd_voz.py               # ⚡ MOTOR BDD: Evaluador de Voz, Ruido y Semántica
├── mock_bot.py                       # 🤖 MOCK API: Servidor Flask que simula al Bot Financiero
├── ejecutar_pruebas.py               # Orquestador que lanza la suite y construye el Dashboard
├── config.json                       # Configuración de URLs y Umbrales de Calidad
├── requirements.txt                  # Dependencias de Python
├── Dockerfile                        # Imagen aislada para ejecución sin dependencias locales
└── README.md                         # Documentación del proyecto
```
##  Requisitos Previos
* **Python 3.12+** instalado y configurado en el PATH.
* **FFmpeg** instalado (Obligatorio para que Whisper y Pydub puedan procesar los MP3).
* **Allure Commandline** instalado (solo si deseas visualizar los reportes en tu máquina local)

## Instalación
1. Clona este repositorio:
   ```bash
   git clone <repository-url>
    cd voice-qa-suite
    ```
2. Crea y activa tu entorno virtual:
   ```bash
    python -m venv venv

    # En Windows:
    .\venv\Scripts\activate

    # En Mac/Linux:
    source venv/bin/activate   
   ```

3. Instala las dependencias del proyecto:
   ```bash
    pip install -r requirements.txt
    pip install sentence-transformers pydub 
   ```

## 🚀 Ejecución de Pruebas (Local)
El proceso consta de dos fases que deben ejecutarse en terminales simultáneas: levantar el entorno del bot y lanzar la auditoría.
### Paso 1: Iniciar el Voicebot (Terminal 1)
Abre una terminal, activa el entorno virtual y levanta la API simulada:
```bash
python mock_bot.py
```
(El bot quedará escuchando en el puerto 5000).
### Paso 2: Lanzar la Auditoría BDD (Terminal 2)
Abre una segunda terminal, activa el entorno y ejecuta el orquestador:
```bash
python ejecutar_pruebas.py
```
(Esto enviará los audios, evaluará las respuestas, calculará las métricas y abrirá el Dashboard de Allure en tu navegador).

## Integración Continua (GitHub Actions)
El proyecto está configurado para ejecutarse automáticamente en la nube sin intervención manual.
1. **Activación:** El pipeline (voice-qa-pipeline.yml) se dispara automáticamente al hacer push o pull_request sobre la rama main y sobre cualquier rama de desarrollo (feature/*).
2. **Entorno:** GitHub Actions se encarga de instalar FFmpeg, levantar el bot en segundo plano y lanzar las pruebas mediante pytest.
3. **Resultados:** Al finalizar, el pipeline guarda un artefacto (allure-results.zip) que puedes descargar desde la pestaña "Actions" en GitHub para generar tu reporte localmente.

## 📏 Configuración de Calidad (Umbrales)
El proyecto utiliza un motor parametrizado a través del archivo config.json. Aquí se define el comportamiento esperado de la IA:
* **Latencia Máxima (latencia_maxima_ms):** Tiempo límite para que el bot conteste (Ej. 5000ms).
* **Precisión de Dicción (wer_minimo_exigido):** Porcentaje mínimo de exactitud en la transcripción de Whisper (Ej. 80%).
* **Comprensión Semántica (similitud_minima):** Similitud Coseno mínima para considerar que el bot entendió la intención (Ej. 55%).

## 🧠 Características Avanzadas
1. **Inyección de Ruido Dinámico (Data Augmentation):**
   Utiliza la librería Pydub para superponer la voz del usuario con sonidos ambientales (ej. tráfico) ajustando los decibelios en tiempo real antes de enviar el payload a la IA.
2. **Protección contra Prompt Injection por Voz:**
   Detecta si el bot es vulnerable a comandos maliciosos inyectados a través de audio, asegurando que responda aplicando políticas de seguridad en lugar de exponer datos confidenciales.
3. **Evaluación Vectorial Semántica:**
   Evaluación Vectorial Semántica:
   Utiliza modelos HuggingFace (MiniLM) para evaluar si la respuesta de la IA significa lo mismo que la intención esperada, evitando fallas por el uso de sinónimos o variaciones en el fraseo.

## 🐛 Troubleshooting
### ERROR: "ModuleNotFoundError: No module named 'sentence_transformers'"
- **Causa:** Faltan librerías en tu entorno.
- **Solución:** Ejecuta pip install sentence-transformers pydub con tu entorno virtual activado.

### ERROR: "[WinError 2] El sistema no puede encontrar el archivo especificado" / "ffprobe error"
- **Causa:** Pydub y Whisper no encuentran el motor de audio.
- **Solución:** Asegúrate de instalar FFmpeg y agregar su carpeta bin a las variables de entorno de tu sistema operativo.

### ERROR: "Connection Refused"
- **Causa:** La prueba intentó enviar el audio pero el bot estaba apagado.
- **Solución:** Asegúrate de estar corriendo python mock_bot.py en una terminal separada antes de iniciar la auditoría.