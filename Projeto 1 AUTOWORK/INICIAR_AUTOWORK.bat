@echo off
echo ===================================================
echo Inicializando AUTOWORK - Assistente Pessoal Jarvis
echo ===================================================
echo.
echo Verificando e instalando dependencias (isso pode demorar um pouco na primeira vez)...
pip install -r requirements.txt
echo.
echo Dependencias verificadas! Iniciando o servidor...
python app.py
pause
