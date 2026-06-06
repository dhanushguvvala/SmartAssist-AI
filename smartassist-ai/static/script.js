async function sendMessage() {

    let message =
        document.getElementById("message").value;

    let mode =
        document.getElementById("mode").value;

    if(message.trim() === "")
        return;

    let chatbox =
        document.getElementById("chatbox");

    chatbox.innerHTML += `
        <div class="user-message">
            ${message}
        </div>
    `;

    chatbox.innerHTML += `
        <div class="loading" id="loading">
            AI is thinking...
        </div>
    `;

    chatbox.scrollTop = chatbox.scrollHeight;

    const response = await fetch("/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            message,
            mode
        })
    });

    const data = await response.json();

    document.getElementById("loading").remove();

    chatbox.innerHTML += `
    <div class="ai-message">
        ${marked.parse(data.reply)}
    </div>
    `;

    chatbox.scrollTop = chatbox.scrollHeight;

    document.getElementById("message").value = "";
}

async function summarizeChat() {

    const response = await fetch("/summarize", {
        method: "POST"
    });

    const data = await response.json();

    alert(data.summary);
}

function startVoice() {

    const recognition =
        new webkitSpeechRecognition();

    recognition.lang = "en-US";

    recognition.onresult = function(event) {

        document.getElementById("message").value =
            event.results[0][0].transcript;
    };

    recognition.start();
}

document
.getElementById("message")
.addEventListener("keypress", function(e){

    if(e.key === "Enter")
        sendMessage();
});