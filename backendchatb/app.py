from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from langchain_core.messages import HumanMessage
from chatbot import run_agent

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get_answer", methods=["POST"])
def get_answer():
    try:
        data = request.json
        user_question = data.get("question", "").strip()

        if not user_question:
            return jsonify({"answer": "Please enter a valid question."}), 400

        # Get response from LangChain AI
        session_id = "user_session"  # Modify this for real session handling
        response = run_agent(HumanMessage(content=user_question), session_id)

        # Debugging: Print the response format to check its structure
        print("Raw Response from LangChain:", response)

        # Ensure correct extraction of answer
        if isinstance(response, dict) and "output" in response:
            answer = response["output"]
        else:
            answer = str(response) if response else "Sorry, I couldn't find an answer."

        return jsonify({"answer": answer})

    except Exception as e:
        print(f"Error processing request: {str(e)}")
        return jsonify({"answer": "I apologize, but I encountered an error processing your request. Please try again."}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
