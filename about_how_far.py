from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route("/")
def index():
    nearest_simple_fraction = request.args.get('nearest_simple_fraction', default="Enter your numbers and submit to see about how far you have come")
    queryNumerator = request.args.get('numerator', default=None)
    queryDenominator = request.args.get('denominator', default=None)
    qualifier = request.args.get('qualifier', default="")
    return render_template("about_how_far.html", nearest_simple_fraction = nearest_simple_fraction, qualifier = qualifier, numerator=queryNumerator, denominator=queryDenominator)

@app.route("/how_far", methods=['POST'])
def how_far():
    numerator = request.form["so-far"]
    denominator = request.form["total"]
    decimal = int(numerator) / int(denominator)

    if decimal > 1 or decimal < 0:
        return redirect(url_for("index"))

    simple_fractions = [
        {"fraction": "0", "value": 0}, 
        {"fraction": "1/10", "value": 1/10}, 
        {"fraction": "1/5", "value": 1/5}, 
        {"fraction": "1/4", "value": 1/4}, 
        {"fraction": "3/10", "value": 3/10}, 
        {"fraction": "1/3", "value": 1/3}, 
        {"fraction": "2/5", "value": 2/5}, 
        {"fraction": "1/2", "value": 1/2}, 
        {"fraction": "3/5", "value": 3/5}, 
        {"fraction": "2/3", "value": 2/3}, 
        {"fraction": "7/10", "value": 7/10}, 
        {"fraction": "3/4", "value": 3/4}, 
        {"fraction": "4/5", "value": 4/5}, 
        {"fraction": "9/10", "value": 9/10}, 
        {"fraction": "1", "value": 1}, 
    ]

    for i, fraction_obj in enumerate(simple_fractions):
        if fraction_obj["value"] == decimal:
            fraction = fraction_obj["fraction"]
            qualifier = "exactly "
            return redirect(url_for("index", nearest_simple_fraction=fraction, qualifier=qualifier, numerator=numerator, denominator=denominator))
        if fraction_obj["value"] > decimal:
            i_of_bigger_fraction = i
            bigger_fraction_obj = fraction_obj
            break

    distance_to_bigger = bigger_fraction_obj["value"] - decimal
    distance_to_smaller = decimal - simple_fractions[i_of_bigger_fraction - 1]["value"]

    if distance_to_bigger <= distance_to_smaller:
        fraction = bigger_fraction_obj["fraction"]
        qualifier = "almost "
    else:
        fraction = simple_fractions[i_of_bigger_fraction - 1]["fraction"]
        qualifier = "a little more than "

    return redirect(url_for("index", nearest_simple_fraction=fraction, qualifier=qualifier, numerator=numerator, denominator=denominator))

app.run(host="0.0.0.0", port=80)