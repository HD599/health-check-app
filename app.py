from flask import Flask, render_template, request
import time
import os

app = Flask(__name__)

@app.route('/')
def form():
    return render_template('form.html')

@app.route('/result', methods=['POST'])
def result():
    age = int(request.form['age'])
    sleep = request.form['sleep']
    tired = request.form['tired']
    digestion = request.form['digestion']

    score = 0
    if sleep == 'bad': score += 1
    if tired == 'yes': score += 1
    if digestion == 'poor': score += 1

    if score == 0:
        status = "สุขภาพดีมาก"
        supplement = "ไม่จำเป็นต้องเสริมอะไร"
    elif score == 1:
        status = "สุขภาพพอใช้"
        supplement = "อาจพิจารณาเสริมวิตามินรวม"
    else:
        status = "ควรปรับพฤติกรรมหรือเสริมอาหาร"
        supplement = "แนะนำวิตามิน B, แมกนีเซียม และดื่มน้ำมากขึ้น"

    with open("health_log.txt", "a", encoding="utf-8") as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} | อายุ:{age} | นอน:{sleep} | เหนื่อย:{tired} | ขับถ่าย:{digestion} | ผล:{status}\n")

    return render_template('result.html', status=status, supplement=supplement)



if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
