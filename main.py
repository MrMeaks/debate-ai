from flask import Flask, render_template, request
import openai
import os

openai.api_key = os.environ.get("OPENAI_API_KEY")

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        topic = request.form["topic"]
        stance = request.form["stance"]

        prompt = f"""
You're a debate assistant. The topic is: "{topic}"
Give a detailed argument for the {stance} side, and 3 rebuttals to the opposing view.

Format:
- Argument:
- Opposing Rebuttals:
    1. [Rebuttal] → [Response]
    2. ...
    3. ...
"""

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=600,
        )

        debate_output = response["choices"][0]["message"]["content"]
        return render_template("index.html", output=debate_output, topic=topic, stance=stance)

    return render_template("index.html", output=None)
