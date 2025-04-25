from flask import Flask, render_template, request, jsonify
from langchain_core.messages import HumanMessage
from chatbot import run_agent

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get_answer", methods=["POST"])
def get_answer():
    data = request.json
    user_question = data.get("question", "").strip()

    if not user_question:
        return jsonify({"answer": "Please enter a valid question."})
    
    # Get response from LangChain AI
    session_id = "user_session"  # You can modify this for real session handling
    response = run_agent(HumanMessage(content=user_question), session_id)
    
    return jsonify({"answer": response.get("output", "I'm not sure how to answer that.")})

if __name__ == "__main__":
    app.run(debug=True)
