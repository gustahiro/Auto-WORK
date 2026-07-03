# -*- coding: utf-8 -*-
"""
AUTOWORK - Assistente Pessoal de Desktop
Backend em Flask com Speech Recognition (STT) e Pyttsx3 (TTS)
Autor: Antigravity (Senior Full Stack Developer)
"""

import os
import sys
import time
import datetime
import subprocess
import webbrowser
import unicodedata
from flask import Flask, render_template, jsonify, request
import speech_recognition as sr

# Inicializa o Flask
app = Flask(__name__, template_folder='templates', static_folder='static')

# Configuração de trava para evitar falas concorrentes
import threading
speak_lock = threading.Lock()

def speak(text):
    """
    Função para sintetizar voz usando pyttsx3 de forma síncrona.
    Bloqueia até que a fala termine para manter sincronia com a interface.
    """
    def run_speech():
        with speak_lock:
            try:
                import pyttsx3
                # Inicializa o motor de voz localmente na thread
                engine = pyttsx3.init()
                engine.setProperty('rate', 175)  # Velocidade natural
                engine.setProperty('volume', 1.0)
                
                # Configura voz em Português do Brasil (pt-BR)
                voices = engine.getProperty('voices')
                for voice in voices:
                    if 'pt-br' in voice.id.lower() or 'portuguese' in voice.name.lower() or 'brazil' in voice.name.lower():
                        engine.setProperty('voice', voice.id)
                        break
                        
                engine.say(text)
                engine.runAndWait()
            except Exception as e:
                print(f"[Aviso] Falha no TTS: {e}")
                
    # Executa a fala. Pode ser síncrono para reter a requisição Flask durante a fala.
    # Isso ajuda o front-end a exibir o estado de "Falando" em perfeita sincronia.
    run_speech()

def normalize_text(text):
    """
    Remove acentos e caracteres especiais, converte para minúsculas.
    Garante maior precisão no reconhecimento dos comandos.
    """
    if not text:
        return ""
    text = text.lower().strip()
    # Remove acentos
    text = "".join(c for c in unicodedata.normalize('NFD', text)
                     if unicodedata.category(c) != 'Mn')
    return text

def open_chrome():
    """ Tenta encontrar e abrir o Google Chrome no Windows. """
    paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        os.path.expandvars(r"%LocalAppData%\Google\Chrome\Application\chrome.exe")
    ]
    for path in paths:
        if os.path.exists(path):
            subprocess.Popen([path])
            return True
    # Fallback usando webbrowser padrão
    webbrowser.open("about:blank")
    return True

def open_vscode():
    """ Tenta abrir o VS Code no Windows buscando nos locais mais comuns. """
    try:
        # Tenta invocar diretamente do PATH
        subprocess.Popen(["code"], shell=True)
        return True
    except Exception:
        # Busca no Local AppData
        local_app_data = os.environ.get("LOCALAPPDATA", "")
        path_local = os.path.join(local_app_data, "Programs", "Microsoft VS Code", "Code.exe")
        if os.path.exists(path_local):
            subprocess.Popen([path_local])
            return True
            
        # Busca Program Files
        prog_files = os.environ.get("ProgramFiles", "C:\\Program Files")
        path_prog = os.path.join(prog_files, "Microsoft VS Code", "Code.exe")
        if os.path.exists(path_prog):
            subprocess.Popen([path_prog])
            return True
    return False

