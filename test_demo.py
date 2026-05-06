import pytest
import requests
import time
import whisper
import warnings
from gtts import gTTS
import jiwer
from sentence_transformers import SentenceTransformer, util

warnings.filterwarnings("ignore")

print("Cargando modelos de IA, por favor espera...")
model_whisper = whisper.load_model("base")
model_similitud = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

# 📊 MATRIZ DE CASOS DE PRUEBA
escenarios_prueba = [
    (
        "exito", 
        "Hola, quiero transferir 500 pesos y también hacer una consulta de saldo.", 
        "hola tu transferencia fue exitosa y tu saldo restante es de 500 pesos", 
        "confirmar transferencia exitosa y reportar saldo"
    ),
    (
        "fuera_alcance", 
        "Quiero pedir una pizza de pepperoni con extra queso a mi dirección.", 
        "lo siento soy el asistente virtual financiero solo puedo ayudarte con informacion financiera y transferencias", 
        "rechazar solicitud por estar fuera de contexto financiero"
    ),
    (
        "incoherente", 
        "abracadabra pata de cabra hocus pocus", 
        "disculpa no logre entenderte podrias repetir tu solicitud mas claramente", 
        "pedir al usuario que repita debido a falta de entendimiento fallback"
    )
]

@pytest.mark.parametrize("escenario, frase_usuario, texto_esperado_bot, intencion_esperada", escenarios_prueba)
def test_matriz_intenciones_orbit(escenario, frase_usuario, texto_esperado_bot, intencion_esperada):
    """Auditoría de Matriz Calidad: Exitosos, Fuera de Alcance e Incoherentes"""
    url = "http://localhost:5000/chat"
    
    audio_user_path = f"audio_usuario_{escenario}.mp3"
    audio_bot_path = f"respuesta_bot_{escenario}.mp3"
    
    # --- 1. SIMULAR USUARIO ---
    tts_user = gTTS(text=frase_usuario, lang='es')
    tts_user.save(audio_user_path) 
    
    # --- 2. MÉTRICA: LATENCIA DE RESPUESTA ---
    inicio = time.time()
    with open(audio_user_path, "rb") as f:
        # Enviamos el audio y una etiqueta para que el mock sepa cómo reaccionar
        response = requests.post(url, files={'audio': f}, data={'escenario': escenario}) 
    fin = time.time()
    
    latencia = round((fin - inicio) * 1000, 2)
    assert latencia < 5000, f"FAIL: Latencia de respuesta crítica ({latencia} ms)"

    # --- 3. MÉTRICA: WER/CER (Dicción) ---
    with open(audio_bot_path, "wb") as f:
        f.write(response.content)
    
    texto_transcrito = model_whisper.transcribe(audio_bot_path)["text"].lower().strip()
    texto_limpio = texto_transcrito.replace(".", "").replace(",", "").replace("¿", "").replace("?", "")
    
    tasa_error = jiwer.wer(texto_esperado_bot, texto_limpio)
    precision = (1 - tasa_error) * 100
    assert precision > 80, f"FAIL: WER/CER inaceptable ({precision}%)"

    # --- 4. MÉTRICA: TASA DE ÉXITO DE INTENTOS ---
    embeddings_esperado = model_similitud.encode(intencion_esperada)
    embeddings_real = model_similitud.encode(texto_transcrito)
    
    similitud = util.cos_sim(embeddings_esperado, embeddings_real).item() * 100
    assert similitud > 30, f"FAIL: Tasa de éxito de intentos baja ({similitud}%)"