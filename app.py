from flask import Flask, render_template, request, jsonify
import os
from face_analysis import vedic_face_reader

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def reduce_number(num):
    while num > 9:
        num = sum(int(d) for d in str(num))
    return num

traits = {
    1: "Leader, confident, ambitious, independent",
    2: "Peaceful, emotional, cooperative, diplomatic",
    3: "Creative, expressive, joyful, optimistic",
    4: "Hardworking, practical, disciplined, loyal",
    5: "Adventurous, energetic, freedom lover",
    6: "Responsible, caring, family-oriented",
    7: "Spiritual, analytical, thinker, introvert",
    8: "Powerful, successful, goal-oriented",
    9: "Helpful, humanitarian, generous"
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/calculate", methods=["POST"])
def calculate():
    dob = request.form["dob"]
    year, month, day = dob.split("-")

    moolank = reduce_number(int(day))
    destiny = reduce_number(sum(int(d) for d in day + month + year))

    return render_template(
        "result.html",
        dob=dob,
        moolank=moolank,
        destiny=destiny,
        moolank_trait=traits[moolank],
        destiny_trait=traits[destiny]
    )

@app.route("/face_reading")
def face_reading():
    return render_template("face_reading.html")

@app.route("/face_analyze", methods=["POST"])
def face_analyze():
    if 'image' not in request.files:
        return render_template("face_reading.html", prediction="No file uploaded")
    file = request.files['image']
    if file.filename == '':
        return render_template("face_reading.html", prediction="No file selected")
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        try:
            prediction = vedic_face_reader(filepath)
            if isinstance(prediction, dict):
                return render_template("face_reading.html", prediction=prediction)
            else:
                return render_template("face_reading.html", prediction=prediction)
        except Exception as e:
            return render_template("face_reading.html", prediction=f"Error: {str(e)}")

if __name__ == "__main__":
    app.run(debug=True)
