// Elements pakdo
const chatToggle = document.getElementById("chatToggle");
const chatBox = document.getElementById("chatBox");
const closeBtn = document.getElementById("closeBtn");
const sendBtn = document.getElementById("sendBtn");
const userInput = document.getElementById("userInput");
const chatMessages = document.getElementById("chatMessages");

// Chat kholo / band karo
chatToggle.addEventListener("click", () => chatBox.classList.toggle("open"));
closeBtn.addEventListener("click", () => chatBox.classList.remove("open"));

// Message screen pe dikhao
function addMessage(text, sender) {
  const div = document.createElement("div");
  div.className = "msg " + sender;
  div.textContent = text;
  chatMessages.appendChild(div);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Message bhejo backend ko
async function sendMessage() {
  const message = userInput.value.trim();
  if (!message) return;

  addMessage(message, "user");
  userInput.value = "";

  // "Typing..." dikhao
  addMessage("Typing...", "bot");
  const typingMsg = chatMessages.lastChild;

  try {
    const res = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: message }),
    });
    const data = await res.json();
    typingMsg.textContent = data.reply;  // "Typing..." ko jawab se replace karo
  } catch (err) {
    typingMsg.textContent = "Sorry, something went wrong. Please try again.";
  }
}

// Send button aur Enter key
sendBtn.addEventListener("click", sendMessage);
userInput.addEventListener("keypress", (e) => {
  if (e.key === "Enter") sendMessage();
});
