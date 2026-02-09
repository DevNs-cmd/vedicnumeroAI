/**
 * Numerology Chatbot - Native Integration
 * 
 * CLEAN INTEGRATION:
 * 1. Injects Chat UI (Hidden by default).
 * 2. Attaches open listeners to any element with class 'numerology-chat-trigger'.
 * 3. Creates a fallback floating button if no triggers are found.
 * 4. Handles API communication with robust error handling and timeouts.
 */

(function () {
    'use strict';

    // --- CONFIGURATION ---
    const API_URL = 'http://localhost:5001/api/chat';
    const CHAT_TITLE = 'Numerology AI Guide';
    const WELCOME_MSG = 'Namaste! I am your Vedic Numerology Guide. Ask me anything about your numbers or destiny.';
    const TIMEOUT_MS = 15000;

    console.log("Numerology Chatbot: Initializing native integration...");

    // --- STYLES ---
    const css = `
        /* Main Chat Container */
        #nc-widget-container {
            font-family: 'Segoe UI', sans-serif;
            z-index: 999999;
        }

        /* Chat Window */
        #nc-window {
            position: fixed;
            bottom: 90px;
            right: 20px;
            width: 360px;
            height: 520px;
            background: white;
            border-radius: 16px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.15);
            display: none;
            flex-direction: column;
            overflow: hidden;
            border: 1px solid #e0e0e0;
            animation: nc-slide-up 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        }

        @keyframes nc-slide-up {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* Header */
        .nc-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 16px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-weight: 600;
            font-size: 16px;
        }
        .nc-close-btn {
            background: none;
            border: none;
            color: white;
            font-size: 24px;
            cursor: pointer;
            line-height: 1;
            padding: 0 4px;
        }

        /* Messages Area */
        .nc-messages {
            flex: 1;
            padding: 16px;
            overflow-y: auto;
            background-color: #f8f9fa;
            display: flex;
            flex-direction: column;
            gap: 12px;
        }

        .nc-msg {
            max-width: 80%;
            padding: 12px 16px;
            border-radius: 16px;
            font-size: 14px;
            line-height: 1.5;
            word-wrap: break-word;
        }

        .nc-msg.ai {
            background-color: white;
            color: #1a1a1a;
            border-bottom-left-radius: 4px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            align-self: flex-start;
        }

        .nc-msg.user {
            background-color: #764ba2;
            color: white;
            border-bottom-right-radius: 4px;
            box-shadow: 0 2px 8px rgba(118, 75, 162, 0.2);
            align-self: flex-end;
        }

        /* Input Area */
        .nc-input-area {
            padding: 16px;
            border-top: 1px solid #eee;
            background: white;
            display: flex;
            gap: 10px;
        }

        .nc-input {
            flex: 1;
            padding: 10px 14px;
            border: 1px solid #ddd;
            border-radius: 24px;
            outline: none;
            font-size: 14px;
            transition: border-color 0.2s;
        }
        .nc-input:focus {
            border-color: #764ba2;
        }

        .nc-send-btn {
            background: #764ba2;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 20px;
            cursor: pointer;
            font-weight: 600;
            transition: opacity 0.2s;
        }
        .nc-send-btn:hover {
            opacity: 0.9;
        }

        /* Default Floating Button (Fallback) */
        #nc-fab {
            position: fixed;
            bottom: 20px;
            right: 20px;
            width: 60px;
            height: 60px;
            border-radius: 50%;
            background-color: #25d366; /* Match WhatsApp Green for familiarity, or use brand color */
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: transform 0.2s;
            z-index: 999998;
            color: white;
            font-size: 30px;
            border: none;
        }
        #nc-fab:hover {
            transform: scale(1.05);
        }

        .nc-hidden { display: none !important; }
        .nc-loading { color: #666; font-size: 12px; font-style: italic; margin-left: 8px; display: none; }
    `;

    // --- DOM GENERATION ---
    function injectStyles() {
        const styleSheet = document.createElement('style');
        styleSheet.textContent = css;
        document.head.appendChild(styleSheet);
    }

    function createChatInterface() {
        const container = document.createElement('div');
        container.id = 'nc-widget-container';

        // Chat Window
        const windowHtml = `
            <div id="nc-window">
                <div class="nc-header">
                    <span>${CHAT_TITLE}</span>
                    <button class="nc-close-btn">&times;</button>
                </div>
                <div class="nc-messages" id="nc-messages">
                    <div class="nc-msg ai">${WELCOME_MSG}</div>
                    <div class="nc-loading" id="nc-loading">Typing...</div>
                </div>
                <div class="nc-input-area">
                    <input type="text" class="nc-input" id="nc-input" placeholder="Type a message..." />
                    <button class="nc-send-btn" id="nc-send-btn">Send</button>
                </div>
            </div>
        `;

        // Render
        container.innerHTML = windowHtml;
        document.body.appendChild(container);

        // Bind Elements
        const ui = {
            window: document.getElementById('nc-window'),
            messages: document.getElementById('nc-messages'),
            input: document.getElementById('nc-input'),
            sendBtn: document.getElementById('nc-send-btn'),
            closeBtn: container.querySelector('.nc-close-btn'),
            loading: document.getElementById('nc-loading')
        };

        return ui;
    }

    function createFloatingButton() {
        const btn = document.createElement('button');
        btn.id = 'nc-fab';
        btn.innerHTML = '💬';
        btn.onclick = () => toggleChat(true);
        document.body.appendChild(btn);
        return btn;
    }

    // --- LOGIC ---
    let ui;
    let isOpen = false;

    function toggleChat(state) {
        isOpen = state !== undefined ? state : !isOpen;
        if (ui.window) {
            ui.window.style.display = isOpen ? 'flex' : 'none';
            if (isOpen) {
                ui.input.focus();
                scrollToBottom();
            }
        }
    }

    function scrollToBottom() {
        if (ui.messages) ui.messages.scrollTop = ui.messages.scrollHeight;
    }

    function addMessage(text, type) {
        const div = document.createElement('div');
        div.className = `nc-msg ${type}`;
        div.textContent = text;
        ui.messages.insertBefore(div, ui.loading);
        scrollToBottom();
    }

    async function handleSend() {
        const text = ui.input.value.trim();
        if (!text) return;

        // UI Updates
        addMessage(text, 'user');
        ui.input.value = '';
        ui.loading.style.display = 'block';
        scrollToBottom();

        // API Call
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), TIMEOUT_MS);

        try {
            const resp = await fetch(API_URL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: text }),
                signal: controller.signal
            });
            clearTimeout(timeoutId);

            if (!resp.ok) throw new Error(`HTTP Error: ${resp.status}`);

            const data = await resp.json();
            const reply = data.reply || data.response || "I am meditating on the numbers. Please try again.";

            addMessage(reply, 'ai');

        } catch (err) {
            console.error("Numerology Chat Error:", err);
            const errMsg = err.name === 'AbortError'
                ? "Request timed out. Please try again."
                : "Unable to connect to the cosmos. Service unavailable.";
            addMessage(errMsg, 'ai');
        } finally {
            ui.loading.style.display = 'none';
            scrollToBottom();
            ui.input.focus();
        }
    }

    // --- INITIALIZATION ---
    function init() {
        injectStyles();
        ui = createChatInterface();

        // Event Bindings
        ui.closeBtn.onclick = () => toggleChat(false);
        ui.sendBtn.onclick = handleSend;
        ui.input.onkeypress = (e) => { if (e.key === 'Enter') handleSend(); };

        // Attach to Triggers
        const triggers = document.querySelectorAll('.numerology-chat-trigger');
        if (triggers.length > 0) {
            console.log(`Numerology Chatbot: Found ${triggers.length} native triggers.`);
            triggers.forEach(el => {
                el.addEventListener('click', (e) => {
                    e.preventDefault();
                    toggleChat(true);
                });
            });
        } else {
            console.log("Numerology Chatbot: No triggers found. Creating fallback FAB.");
            createFloatingButton();
        }
    }

    // Run when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

})();
