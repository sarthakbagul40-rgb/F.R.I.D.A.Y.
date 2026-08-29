/* ==========================================================================
   F.R.I.D.A.Y. // NEURAL TACTICAL HUD CONTROLLER (UI/UX PRO)
   ========================================================================== */

const statusIndicator = document.getElementById('status-indicator');
const chatContainer = document.getElementById('chat-container');
const chatInput = document.getElementById('chat-input');
const sendBtn = document.getElementById('send-btn');
const audioWave = document.getElementById('audio-wave');
const backToTopBtn = document.getElementById('back-to-top-btn');
const voiceLabel = document.getElementById('active-voice-label');

// Transmit button & Enter key
sendBtn.addEventListener('click', () => {
    const text = chatInput.value.trim();
    if(text) {
        addMessage(text, 'user');
        sendCommand(text);
        chatInput.value = '';
    }
});

chatInput.addEventListener('keypress', (e) => {
    if(e.key === 'Enter') sendBtn.click();
});

// Interactive Quick Action Chips
document.querySelectorAll('.chip-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        const cmd = btn.getAttribute('data-cmd');
        if (cmd) {
            addMessage(cmd, 'user');
            sendCommand(cmd);
        }
    });
});

// Smooth Back to Top Button
if (chatContainer && backToTopBtn) {
    chatContainer.addEventListener('scroll', () => {
        if (chatContainer.scrollTop > 300) {
            backToTopBtn.classList.add('visible');
        } else {
            backToTopBtn.classList.remove('visible');
        }
    });

    backToTopBtn.addEventListener('click', () => {
        chatContainer.scrollTo({ top: 0, behavior: 'smooth' });
    });
}

function formatTime() {
    const now = new Date();
    return now.toTimeString().split(' ')[0]; // Returns HH:MM:SS
}

function escapeHtml(text) {
    return text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

function detectVoiceProfile(text) {
    const marathiKeywords = ["ahe", "aahe", "ahet", "zala", "kasa", "kashi", "namaskar", "dhanyawad", "kay", "ho"];
    const hindiKeywords = ["haan", "nahi", "karo", "karna", "kaise", "kripya", "acha", "theek", "bhai", "shukriya", "kya", "hai", "main", "abhi"];
    
    // Check Devanagari Unicode
    if (/[\u0900-\u097F]/.test(text)) {
        if (/आहे|झाला|कसा|काय|नमस्कार/.test(text)) return "AUDIO: AAROHI (MARATHI)";
        return "AUDIO: SWARA (HINDI)";
    }
    
    const words = text.toLowerCase().split(/\W+/);
    if (words.some(w => marathiKeywords.includes(w))) return "AUDIO: AAROHI (MARATHI)";
    if (words.some(w => hindiKeywords.includes(w))) return "AUDIO: SWARA (HINDI)";
    return "AUDIO: EMILY NEURAL (IRISH)";
}

function formatAiResponse(text) {
    // Check for code blocks in triple backticks
    const codeBlockRegex = /```([a-zA-Z0-9_\-\+]*)\n([\s\S]*?)```/g;
    let formatted = text.replace(codeBlockRegex, (match, lang, code) => {
        const escapedCode = escapeHtml(code.trim());
        const langLabel = lang ? lang.toUpperCase() : 'CODE';
        return `
            <div class="code-box">
                <div class="code-box-header">
                    <span class="code-lang">${langLabel}</span>
                    <button class="copy-code-btn" onclick="navigator.clipboard.writeText(\`${escapedCode.replace(/`/g, '\\`')}\`); this.innerText='COPIED!'; setTimeout(() => this.innerText='COPY', 2000)">COPY</button>
                </div>
                <pre class="code-content"><code>${escapedCode}</code></pre>
            </div>
        `;
    });

    // Replace line breaks outside code boxes
    formatted = formatted
        .replace(/\n\n/g, '<br><br>')
        .replace(/\n/g, '<br>');
    return formatted;
}

function addMessage(text, sender, downloadUrl = null) {
    const div = document.createElement('div');
    const timeStr = formatTime();
    div.className = `message ${sender}`;

    if (sender === 'user') {
        div.innerHTML = `
            <div class="msg-meta">
                <span class="msg-sender">[ OPERATOR // BOSS ]</span>
                <span class="msg-time">${timeStr}</span>
            </div>
            <div class="msg-bubble user-bubble">
                ${escapeHtml(text)}
            </div>
        `;
    } else {
        // Auto-update top bar voice profile pill
        if (voiceLabel) {
            voiceLabel.innerText = detectVoiceProfile(text);
        }

        let html = `
            <div class="msg-meta">
                <span class="msg-sender">[ F.R.I.D.A.Y. // NEURAL CORE ]</span>
                <span class="msg-time">${timeStr}</span>
            </div>
            <div class="msg-bubble ai-bubble">
                ${formatAiResponse(text)}
        `;
        if (downloadUrl) {
            html += `<br><a href="${downloadUrl}" class="download-link" target="_blank">📥 DOWNLOAD GENERATED FILE</a>`;
        }
        html += `</div>`;
        div.innerHTML = html;
    }
    
    chatContainer.appendChild(div);
    chatContainer.scrollTo({
        top: chatContainer.scrollHeight,
        behavior: 'smooth'
    });
}

async function sendCommand(cmd) {
    statusIndicator.innerText = "PROCESSING";
    statusIndicator.classList.remove('error');
    if (audioWave) audioWave.classList.remove('hidden');
    
    try {
        const res = await fetch('/api/command', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({command: cmd})
        });
        const data = await res.json();
        
        statusIndicator.innerText = "UPLINK_STABLE";
        statusIndicator.classList.remove('error');
        if (audioWave) audioWave.classList.add('hidden');
        
        let responseText = data.response || (data.action_taken ? "Command executed silently, Boss." : "No response generated.");
        addMessage(responseText, 'system', data.download_url);
    } catch(err) {
        console.error(err);
        statusIndicator.innerText = "LINK_DROPPED";
        statusIndicator.classList.add('error');
        if (audioWave) audioWave.classList.add('hidden');
        addMessage("CRITICAL ERROR: Telemetry link dropped with core server.", 'system');
    }
}

// Security Protocol: GPS Telemetry Sync
if ("geolocation" in navigator) {
    navigator.geolocation.getCurrentPosition(async (position) => {
        try {
            await fetch('/api/location', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    lat: position.coords.latitude,
                    lon: position.coords.longitude
                })
            });
        } catch (e) {
            console.error("Location sync failed.", e);
        }
    }, (error) => {
        console.warn("Location telemetry permission not granted.");
    });
}
