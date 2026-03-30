import os
import shutil
import subprocess

def main():
    print("==================================================")
    print("🚀 INICIANDO AUDITORÍA DE IA (VOICE FRAMEWORK) 🚀")
    print("==================================================\n")

    # 1. Ejecutar Pytest (Limpiando la carpeta temporal de resultados)
    print("🧪 1. Ejecutando pruebas y evaluando métricas...")
    subprocess.run(["pytest", "tests/test_bdd_voz.py", "--clean-alluredir", "--alluredir=allure-results"])

    # 2. Lógica de retención de historial
    report_history = os.path.join("allure-report", "history")
    results_history = os.path.join("allure-results", "history")

    if os.path.exists(report_history):
        print("📦 2. Rescatando historial de tendencias anterior...")
        shutil.copytree(report_history, results_history, dirs_exist_ok=True)
    else:
        print("🆕 2. Primera ejecución: No hay historial previo guardado.")

    # 3. Construir el reporte físico permanente
    print("📊 3. Construyendo el Dashboard gerencial...")
    allure_bat = os.path.join("allure", "bin", "allure.bat")
    subprocess.run([allure_bat, "generate", "allure-results", "--clean", "-o", "allure-report"])

    # 4. Abrir el reporte en el navegador
    print("🌐 4. Abriendo el reporte en tu navegador...")
    subprocess.run([allure_bat, "open", "allure-report"])

if __name__ == "__main__":
    main()