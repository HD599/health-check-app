from flask import Flask, render_template, request, redirect, url_for, session
import time
import os


app = Flask(__name__)
app.secret_key = "secret123"  # ใช้สำหรับ session

# คำถามตัวอย่าง
questions = [
    {"q": "ท้องฟ้ามีสีอะไร?", "options": ["แดง", "ฟ้า", "เขียว", "เหลือง"], "answer": "ฟ้า"},
    {"q": "2+2 เท่ากับ?", "options": ["3", "4", "5", "6"], "answer": "4"},
    # ... เพิ่มจนครบ 10 ข้อ
]

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        session["name"] = request.form.get("username")
        session["score"] = 0
        session["current_q"] = 0
        return redirect(url_for("quiz"))
    return render_template("index.html")

@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    current_q = session.get("current_q", 0)
    score = session.get("score", 0)

    if request.method == "POST":
        answer = request.form.get("answer")
        if answer == questions[current_q]["answer"]:
            score += 1
        session["score"] = score
        session["current_q"] = current_q + 1

        if session["current_q"] >= len(questions):
            return redirect(url_for("result"))

        return redirect(url_for("quiz"))

    return render_template("quiz.html", 
                           question=questions[current_q], 
                           qnum=current_q+1, 
                           total=len(questions),
                           progress=(current_q/len(questions))*100)

@app.route("/result")
def result():
    score = session.get("score", 0)
    if score <= 3:
        color = "เมฆสีเทาเข้ม"
    elif score <= 6:
        color = "เมฆสีเทาอ่อน"
    else:
        color = "เมฆสีฟ้า"
    return render_template("result.html", score=score, color=color)

#if __name__ == "__main__":
    #app.run(debug=True)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)




