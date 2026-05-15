import os
import json
import pytest
import requests
import time
import whisper
import jiwer
import warnings
import allure
from allure_commons.types import Severity
from pytest_bdd import scenario, given, when, then, parsers
from sentence_transformers import SentenceTransformer, util
from pydub import AudioSegment # 🚀 NUEVO IMPORT PARA MEZCLAR AUDIO

warnings.filterwarnings("ignore")

# 1. CARGA INICIAL
print("⏳ Cargando configuración y modelos de IA...")
with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

model_whisper = whisper.load_model("base")
model_similitud = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

# 2. VINCULAR EL ARCHIVO GHERKIN EXPLICITAMENTE
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FEATURE_FILE = os.path.join(BASE_DIR, 'features', 'evaluacion_voz.feature')

# --- 🚀 ESCENARIO 1: EVALUACIÓN CON RUIDO ---
@allure.epic("Core Bancario Voice")
@allure.feature("Auditoría de IA Financiera")
@allure.story("Transacciones seguras con ruido de fondo pregrabado")
@allure.severity(Severity.CRITICAL)
@scenario(FEATURE_FILE, 'La IA procesa audios con diferentes dificultades')
def test_evaluacion_voz_con_ruido():
    pass

# --- 🛡️ ESCENARIO 2: CIBERSEGURIDAD (PROMPT INJECTION) ---
@allure.epic("Core Bancario Voice")
@allure.feature("Ciberseguridad de IA")
@allure.story("Prevención de Prompt Injection por Voz")
@allure.severity(Severity.BLOCKER)
@scenario(FEATURE_FILE, 'La IA bloquea intentos de inyección de comandos por voz (Prompt Injection)')
def test_seguridad_prompt_injection():
    pass

# --- 🌪️ ESCENARIO 3: INYECCIÓN DE RUIDO DINÁMICO ---
@allure.epic("Core Bancario Voice")
@allure.feature("Data Augmentation y Resiliencia")
@allure.story("Inyección de ruido de fondo en tiempo real")
@allure.severity(Severity.NORMAL)
@scenario(FEATURE_FILE, 'La IA procesa audios con inyección de ruido dinámico')
def test_ruido_dinamico():
    pass

# 3. FIXTURE DE CONTEXTO
@pytest.fixture
def context():
    return {}

# --- PASOS GIVEN ---
@given('que el framework está configurado para apuntar al "Bot Financiero Generico"')
def configurar_entorno(context):
    context['url'] = config['target_ai']['endpoint_url']
    context['umbrales'] = config['umbrales_calidad']
    os.makedirs(config['rutas']['dataset_audios'], exist_ok=True)
    os.makedirs(config['rutas']['evidencia_salida'], exist_ok=True)
    context['rutas'] = config['rutas']
    
    os.makedirs("allure-results", exist_ok=True)
    env_path = os.path.join("allure-results", "environment.properties")
    with open(env_path, "w", encoding="utf-8") as f:
        f.write(f"Target_Bot={context['url']}\n")
        f.write(f"Latencia_Maxima={context['umbrales']['latencia_maxima_ms']}ms\n")
        f.write(f"Precision_Minima_WER={context['umbrales']['wer_minimo_exigido']}%\n")
        f.write(f"Similitud_Minima={context['umbrales']['similitud_minima']}%\n")
        f.write("Framework=Pytest-BDD + Whisper + MiniLM\n")
        
    cat_path = os.path.join("allure-results", "categories.json")
    categorias = [
        {"name": "⏱️ Defecto: IA Demasiado Lenta", "matchedStatuses": ["failed"], "messageRegex": ".*IA demasiado lenta.*"},
        {"name": "🗣️ Defecto: Mala Dicción (WER)", "matchedStatuses": ["failed"], "messageRegex": ".*Dicción inaceptable.*"},
        {"name": "🧠 Defecto: Alucinación Semántica", "matchedStatuses": ["failed"], "messageRegex": ".*no cumplió la intención.*"}
    ]
    with open(cat_path, "w", encoding="utf-8") as f:
        json.dump(categorias, f, indent=4, ensure_ascii=False)

@given(parsers.parse('selecciono el archivo de audio "{archivo_audio}" del dataset'))
def cargar_audio_real(context, archivo_audio):
    ruta_audio = os.path.join(context['rutas']['dataset_audios'], archivo_audio)
    assert os.path.exists(ruta_audio), f"❌ Falla: No se encontró el audio de prueba en {ruta_audio}"
    context['ruta_audio_usuario'] = ruta_audio
    allure.attach.file(ruta_audio, name="1. Audio Original del Usuario", attachment_type="audio/mpeg", extension="mp3")

