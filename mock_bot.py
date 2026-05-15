from flask import Flask, send_file, request
from flask_wtf.csrf import CSRFProtect
from gtts import gTTS
import time
import os

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', os.urandom(24)) # NOSONAR
csrf = CSRFProtect(app)

@app.route('/chat', methods=['POST'])
@csrf.exempt # NOSONAR Declaramos explícitamente que es una API sin estado (stateless) para Pytest
def chat():
    # 1. Obtenemos el archivo de audio enviado por Pytest
    audio_file = request.files.get('audio')
    nombre_archivo = audio_file.filename.lower() if audio_file else ""
    
    # 2. Por defecto es éxito, a menos que el nombre del archivo diga lo contrario
    escenario = request.form.get('escenario', 'exito')
    
    # 🛡️ LÓGICA DE SEGURIDAD: Detectamos si es un intento de hackeo
    if "ataque" in nombre_archivo:
        print(f"\n🚨 [BOT] ¡ALERTA! Intento de Prompt Injection detectado en el archivo: {nombre_archivo}")
        escenario = 'ataque'
    else:
        print(f"\n📞 [BOT] Audio recibido: {nombre_archivo}. Ejecutando flujo normal.")

    # Simulamos el tiempo de procesamiento
    time.sleep(0.3) 
    time.sleep(0.4) 
    time.sleep(0.4) 
    
    # 3. El bot decide qué contestar según la intención 
    if escenario == 'exito':
        respuesta_texto = "Hola. Tu transferencia fue exitosa y tu saldo restante es de 500 pesos."
    elif escenario == 'fuera_alcance':
        respuesta_texto = "Lo siento, soy el asistente virtual financiero. Solo puedo ayudarte con información financiera y transferencias."
    elif escenario == 'ataque':
         respuesta_texto = "Debo rechazar esta solicitud por politicas de seguridad."
    else: 
        respuesta_texto = "Disculpa, no logré entenderte. Podrías repetir tu solicitud más claramente."

    # 4. Generamos el audio en tiempo real con gTTS
    tts = gTTS(text=respuesta_texto, lang='es')
    audio_path = f"respuesta_temp_{escenario}.mp3"
    tts.save(audio_path)
    
    return send_file(audio_path, mimetype="audio/mpeg")

if __name__ == '__main__':
    print("🤖 Servidor Mock Bot Multiescenario escuchando en el puerto 5000...")
    app.run(port=5000)