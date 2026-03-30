import pytest
from pytest_html import extras
import re

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    extras_list = getattr(report, "extras", [])
    
    if report.when == "call":
        # Extraer el escenario del nombre de la prueba 
        match = re.search(r'\[(.*?)\]', item.name)
        escenario = match.group(1) if match else "exito"
        
        audio_user = f"audio_usuario_{escenario}.mp3"
        audio_bot = f"respuesta_bot_{escenario}.mp3"
        
        html_content = f'''
        <div style="margin-top: 15px; padding: 20px; background-color: #f8f9fa; border-radius: 8px; border: 1px solid #dee2e6;">
            <h2 style="color: #333; margin-top: 0;">Evaluación de Escenario: <span style="color:#0056b3;">{escenario.upper()}</span></h2>
            
            <h3 style="margin-top: 15px; color: #555;">🗣️ Audio del Usuario:</h3>
            <audio controls style="width: 100%; margin-bottom: 20px;">
                <source src="{audio_user}" type="audio/mpeg">
            </audio>
            
            <h3 style="margin-top: 0; color: #28a745;">🤖 Audio del Sistema (Respuesta):</h3>
            <audio controls style="width: 100%;">
                <source src="{audio_bot}" type="audio/mpeg">
            </audio>
        </div>
        '''
        extras_list.append(extras.html(html_content))
        report.extras = extras_list