/* CHATBOT FUNCTIONALITY */
(function () {
    // 1. Create HTML Elements
    const chatbotHTML = `
        <div class="chatbot-trigger" id="chatbotTrigger">
            💬
        </div>
        <div class="chatbot-container" id="chatbotContainer">
            <div class="chatbot-header">
                <h3>✨ Cosmic Guide</h3>
                <button class="chatbot-close" id="chatbotClose">&times;</button>
            </div>
            <div class="chatbot-messages" id="chatbotMessages">
                <div class="message bot">
                    Namaste! I am your AI Cosmic Guide. How can I help you unlock your destiny today?
                </div>
            </div>
            <div class="chatbot-input-area">
                <input type="text" class="chatbot-input" id="chatbotInput" placeholder="Ask about your destiny...">
                <button class="chatbot-send" id="chatbotSend">
                    <i class="fas fa-paper-plane"></i>
                </button>
            </div>
        </div>
    `;

    document.body.insertAdjacentHTML('beforeend', chatbotHTML);

    const trigger = document.getElementById('chatbotTrigger');
    const container = document.getElementById('chatbotContainer');
    const closeBtn = document.getElementById('chatbotClose');
    const sendBtn = document.getElementById('chatbotSend');
    const input = document.getElementById('chatbotInput');
    const messagesContainer = document.getElementById('chatbotMessages');

    // 2. Toggle Chat
    trigger.addEventListener('click', () => {
        container.classList.add('active');
        trigger.style.display = 'none';
    });

    closeBtn.addEventListener('click', () => {
        container.classList.remove('active');
        trigger.style.display = 'flex';
    });

    // 3. Send Message
    async function sendMessage() {
        const text = input.value.trim();
        if (!text) return;

        // Add user message
        addMessage(text, 'user');
        input.value = '';

        // Check login
        const token = localStorage.getItem('vedic_token');
        if (!token) {
            addMessage('Please sign in to chat with the cosmic guide. 🔒', 'bot');
            return;
        }

        try {
            const res = await fetch(`${window.API_BASE_URL}/api/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({ message: text })
            });

            const data = await res.json();
            if (res.ok) {
                addMessage(data.response, 'bot');
            } else {
                addMessage('The cosmic energies are turbulent right now. Please try again later.', 'bot');
            }
        } catch (err) {
            addMessage('I cannot reach the stars. Is your internet connection active?', 'bot');
        }
    }

    function addMessage(text, sender) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${sender}`;
        msgDiv.innerText = text;
        messagesContainer.appendChild(msgDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    sendBtn.addEventListener('click', sendMessage);
    input.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });

})();
