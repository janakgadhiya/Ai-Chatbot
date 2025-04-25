//Function to validate login form
function validateForm() {
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;
    
    if (username === "" || password === "") {
        alert("Both fields are required");
        return false;
    }
    return true;
}

//Function to handle login redirection
function redirectToLanding(event) {
    event.preventDefault(); // Prevent actual form submission
    
    if (validateForm()) {
        window.location.href = "dummy.html"; // Redirect only if validation passes
    }
}

// Function to send chatbot query
function sendQuery() {
    const userInput = document.getElementById("userInput").value.trim();

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
        document.getElementById("userInput").value = "";
        chatbox.scrollTop = chatbox.scrollHeight;
    })
    .catch(error => {
        console.error("Error:", error);
        alert("Something went wrong. Please try again.");
    });
}

// ✅ Function to toggle chatbot visibility
function toggleChat() {
    const chatContainer = document.getElementById("chatbot-container");
    chatContainer.classList.toggle("chatbot-hidden");
}

// ✅ Handle Enter key press in chatbot input field
document.addEventListener("DOMContentLoaded", function () {
    const userInput = document.getElementById("userInput");
    
    userInput.addEventListener("keypress", function (event) {
        if (event.key === "Enter") {
            event.preventDefault(); // Prevents newline in input
            sendQuery();
        }
    });

    // ✅ Attach chatbot toggle button functionality
    document.getElementById("chatbot-toggle").addEventListener("click", toggleChat);
});
