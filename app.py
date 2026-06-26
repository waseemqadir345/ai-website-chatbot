"""
AI Customer Support Chatbot - Backend
--------------------------------------
Flask server jo ChatGPT API se connect hota hai.
Business ki apni info (services, pricing, FAQs) ke hisaab se jawab deta hai.

Setup:
    1. pip install -r requirements.txt
    2. .env file mein apni OPENAI_API_KEY daalo
    3. python app.py
    4. Browser mein kholo: http://localhost:5000
"""

import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from openai import OpenAI

# .env file se API key load karo
load_dotenv()

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ===========================================================
# YAHAN APNE BUSINESS KI INFO DAALO (chatbot isi se jawab dega)
# ===========================================================
BUSINESS_INFO = """
You are a friendly customer support assistant for "BrightClean Services",
a home cleaning company based in New York.

Business details:
- Services: house cleaning, office cleaning, deep cleaning, carpet cleaning.
- Pricing: house cleaning starts at $80, deep cleaning at $150.
- Hours: Monday to Saturday, 8 AM - 6 PM.
- Booking: customers can book by calling (555) 123-4567 or emailing hello@brightclean.com.
- Service area: New York City and nearby areas.

Rules:
- Answer only based on the information above.
- Be polite, short, and helpful.
- If you don't know something, tell the customer to contact us by phone or email.
"""


@app.route("/")
def home():
    """Chat widget wala page dikhata hai."""
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    """User ka message leta hai, ChatGPT se jawab laata hai."""
    user_message = request.json.get("message", "").strip()

    if not user_message:
        return jsonify({"reply": "Please type a message."})

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": BUSINESS_INFO},
                {"role": "user", "content": user_message},
            ],
            max_tokens=200,
            temperature=0.7,
        )
        reply = response.choices[0].message.content.strip()
        return jsonify({"reply": reply})

    except Exception as e:
        print("Error:", e)
        return jsonify({
            "reply": "Sorry, I'm having trouble right now. "
                     "Please contact us by phone or email."
        })


if __name__ == "__main__":
    app.run(debug=True, port=5000)
