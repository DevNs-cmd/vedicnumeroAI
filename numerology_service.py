from flask import Flask, render_template, request

app = Flask(__name__)

# Reduce number to single digit (Numerology rule)
def reduce_number(num):
    while num > 9:
        num = sum(int(d) for d in str(num))
    return num

# Numerology traits
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
    dob = request.form["dob"]  # YYYY-MM-DD

    year, month, day = dob.split("-")

    # Moolank (Birth Number)
    moolank = reduce_number(int(day))

    # Destiny Number
    destiny_sum = sum(int(d) for d in day + month + year)
    destiny = reduce_number(destiny_sum)

    return render_template(
        "result.html",
        dob=dob,
        moolank=moolank,
        destiny=destiny,
        moolank_trait=traits[moolank],
        destiny_trait=traits[destiny]
    )

if __name__ == "__main__":
    app.run(debug=True)
