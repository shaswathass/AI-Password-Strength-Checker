from flask import Flask, render_template, request
import pickle
import math

app = Flask(__name__)

vectorizer, model = pickle.load(open("password_model.pkl", "rb"))

@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None

    if request.method == "POST":
        password = request.form["password"]

        # RULE BASED CHECK
        length = len(password)
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_symbol = any(not c.isalnum() for c in password)

        score = 0
        if length >= 8:
            score += 1
        if has_upper:
            score += 1
        if has_lower:
            score += 1
        if has_digit:
            score += 1
        if has_symbol:
            score += 1

        # ENTROPY
        char_pool = 0
        if has_lower:
            char_pool += 26
        if has_upper:
            char_pool += 26
        if has_digit:
            char_pool += 10
        if has_symbol:
            char_pool += 32

        entropy = 0
        if char_pool > 0:
            entropy = length * math.log2(char_pool)

        # FINAL DECISION
        if entropy < 28 or score <= 2:
            prediction = "Weak 🔴"
        elif 28 <= entropy < 50 or score == 3:
            prediction = "Medium 🟡"
        else:
            prediction = "Strong 🟢"

    return render_template("index.html", prediction=prediction)

if __name__ == "__main__":
    app.run(debug=True)
