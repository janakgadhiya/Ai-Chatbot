// Function to send query to backend
function sendQuery() {
    const userInputField = document.getElementById("userInput");
    const userInput = userInputField.value.trim();

    if (userInput === "") {
        alert("Please enter a question.");
        return;
    }

    fetch("/get_answer", { 
        method: "POST",
        body: JSON.stringify({ question: userInput }),  
        headers: { "Content-Type": "application/json" }
    })
    .then(response => response.json())
    .then(data => {
        const chatbox = document.getElementById("chatbox");
        chatbox.innerHTML += `<p><b>You:</b> ${userInput}</p>`;
        chatbox.innerHTML += `<p><b>Bot:</b> ${data.answer}</p>`; 

        userInputField.value = ""; // Clear input field
        userInputField.focus(); // Auto-focus back on input field
        chatbox.scrollTop = chatbox.scrollHeight; // Auto-scroll to the latest message
    })
    .catch(error => {
        console.error("Error:", error);
        alert("Something went wrong. Please try again.");
    });
}

// ✅ Allow pressing "Enter" to send a message
document.getElementById("userInput").addEventListener("keydown", function (event) {
    if (event.key === "Enter") {
        event.preventDefault(); // Prevents newline in input
        sendQuery(); // Call sendQuery function
    }
});

// ✅ Toggle chat visibility
function toggleChat() {
    const chatContainer = document.getElementById("chat-container");
    chatContainer.style.display = (chatContainer.style.display === "block") ? "none" : "block";
}
