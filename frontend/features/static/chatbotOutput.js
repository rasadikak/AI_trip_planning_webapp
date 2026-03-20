async function sendChat() {
    console.log("sendChat() called");
    const input = document.getElementById("chatInput");
    const chatBox = document.getElementById("chatBox");
    const sendBtn = document.getElementById("send-btn");
    console.log("input:", input);
    console.log("chatBox:", chatBox);
    console.log("sendBtn:", sendBtn);

    const userText = input.value.trim();
    console.log("userText:", userText);

    if (!userText) {
        console.log("Empty input, returning");
        return;
    }

    appendMessage("user", userText);
    input.value = "";
    input.style.height = "auto";
    chatBox.scrollTop = chatBox.scrollHeight;

    sendBtn.disabled = true;
    console.log("Send button disabled");

    const thinkingId = "thinking_" + Date.now();
    console.log("thinkingId:", thinkingId);

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
    console.log("Thinking animation added");

    try {
        const formdata = new FormData();
        formdata.append("chatInput", userText);
        console.log("Sending fetch to chatbot API...");

        const response = await fetch("http://127.0.0.1:8000/chatbot/", {
            method: "POST",
            body: formdata,
            credentials: "include" // Include cookies for authentication
        });
        console.log("Response received:", response.status, response.ok);

        if (!response.ok) throw new Error("Server error: " + response.status);

        const result = await response.json();
        console.log("Result:", result);

        document.getElementById(thinkingId)?.remove();
        console.log("Thinking animation removed");

        appendMessage("bot", result.response);
        console.log("Bot message appended");

    } catch (error) {
        console.error("Error in sendChat:", error);
        document.getElementById(thinkingId)?.remove();
        appendMessage("bot", "Sorry, something went wrong. Please try again.");
        showToast("❌ Something went wrong. Please try again.", "error");
    }

    sendBtn.disabled = false;
    console.log("Send button re-enabled");
    chatBox.scrollTop = chatBox.scrollHeight;
}

function appendMessage(role, text) {
    console.log("appendMessage called — role:", role);
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
    console.log("appendMessage done");
}

function escapeHtml(text) {
    return text
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;");
}

function handleChatKey(event) {
    console.log("Key pressed:", event.key);
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        console.log("Enter pressed — calling sendChat()");
        sendChat();
    }
}

function autoResize(textarea) {
    textarea.style.height = "auto";
    textarea.style.height = textarea.scrollHeight + "px";
}

function clearChat() {
    console.log("clearChat() called");
    const chatBox = document.getElementById("chatBox");
    chatBox.innerHTML = `
        <div class="message bot-message">
            <div class="avatar bot-avatar">🌴</div>
            <div class="bubble bot-bubble">
                <p>Chat cleared! How can I help you with your Sri Lanka trip? 🌴</p>
            </div>
        </div>`;
    console.log("Chat cleared");
    showToast("🗑️ Chat cleared", "info");
}

console.log("chatbotOutput.js loaded successfully");