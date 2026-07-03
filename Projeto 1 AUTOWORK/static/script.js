/* 
   AUTOWORK JS - Controlador de Interface e Comunicação API
   Autor: Antigravity (Senior Full Stack Developer)
*/

document.addEventListener('DOMContentLoaded', () => {
    // Referências do DOM
    const reactorTrigger = document.getElementById('reactor-trigger');
    const assistantStatus = document.getElementById('assistant-status');
    const speechTranscript = document.getElementById('speech-transcript');
    const speechReply = document.getElementById('speech-reply');
    const logConsole = document.getElementById('log-console');
    const clockDisplay = document.getElementById('hud-clock');
    const statusPulse = document.getElementById('status-pulse');
    const statusText = document.getElementById('status-text');

    // Variável de controle de estado
    let isWorking = false;

    // 1. Atualização do Relógio da HUD
    function updateClock() {
        const now = new Date();
        const hrs = String(now.getHours()).padStart(2, '0');
        const mins = String(now.getMinutes()).padStart(2, '0');
        const secs = String(now.getSeconds()).padStart(2, '0');
        clockDisplay.textContent = `${hrs}:${mins}:${secs}`;
    }
    setInterval(updateClock, 1000);
    updateClock();

    // 2. Auxiliar para Adição de Logs no Console Visual
    function addLog(message, type = 'system') {
        const entry = document.createElement('div');
        entry.className = `log-entry ${type}`;
        
        const now = new Date();
        const timeStr = `[${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}:${String(now.getSeconds()).padStart(2, '0')}]`;
        
        const spanTime = document.createElement('span');
        spanTime.className = 'timestamp';
        spanTime.textContent = timeStr;
        
        const textNode = document.createTextNode(` ${message}`);
        
        entry.appendChild(spanTime);
        entry.appendChild(textNode);
        
        logConsole.appendChild(entry);
        
        // Mantém o scroll sempre no final do console
        logConsole.scrollTop = logConsole.scrollHeight;
    }

    // 3. Gerenciamento de Estilos de Estados Visuais no Reator
    function setAssistantState(state) {
        // Remove classes estaduais anteriores
        reactorTrigger.classList.remove('listening', 'processing', 'speaking');
        
        if (state === 'listening') {
            reactorTrigger.classList.add('listening');
            assistantStatus.textContent = 'OUVINDO COMANDO DE VOZ...';
            statusText.textContent = 'SYSTEM STATUS: CAPTURANDO ÁUDIO';
            statusPulse.style.backgroundColor = '#39ff14';
            statusPulse.style.boxShadow = '0 0 10px #39ff14';
        } else if (state === 'processing') {
            reactorTrigger.classList.add('processing');
            assistantStatus.textContent = 'PROCESSANDO DADOS DE VOZ...';
            statusText.textContent = 'SYSTEM STATUS: COGNITIVO';
            statusPulse.style.backgroundColor = '#ffdf00';
            statusPulse.style.boxShadow = '0 0 10px #ffdf00';
        } else if (state === 'speaking') {
            reactorTrigger.classList.add('speaking');
            assistantStatus.textContent = 'SINTETIZANDO RESPOSTA (VOZ)...';
            statusText.textContent = 'SYSTEM STATUS: COMUNICANDO';
            statusPulse.style.backgroundColor = '#00f3ff';
            statusPulse.style.boxShadow = '0 0 10px #00f3ff';
        } else {
            // Idle / Padrão
            assistantStatus.textContent = 'CLIQUE NO REATOR PARA ENVIAR COMANDO';
            statusText.textContent = 'SYSTEM STATUS: ONLINE';
            statusPulse.style.backgroundColor = '#00f3ff';
            statusPulse.style.boxShadow = '0 0 10px #00f3ff';
        }
    }

    // 4. Fluxo Principal de Escuta de Voz
    async function startVoiceInteraction() {
        if (isWorking) return;
        isWorking = true;
        
        setAssistantState('listening');
        addLog('Iniciando captura do microfone...', 'system');
        
        try {
            // 4.1 Chama API para ouvir o microfone
            const response = await fetch('/api/listen');
            const data = await response.json();
            
            if (data.status === 'success' && data.text) {
                const command = data.text;
                speechTranscript.textContent = `"${command}"`;
                addLog(`Áudio traduzido: "${command}"`, 'user');
                
                // 4.2 Executa o comando e fala o retorno
                await executeCommand(command);
            } else {
                // Trata as falhas de áudio (silêncio / erro etc)
                const msgError = data.message || 'Falha no reconhecimento de voz.';
                addLog(`Aviso de entrada: ${msgError}`, 'error');
                speechTranscript.textContent = '"Nenhum comando reconhecido"';
                speechReply.textContent = `[Erro]: ${msgError}`;
                setAssistantState('idle');
                isWorking = false;
            }
        } catch (err) {
            console.error(err);
            addLog(`Falha geral na requisição: ${err.message}`, 'error');
            setAssistantState('idle');
            isWorking = false;
        }
    }

    // 5. Envia o texto reconhecido ou clicado para processamento e fala no backend
    async function executeCommand(commandText) {
        setAssistantState('processing');
        addLog(`Buscando ações para: "${commandText}"`, 'system');
        
        try {
            // Cria um atraso visual rápido para dar sensação de "pensamento" da IA
            await new Promise(resolve => setTimeout(resolve, 600));
            setAssistantState('speaking');

            const response = await fetch('/api/execute', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ text: commandText })
            });
            
            const data = await response.json();
            
            if (data.status === 'success') {
                speechReply.textContent = `"${data.reply}"`;
                addLog(`Resposta do AUTOWORK: "${data.reply}"`, 'assistant');
                if (data.executed) {
                    addLog('Automação de sistema executada com sucesso.', 'system');
                } else {
                    addLog('Comando processado, mas nenhuma automação foi disparada.', 'system');
                }
            } else {
                addLog('Erro ao executar processador de comandos.', 'error');
            }
        } catch (err) {
            console.error(err);
            addLog(`Erro ao realizar requisição de execução: ${err.message}`, 'error');
        } finally {
            // Volta ao estado inicial
            setAssistantState('idle');
            isWorking = false;
        }
    }

    // Listener do clique no reator central
    reactorTrigger.addEventListener('click', () => {
        startVoiceInteraction();
    });

    // Expondo a função para ser usada globalmente pelos botões de atalho rápido
    window.executeQuickCommand = function(text) {
        if (isWorking) return;
        isWorking = true;
        
        speechTranscript.textContent = `"${text}" [Painel Dinâmico]`;
        addLog(`Comando via atalho: "${text}"`, 'user');
        
        executeCommand(text);
    };
});
