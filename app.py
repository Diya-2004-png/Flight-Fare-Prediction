from flask import Flask, render_template, request
import pickle
import pandas as pd

# ⭐ FIRST create Flask app
app = Flask(__name__)

# ⭐ Load model
model = pickle.load(open("flight_model.pkl", "rb"))


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    try:
        airline = int(request.form.get("airline"))
        source = int(request.form.get("source"))
        destination = int(request.form.get("destination"))

        date = request.form.get("date")
        time = request.form.get("time")

        day = int(date.split("-")[2])
        month = int(date.split("-")[1])

        hour = int(time.split(":")[0])
        minute = int(time.split(":")[1])

        sample = pd.DataFrame([{
            'Airline_encoded': airline,
            'Source_encoded': source,
            'Destination_encoded': destination,
            'Hour': hour,
            'Minute': minute,
            'Journey_Day': day,
            'Journey_Month': month
        }])

        prediction = model.predict(sample)[0]

        return render_template(
            "index.html",
            result=f"₹ {round(prediction,2)}"
        )

    except:
        return render_template(
            "index.html",
            result="⚠️ Error in input"
        )


# ⭐ VERY IMPORTANT LAST LINE
if __name__ == "__main__":
    app.run(debug=True)