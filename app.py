from flask import Flask, render_template, request, redirect, url_for, session
import numpy as np
from scipy import stats

app = Flask(__name__)

# Used to temporarily store the latest analysis result
app.secret_key = "smartphone-battery-analysis-2026"


def calculate_analysis(times, batteries, threshold):

    times = np.array(times, dtype=float)
    batteries = np.array(batteries, dtype=float)

    # -----------------------------
    # BASIC STATISTICS
    # -----------------------------

    mean_battery = np.mean(batteries)
    variance = np.var(batteries)
    standard_deviation = np.std(batteries)

    # -----------------------------
    # LINEAR REGRESSION
    # -----------------------------

    slope, intercept, r_value, p_value, std_err = stats.linregress(
        times,
        batteries
    )

    predicted_battery = slope * times + intercept

    correlation = r_value
    r_squared = r_value ** 2

    # Battery drain rate
    drain_rate = abs(slope)

    # -----------------------------
    # THRESHOLD PREDICTION
    # -----------------------------

    if slope < 0:
        threshold_time = (threshold - intercept) / slope

        if threshold_time < 0:
            threshold_time = None
    else:
        threshold_time = None

    # -----------------------------
    # NORMAL DISTRIBUTION
    # -----------------------------

    if standard_deviation > 0:

        z_score = (
            threshold - mean_battery
        ) / standard_deviation

        normal_probability = stats.norm.cdf(z_score)

    else:

        z_score = 0
        normal_probability = 0

    # -----------------------------
    # EMPIRICAL PROBABILITY
    # -----------------------------

    empirical_probability = np.mean(
        batteries <= threshold
    )

    # -----------------------------
    # PROBABILITY DISTRIBUTION
    # -----------------------------

    probability_distribution = []

    for battery in batteries:

        if standard_deviation > 0:

            probability = stats.norm.pdf(
                battery,
                mean_battery,
                standard_deviation
            )

        else:

            probability = 0

        probability_distribution.append({
            "battery": round(float(battery), 2),
            "probability": round(float(probability), 6)
        })

    # -----------------------------
    # DRAIN INTERPRETATION
    # -----------------------------

    if drain_rate > 8:

        drain_interpretation = (
            "The battery is draining very quickly."
        )

    elif drain_rate > 4:

        drain_interpretation = (
            "The battery is draining at a moderate rate."
        )

    else:

        drain_interpretation = (
            "The battery is draining slowly."
        )

    # -----------------------------
    # CORRELATION INTERPRETATION
    # -----------------------------

    if correlation < -0.8:

        correlation_interpretation = (
            "There is a very strong negative relationship "
            "between time and battery percentage."
        )

    elif correlation < -0.5:

        correlation_interpretation = (
            "There is a strong negative relationship "
            "between time and battery percentage."
        )

    elif correlation < 0:

        correlation_interpretation = (
            "There is a negative relationship between "
            "time and battery percentage."
        )

    else:

        correlation_interpretation = (
            "The relationship between time and battery "
            "percentage is weak or positive."
        )

    # -----------------------------
    # THRESHOLD MESSAGE
    # -----------------------------

    if threshold_time is not None:

        threshold_message = (
            f"The battery is estimated to reach "
            f"{threshold}% at approximately "
            f"{threshold_time:.2f} hours."
        )

    else:

        threshold_message = (
            "The selected threshold cannot be reached "
            "using the current linear model."
        )

    # -----------------------------
    # RETURN ALL RESULTS
    # -----------------------------

    return {

        "times": [
            float(value)
            for value in times
        ],

        "batteries": [
            float(value)
            for value in batteries
        ],

        "threshold": float(threshold),

        "mean_battery":
            round(float(mean_battery), 2),

        "variance":
            round(float(variance), 2),

        "standard_deviation":
            round(float(standard_deviation), 2),

        "drain_rate":
            round(float(drain_rate), 2),

        "slope":
            round(float(slope), 4),

        "intercept":
            round(float(intercept), 4),

        "correlation":
            round(float(correlation), 4),

        "r_squared":
            round(float(r_squared), 4),

        "p_value":
            round(float(p_value), 6),

        "threshold_time":
            (
                round(float(threshold_time), 2)
                if threshold_time is not None
                else None
            ),

        "survival_prediction":
            (
                round(float(threshold_time), 2)
                if threshold_time is not None
                else None
            ),

        "z_score":
            round(float(z_score), 4),

        "normal_probability":
            round(float(normal_probability), 4),

        "empirical_probability":
            round(float(empirical_probability), 4),

        "probability_distribution":
            probability_distribution,

        "drain_interpretation":
            drain_interpretation,

        "correlation_interpretation":
            correlation_interpretation,

        "threshold_message":
            threshold_message,

        "predicted_battery": [
            round(float(value), 2)
            for value in predicted_battery
        ]
    }


@app.route("/", methods=["GET", "POST"])
def index():

    # --------------------------------
    # GET REQUEST
    # --------------------------------

    if request.method == "GET":

        result = session.pop("analysis_result", None)
        error = session.pop("analysis_error", None)

        return render_template(
            "index.html",
            result=result,
            error=error
        )

    # --------------------------------
    # POST REQUEST
    # --------------------------------

    try:

        time_input = request.form.get(
            "times",
            ""
        ).strip()

        battery_input = request.form.get(
            "batteries",
            ""
        ).strip()

        threshold_input = request.form.get(
            "threshold",
            "10"
        ).strip()

        # Check empty input

        if not time_input or not battery_input:

            raise ValueError(
                "Please enter both time values and battery values."
            )

        # Convert time values

        times = [
            float(value.strip())
            for value in time_input.split(",")
            if value.strip()
        ]

        # Convert battery values

        batteries = [
            float(value.strip())
            for value in battery_input.split(",")
            if value.strip()
        ]

        # Convert threshold

        threshold = float(threshold_input)

        # Minimum observations

        if len(times) < 3:

            raise ValueError(
                "Please enter at least 3 observations."
            )

        # Matching number of values

        if len(times) != len(batteries):

            raise ValueError(
                "The number of time values must match "
                "the number of battery values."
            )

        # Battery range

        if any(
            value < 0 or value > 100
            for value in batteries
        ):

            raise ValueError(
                "Battery values must be between 0 and 100."
            )

        # Threshold range

        if threshold < 0 or threshold > 100:

            raise ValueError(
                "Threshold must be between 0 and 100."
            )

        # Time values must be non-negative

        if any(
            value < 0
            for value in times
        ):

            raise ValueError(
                "Time values cannot be negative."
            )

        # Duplicate time values are not useful
        # for this regression model

        if len(set(times)) != len(times):

            raise ValueError(
                "Time values should not contain duplicates."
            )

        # Sort observations by time

        observations = sorted(
            zip(times, batteries),
            key=lambda item: item[0]
        )

        times = [
            item[0]
            for item in observations
        ]

        batteries = [
            item[1]
            for item in observations
        ]

        # Perform complete analysis

        result = calculate_analysis(
            times,
            batteries,
            threshold
        )

        # Store result temporarily

        session["analysis_result"] = result

        # Redirect after POST
        # This prevents the browser from
        # resubmitting the form on refresh.

        return redirect(
            url_for("index")
        )

    except ValueError as exc:

        session["analysis_error"] = str(exc)

        return redirect(
            url_for("index")
        )

    except Exception as exc:

        session["analysis_error"] = (
            f"An unexpected error occurred: {exc}"
        )

        return redirect(
            url_for("index")
        )


if __name__ == "__main__":

    app.run(
        debug=True
    )