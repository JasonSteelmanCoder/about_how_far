from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route("/")
def index():
    nearest_simple_fraction = request.args.get('nearest_simple_fraction', default="Enter your numbers and submit to see about how far you've come")
    queryNumerator = request.args.get('numerator', default=None)
    queryDenominator = request.args.get('denominator', default=None)
    if queryNumerator and queryDenominator:
        queryPercent = str(round((int(queryNumerator) / int(queryDenominator)) * 100))
    else:
        queryPercent = 0
    queryFractionValue = request.args.get('fraction_value', default=None)
    qualifier = request.args.get('qualifier', default="")
    return render_template("about_how_far.html", nearest_simple_fraction = nearest_simple_fraction, qualifier = qualifier, numerator=queryNumerator, denominator=queryDenominator, percent=queryPercent, fraction_value=queryFractionValue)

@app.route("/how_far", methods=['POST'])
def how_far():
    numerator = request.form["so-far"]
    denominator = request.form["total"]
    decimal = int(numerator) / int(denominator)

    if decimal > 1 or decimal < 0:
        return redirect(url_for("index"))

    simple_fractions = [
        {"fraction": "0%", "value": 0}, 
        {"fraction": "1/10", "value": 1/10},
        {"fraction": "1/6", "value": 1/6}, 
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
        {"fraction": "5/6", "value": 5/6}, 
        {"fraction": "9/10", "value": 9/10}, 
        {"fraction": "all", "value": 1}, 
    ]

    # Go through the simple fractions from low to high.
    for i, fraction_obj in enumerate(simple_fractions):
        # If the next fraction has exactly the same value as the decimal, rerender the page with "exactly" and the fraction
        if fraction_obj["value"] == decimal:
            fraction = fraction_obj["fraction"]
            fraction_value = fraction_obj["value"]
            qualifier = "exactly "
            return redirect(url_for("index", nearest_simple_fraction=fraction, qualifier=qualifier, numerator=numerator, denominator=denominator, fraction_value=fraction_value))
        # If the next fraction is higher than the decimal value, remember which one it is and stop iterating
        if fraction_obj["value"] > decimal:
            i_of_bigger_fraction = i
            bigger_fraction_obj = fraction_obj
            break

    # Find distances to the two nearest fractions to the decimal value
    distance_to_bigger = bigger_fraction_obj["value"] - decimal
    distance_to_smaller = decimal - simple_fractions[i_of_bigger_fraction - 1]["value"]

    # Check which fraction is closest to the decimal value
    if distance_to_bigger <= distance_to_smaller:
        fraction = bigger_fraction_obj["fraction"]
        fraction_value = bigger_fraction_obj["value"]
        qualifier = "almost "
    else:
        fraction = simple_fractions[i_of_bigger_fraction - 1]["fraction"]
        fraction_value = simple_fractions[i_of_bigger_fraction - 1]["value"]
        qualifier = "a little more than "

    # Rerender the page with the correct fraction and qualifier
    return redirect(url_for("index", nearest_simple_fraction=fraction, qualifier=qualifier, numerator=numerator, denominator=denominator, fraction_value=fraction_value))

app.run(host="0.0.0.0", port=80)