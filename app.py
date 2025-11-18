from flask import Flask, render_template, request

from ml.predictor import RandomForestPredictor

app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/static",
)

predictor = RandomForestPredictor()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        prediction = predictor.predict_from_form(request.form)
    except (KeyError, ValueError) as exc:
        return render_template("index.html", error=str(exc)), 400

    return render_template("index.html", prediction=prediction)


if __name__ == '__main__':
    app.run(debug=True)
