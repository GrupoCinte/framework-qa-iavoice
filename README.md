# 🎙️ Auditoría de IA - Voice-QA Enterprise Suite

Este framework representa una solución avanzada de QA Automation diseñada específicamente para la validación integral de asistentes virtuales de voz (Voicebots). A diferencia de las pruebas de software tradicionales, este sistema emplea una metodología de Evaluación Triádica que permite auditar no solo la respuesta del bot, sino también su capacidad de comprensión y la calidad acústica de su salida en entornos de estrés.
## 🏗️ Arquitectura del Sistema

El framework opera aislando el Sistema Bajo Prueba (SUT) e interactuando con múltiples motores de IA para generar un veredicto integral.

### 1. Diagrama de Contexto
El siguiente diagrama ilustra el ecosistema completo donde opera el framework. El Analista de QA interactúa como el orquestador que prepara los datasets y niveles de ruido, mientras que el Framework (Voice-QA) actúa como el núcleo que consume servicios de IA externos (Whisper, Llama 3, SpeechMOS) para entregar un tablero de resultados detallado al Cliente final.
   
![Diagrama de Contexto](docs/Diagrama%20de%20Contexto.drawio.jpg)

### 2. Arquitectura de Componentes (C4)
Internamente, el sistema se divide en módulos especializados. El Procesador de Audio se encarga del data augmentation (overlay de ruido), mientras que el Cliente HTTP gestiona la comunicación con el Sistema Bajo Prueba (SUT). El componente crítico es la Calculadora de Score Triádico, que consolida las métricas de los tres ejes de evaluación para generar una calificación única de precisión.
![Diagrama de Componentes C4](docs/Diagrama%20de%20componentesC4.drawio.jpg)

### 3. Flujo de Trabajo (Pipeline QA)
El proceso comienza con la preparación del dataset. Mediante scripts de automatización, se toman audios limpios y se les inyecta ruido de fondo (estrés) para simular entornos reales. Estos audios "estresados" son los que finalmente se envían al Bot para evaluar su resiliencia.
![Diagrama de Flujo](docs/Diagrama%20de%20Flujo.drawio.jpg)

## ⚡ La Evaluación Triádica: El Corazón del Framework
El diferencial de este framework es su capacidad de evaluar la respuesta de la IA desde tres perspectivas simultáneas y asíncronas, como se observa en el diagrama de secuencia a continuación:
1. Eje de Consistencia (STT): Utiliza OpenAI Whisper para transcribir la respuesta de audio del bot. Mediante el algoritmo JIWER, se calcula el Word Error Rate (WER), determinando si el bot tiene una "dicción" clara y si las palabras emitidas coinciden con el guion esperado.
2. Eje Cognitivo (LLM Judge): La transcripción se envía a Llama 3 (vía Groq API). Este motor actúa como un juez inteligente que evalúa si, más allá de las palabras exactas, la intención semántica de la respuesta cumple con los objetivos de negocio y seguridad.
3. Eje Acústico (MOS): Se emplea SpeechMOS para analizar las propiedades físicas del audio generado por el bot, otorgando un puntaje de naturalidad (Mean Opinion Score). Esto asegura que el bot no suene excesivamente robótico o con artefactos de audio molestos.
![Secuencia de Ejecución](docs/Diagrama%20de%20Secuencia%203.drawio.jpg)
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