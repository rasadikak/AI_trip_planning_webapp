async function sendChat() {
    const input = document.getElementById("chatInput");
    const chatBox = document.getElementById("chatBox");
    const sendBtn = document.getElementById("send-btn");
    const userText = input.value.trim();

    if (!userText) return;

    // Add user bubble
    appendMessage("user", userText);
    input.value = "";
    input.style.height = "auto";
    chatBox.scrollTop = chatBox.scrollHeight;

    // Disable send button while waiting
    sendBtn.disabled = true;

    // Add thinking animation
    const thinkingId = "thinking_" + Date.now();
    chatBox.innerHTML += `
        <div class="message bot-message" id="${thinkingId}">
            <div class="avatar bot-avatar">🌴</div>
            <div class="bubble bot-bubble thinking-bubble">
                <div class="dot"></div>
                <div class="dot"></div>
                <div class="dot"></div>
            </div>
        </div>`;
    chatBox.scrollTop = chatBox.scrollHeight;

    try {
        const formdata = new FormData();
        formdata.append("chatInput", userText);

        const response = await fetch("http://127.0.0.1:8000/chatbot/", {
            method: "POST",
            body: formdata
        });

        if (!response.ok) throw new Error("Server error");
        const result = await response.json();

        // Remove thinking dots
        document.getElementById(thinkingId)?.remove();

        // Add bot response
        appendMessage("bot", result.response);

    } catch (error) {
        document.getElementById(thinkingId)?.remove();
        appendMessage("bot", "Sorry, something went wrong. Please try again.");
    }

    sendBtn.disabled = false;
    chatBox.scrollTop = chatBox.scrollHeight;
}

function appendMessage(role, text) {
    const chatBox = document.getElementById("chatBox");
    const isUser = role === "user";

    const div = document.createElement("div");
    div.className = `message ${isUser ? "user-message" : "bot-message"}`;

    const avatar = document.createElement("div");
    avatar.className = `avatar ${isUser ? "user-avatar" : "bot-avatar"}`;
    avatar.innerText = isUser ? "You" : "🌴";

    const bubble = document.createElement("div");
    bubble.className = `bubble ${isUser ? "user-bubble" : "bot-bubble"}`;
    bubble.innerHTML = isUser ? escapeHtml(text) : marked.parse(text);

    div.appendChild(avatar);
    div.appendChild(bubble);
    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function escapeHtml(text) {
    return text
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;");
}

function handleChatKey(event) {
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        sendChat();
    }
}

function autoResize(textarea) {
    textarea.style.height = "auto";
    textarea.style.height = textarea.scrollHeight + "px";
}

function clearChat() {
    const chatBox = document.getElementById("chatBox");
    chatBox.innerHTML = `
        <div class="message bot-message">
            <div class="avatar bot-avatar">🌴</div>
            <div class="bubble bot-bubble">
                <p>Chat cleared! How can I help you with your Sri Lanka trip? 🌴</p>
            </div>
        </div>`;
}