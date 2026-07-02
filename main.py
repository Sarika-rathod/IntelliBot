from flask import Flask,render_template,request, jsonify
import os
from dotenv import load_dotenv
from groq import Groq 

app = Flask(__name__)

load_dotenv()
api_key=os.getenv("GROQ_API_KEY")

client=Groq(api_key=api_key)

@app.route("/")
def hello_world():
    return render_template("index.html")

@app.route("/ask",methods=["POST"])
def ask():
    question = request.form.get("question")

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role":"system",
                "content":"""Answer in 5-8 sentences unless the user asks for details.
                    - Be direct and concise.
                    - Do not explain unnecessarily.
                    - Use bullet points.
                    - If a one-line answer is enough, give one."""
            },
            {
                "role":"user",
                "content":question
            }
        ],
        temperature=0.1,
        max_tokens=512
    )

    answer=response.choices[0].message.content

    return jsonify({"response":answer}),200

@app.route("/summarize",methods=["POST"])
def summarize():
    email = request.form.get("email")

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role":"system",
                "content":"You are an expert email assistant."
            },
            {
                "role":"user",
                "content":f"Summarize this email in 2-3 sentences:\n{email}"
            }
        ],
        temperature=0.1,
        max_tokens=512
    )

    summary=response.choices[0].message.content
    return jsonify({"response":summary}),200

if __name__=="__main__":
    app.run(debug=True)