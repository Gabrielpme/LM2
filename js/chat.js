document.addEventListener('DOMContentLoaded', function () {
    const chatToggle = document.getElementById('chat-toggle');
    const chatWindow = document.getElementById('chat-window');
    const chatClose = document.getElementById('chat-close');
    const chatSend = document.getElementById('chat-send');
    const chatInput = document.getElementById('chat-input');
    const chatMessages = document.getElementById('chat-messages');
 
    if (!chatToggle || !chatWindow) {
        console.error('Elementos do chat não encontrados!');
        return;
    }
 
    let conversationHistory = [];
    let isWaiting = false;
 
    chatToggle.onclick = () => chatWindow.classList.toggle('chat-hidden');
    chatClose.onclick = () => chatWindow.classList.add('chat-hidden');
 
    chatSend.onclick = sendMessage;
    chatInput.onkeypress = (e) => { if (e.key === 'Enter') sendMessage(); };
 
    async function sendMessage() {
        const text = chatInput.value.trim();
        if (!text || isWaiting) return;
 
        appendMessage(text, 'user');
        chatInput.value = '';
        isWaiting = true;
 
        conversationHistory.push({ role: 'user', content: text });
 
        const typingEl = showTypingIndicator();
 
        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ messages: conversationHistory })
            });
 
            const data = await response.json();
 
            if (data.reply) {
                conversationHistory.push({ role: 'assistant', content: data.reply });
                typingEl.remove();
                appendMessage(data.reply, 'bot');
            } else {
                throw new Error(data.error || 'Erro desconhecido');
            }
 
        } catch (error) {
            typingEl.remove();
            appendMessage('Desculpe, ocorreu um erro. Por favor, tente novamente ou ligue: (38) 99115-5388.', 'bot');
            console.error('Erro no chat:', error);
        } finally {
            isWaiting = false;
        }
    }
 
    function appendMessage(text, sender) {
        const div = document.createElement('div');
        div.classList.add('message', sender);
        div.innerText = text;
        chatMessages.appendChild(div);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
 
    function showTypingIndicator() {
        const div = document.createElement('div');
        div.classList.add('message', 'bot', 'typing-indicator');
        div.innerHTML = '<span></span><span></span><span></span>';
        chatMessages.appendChild(div);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        return div;
    }
});