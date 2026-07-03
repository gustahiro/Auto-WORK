# AUTOWORK - Assistente Pessoal de Desktop (Jarvis-inspired)

Este projeto é um assistente virtual de desktop que combina um backend em **Python (Flask)** com um frontend visualmente inspirado no **Jarvis de Tony Stark (Homem de Ferro)**, com luzes de néon azuis, círculos concêntricos animados e controle interativo de voz.

---

## 🛠️ Requisitos e Dependências

Para que o assistente funcione perfeitamente, você precisará do Python instalado no seu sistema Windows e das bibliotecas listadas no `requirements.txt`.

### Importante: PyAudio no Windows
O módulo `SpeechRecognition` depende do `PyAudio` para gravar áudio do seu microfone. No Windows, o `PyAudio` pode ser facilmente instalado via pip na maioria das versões do Python (3.7+). Caso encontre alguma instrução de erro de compilação C++, execute:
```bash
pip install pipwin
pipwin install pyaudio
```

---

## 🚀 Como Instalar e Executar

Siga os passos abaixo no seu terminal (PowerShell ou Prompt de Comando):

### 1. Clonar ou Navegar até a Pasta do Projeto
Certifique-se de estar dentro da pasta do projeto:
```bash
cd "c:\Users\SAMSUNG\OneDrive\Área de Trabalho\Programas e jogos\Projeto 1 AUTOWORK"
```

### 2. Instalar as Dependências
Instale todos os pacotes necessários rodando:
```bash
pip install -r requirements.txt
```

### 3. Executar o Servidor Local
Após a instalação bem-sucedida, inicialize o servidor do assistente:
```bash
python app.py
```
Você ouvirá uma voz de boas-vindas sintetizada dizendo: *"Sistema AUTOWORK inicializado. Aguardando comandos."*

### 4. Acessar a Interface Gráfica
Abra o navegador e acesse a URL local:
👉 **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

## 🎤 Comandos Disponíveis (Voz ou Clique)

Você pode clicar no **Reator de Arc no centro da tela** para ativar o microfone e dizer um comando, ou simplesmente clicar em um dos **botões de controle rápido** do painel direito:

* **"Abrir Chrome" / "Abrir Navegador"**: Abre o Google Chrome.
* **"Abrir VS Code" / "Abrir Editor"**: Abre o editor code do VS Code.
* **"Abrir Google"**: Abre a página principal do buscador Google.
* **"Abrir YouTube"**: Abre o site do YouTube.
* **"Horas" / "Que horas são"**: Responde por voz e exibe o horário de Brasília.
* **"Data" / "Que dia é hoje"**: Responde por voz a data completa em português.
* **"Ajuda" / "Comandos"**: Lista os comandos em formato de síntese.

---

## 📂 Visão Geral dos Arquivos

* `app.py`: Backend Flask principal. Lida com chamadas à API, reconhecimento de fala do Google, vocalização por voz de sistema e disparadores de automação.
* `templates/index.html`: Dashboard com estilo Jarvis HUD.
* `static/style.css`: Estilização neon-blue, grids e animações rotacionais.
* `static/script.js`: Gerenciador de eventos, rotinas de requisição fetch e sincronia de animações de estados.
* `static/images/background.png`: Papel de parede tecnológico gerado por Inteligência Artificial para cobertura da HUD.
