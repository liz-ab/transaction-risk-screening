from flask import Flask, render_template, request

app = Flask(__name__)

# ---------------- FRAUD RISK ENGINE ----------------

def calculate_risk(amount, time, txn_count_last_min):
    risk_score = 0

    # Amount-based risk
    if amount >= 100000:
        risk_score += 50
    elif amount >= 50000:
        risk_score += 30
    elif amount >= 20000:
        risk_score += 10

    # Time-based risk (late night)
    if 0 <= time <= 5:
        risk_score += 20

    # Velocity-based risk
    if txn_count_last_min >= 5:
        risk_score += 30
    elif txn_count_last_min >= 3:
        risk_score += 15

    return risk_score


def fraud_decision(risk_score):
    if risk_score >= 70:
        return "Transaction Blocked"
    elif risk_score >= 40:
        return "Additional Verification Required"
    else:
        return "Transaction Approved"

# ---------------- ROUTES ----------------

@app.route("/")
def welcome():
    return render_template("welcome.html")


@app.route("/check", methods=["GET", "POST"])
def check_transaction():
    result = ""

    if request.method == "POST":
        amount = int(request.form["amount"])
        time = int(request.form["time"])
        txn_count_last_min = int(request.form["txn_count"])

        risk_score = calculate_risk(amount, time, txn_count_last_min)
        result = fraud_decision(risk_score)

    return render_template("index.html", result=result)


if __name__ == "__main__":
    app.run(debug=True)