def parse_and_execute(command_text):
    """
    Processa o texto reconhecido e executa a devida automação de sistema.
    Retorna a frase de resposta e um status de execução.
    """
    cmd = normalize_text(command_text)
    reply = ""
    executed = False
    
    if not cmd:
        return "Não entendi o comando. Poderia repetir?", False
        
    print(f"[Comando Normalizado]: {cmd}")
    
    if "abrir chrome" in cmd or "abrir navegador" in cmd:
        open_chrome()
        reply = "Abrindo o navegador Google Chrome."
        executed = True
    elif "abrir vs code" in cmd or "abrir codigo" in cmd or "abrir editor" in cmd:
        if open_vscode():
            reply = "Abrindo o Visual Studio Code. Bom trabalho."
        else:
            reply = "VS Code não encontrado nas pastas padrão, mas tentei iniciar."
        executed = True
    elif "abrir google" in cmd:
        webbrowser.open("https://www.google.com")
        reply = "Abrindo a página de buscas do Google."
        executed = True
    elif "abrir youtube" in cmd:
        webbrowser.open("https://www.youtube.com")
        reply = "Redirecionando para o YouTube."
        executed = True
    elif "horas" in cmd or "que horas sao" in cmd:
        now = datetime.datetime.now()
        reply = f"Atualmente são {now.hour} horas e {now.minute} minutos."
        executed = True
    elif "data" in cmd or "que dia e hoje" in cmd or "dia de hoje" in cmd:
        now = datetime.datetime.now()
        meses = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", 
                 "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
        reply = f"Hoje é dia {now.day} de {meses[now.month-1]} de {now.year}."
        executed = True
    elif "ajuda" in cmd or "comandos" in cmd:
        reply = "Você pode dizer: abrir Chrome, abrir VS Code, abrir Google, abrir YouTube, horas, ou data."
        executed = True
    else:
        # Se não reconhecer automático, tenta apenas avisar que foi recebido mas não mapeado
        reply = f"Comando '{command_text}' recebido, mas não há nenhuma ação configurada."
        executed = False
        
    return reply, executed

@app.route('/')
def index():
    """ Rota principal que carrega a página HTML da interface Jarvis. """
    return render_template('index.html')

@app.route('/api/listen', methods=['GET'])
def listen_route():
    """
    Endpoint que ativa o microfone do servidor usando SpeechRecognition.
    Aguarda e retorna o texto reconhecido em formato JSON.
    """
    r = sr.Recognizer()
    # Reduzir ruído de silêncio
    r.dynamic_energy_threshold = True
    
    try:
        with sr.Microphone() as source:
            print("[MICROFONE] Ajustando áudio para ruído de fundo...")
            r.adjust_for_ambient_noise(source, duration=0.8)
            print("[MICROFONE] Ouvindo comando...")
            # Limites de escuta rápida
            audio = r.listen(source, timeout=4, phrase_time_limit=4)
            
        print("[MICROFONE] Processando áudio pelo Google STT...")
        recognized_text = r.recognize_google(audio, language='pt-BR')
        print(f"[MICROFONE] Reconhecido: {recognized_text}")
        
        return jsonify({
            "status": "success",
            "text": recognized_text
        })
        
    except sr.WaitTimeoutError:
        print("[MICROFONE] Limite de tempo excedido aguardando áudio.")
        return jsonify({
            "status": "timeout",
            "text": "",
            "message": "Ninguém falou no tempo limite."
        })
    except sr.UnknownValueError:
        print("[MICROFONE] Não foi possível compreender o áudio.")
        return jsonify({
            "status": "error",
            "text": "",
            "message": "Não entendi nada do áudio."
        })
    except Exception as e:
        print(f"[MICROFONE] Erro inesperado: {e}")
        return jsonify({
            "status": "error",
            "text": "",
            "message": f"Erro de hardware ou configuração: {str(e)}"
        })

@app.route('/api/execute', methods=['POST'])
def execute_route():
    """
    Endpoint que recebe o texto traduzido, executa a ação correspondente
    no sistema operacional e inicializa a resposta de voz pelo pyttsx3.
    """
    data = request.get_json() or {}
    command_text = data.get("text", "")
    
    # 1. Processa lógica e executa comandos (como abrir sites ou programas)
    reply, executed = parse_and_execute(command_text)
    
    # 2. Executa a fala de retorno pelo console/TTS (bloqueante)
    speak(reply)
    
    return jsonify({
        "status": "success",
        "reply": reply,
        "executed": executed
    })

if __name__ == '__main__':
    print("Iniciando AUTOWORK Desktop Assistant...")
    
    # Boas-vindas falada ao iniciar o assistente e abrir navegador
    def on_startup():
        time.sleep(1.5)
        # Abre automaticamente a interface no navegador padrao
        webbrowser.open('http://127.0.0.1:5000')
        speak("Sistema AUTOWORK inicializado. A interface web foi aberta no seu navegador. Aguardando comandos.")

    threading.Thread(target=on_startup).start()
    
    # Executa o servidor na porta local padrão
    app.run(host='127.0.0.1', port=5000, debug=True, use_reloader=False)