# MEZCLADORA DE AUDIO
@given(parsers.parse('le inyecto ruido de fondo "{archivo_ruido}" a "{db_diferencia}" decibelios'))
def inyectar_ruido_dinamico(context, archivo_ruido, db_diferencia):
    ruta_limpio = context['ruta_audio_usuario']
    ruta_ruido = os.path.join(context['rutas']['dataset_audios'], archivo_ruido)
    
    assert os.path.exists(ruta_ruido), f"❌ Falla: No se encontró la pista de ruido en {ruta_ruido}"
    
    with allure.step(f"🎛️ Mezclando audios: Inyectando ruido a {db_diferencia} dB"):
        # 1. Cargar las dos pistas
        audio_base = AudioSegment.from_file(ruta_limpio)
        ruido = AudioSegment.from_file(ruta_ruido)
        
        # 2. Ajustar el volumen del ruido
        ruido = ruido + int(db_diferencia)
        
        # 3. Igualar duraciones 
        if len(ruido) < len(audio_base):
            ruido = ruido * (len(audio_base) // len(ruido) + 1)
        ruido = ruido[:len(audio_base)] 
        
        # 4. Superponer (Overlay) las dos pistas
        audio_mezclado = audio_base.overlay(ruido)
        
        # 5. Guardar la nueva pista generada temporalmente
        nueva_ruta = os.path.join(context['rutas']['evidencia_salida'], "audio_mezclado_temp.mp3")
        audio_mezclado.export(nueva_ruta, format="mp3")
        
        # 6. Decirle que el archivo a enviar ahora es el mezclado
        context['ruta_audio_usuario'] = nueva_ruta
        
        # Adjuntar al reporte para poder escucharlo
        allure.attach.file(nueva_ruta, name=f"🎧 Audio Dinámico Generado (Ruido {db_diferencia}dB)", attachment_type="audio/mpeg", extension="mp3")

# --- PASOS WHEN ---
@when('envío el flujo de voz a la IA objetivo')
def enviar_peticion_ia(context):
    with allure.step("1. Iniciar cronómetro y enviar POST request"):
        inicio = time.time()
        with open(context['ruta_audio_usuario'], "rb") as f:
            response = requests.post(context['url'], files={'audio': f})
        fin = time.time()
        context['latencia_ms'] = round((fin - inicio) * 1000, 2)
        
    with allure.step("2. Guardar respuesta de audio localmente"):
        ruta_respuesta = os.path.join(context['rutas']['evidencia_salida'], "respuesta_ia.mp3")
        with open(ruta_respuesta, "wb") as f:
            f.write(response.content)
        context['ruta_respuesta_ia'] = ruta_respuesta
        allure.attach.file(ruta_respuesta, name="2. Respuesta de Audio del Bot", attachment_type="audio/mpeg", extension="mp3")

# --- PASOS THEN ---
@then('la latencia de respuesta debe cumplir con el umbral configurado')
def validar_latencia(context):
    limite = context['umbrales']['latencia_maxima_ms']
    latencia_real = context['latencia_ms']
    
    allure.dynamic.parameter("⏱️ Latencia Final", f"{latencia_real} ms")
    
    tabla_md = f"""| Métrica | Valor Obtenido | Límite Permitido | Estado |
| :--- | :---: | :---: | :---: |
| **Latencia** | {latencia_real} ms | {limite} ms | {'✅' if latencia_real <= limite else '❌'} |"""
    allure.attach(tabla_md, name="Métricas de Latencia (Tabla)", attachment_type="text/markdown", extension="md")    
    assert latencia_real <= limite, f"FAIL: IA demasiado lenta ({latencia_real} ms)"

@then(parsers.parse('la precisión de dicción de la respuesta debe evaluarse contra "{texto_esperado}"'))
def validar_wer(context, texto_esperado):
    with allure.step("1. Transcribir audio de la IA usando Whisper local"):
        texto_transcrito = model_whisper.transcribe(context['ruta_respuesta_ia'])["text"].lower().strip()
        texto_limpio = texto_transcrito.replace(".", "").replace(",", "")
        context['texto_transcrito'] = texto_limpio
    
    with allure.step("2. Calcular Word Error Rate (WER)"):
        tasa_error = jiwer.wer(texto_esperado.lower(), texto_limpio)
        precision = (1 - tasa_error) * 100
        limite_wer = context['umbrales']['wer_minimo_exigido']
        
    allure.dynamic.parameter("🗣️ Precisión WER", f"{precision:.2f}%")
    
    tabla_md = f"""### Comparativa de Transcripción
| Origen | Texto |
| :--- | :--- |
| **Esperado (Gherkin)** | {texto_esperado.lower()} |
| **Real (Whisper)** | {texto_limpio} |

### Resultados
| Precisión WER | Umbral Mínimo | Estado |
| :---: | :---: | :---: |
| **{precision:.2f}%** | {limite_wer}% | {'✅' if precision >= limite_wer else '❌'} |"""
    allure.attach(tabla_md, name="Auditoría de Dicción (WER)", attachment_type="text/markdown", extension="md")
    assert precision >= limite_wer, f"FAIL: Dicción inaceptable ({precision}%)"

@then(parsers.parse('la intención semántica detectada debe coincidir con "{intencion_esperada}"'))
def validar_intencion_semantica(context, intencion_esperada):
    if 'texto_transcrito' not in context:
        with allure.step("🔍 Transcribir audio de la IA usando Whisper (Automático)"):
            texto = model_whisper.transcribe(context['ruta_respuesta_ia'])["text"].lower().strip()
            context['texto_transcrito'] = texto.replace(".", "").replace(",", "")
            
    texto_ia = context['texto_transcrito']
    
    with allure.step(f"1. Vectorizar intención esperada: '{intencion_esperada}'"):
        embeddings_esperado = model_similitud.encode(intencion_esperada)
        
    with allure.step("2. Vectorizar transcripción real de la IA"):
        embeddings_real = model_similitud.encode(texto_ia)
    
    with allure.step("3. Calcular Distancia Coseno (Similitud)"):
        similitud = util.cos_sim(embeddings_esperado, embeddings_real).item() * 100
        limite_similitud = context['umbrales']['similitud_minima']
        
    allure.dynamic.parameter("🧠 Similitud Semántica", f"{similitud:.2f}%")
    
    tabla_md = f"""| Métrica | Nivel Obtenido | Nivel Exigido | Estado |
| :--- | :---: | :---: | :---: |
| **Similitud Semántica** | {similitud:.2f}% | {limite_similitud}% | {'✅' if similitud >= limite_similitud else '❌'} |"""
    allure.attach(tabla_md, name="Auditoría de Similitud Semántica", attachment_type="text/markdown", extension="md")
    assert similitud >= limite_similitud, f"FAIL: La IA no cumplió la intención de negocio ({similitud}%)"