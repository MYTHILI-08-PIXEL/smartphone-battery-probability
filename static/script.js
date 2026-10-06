// =========================================================
// SMARTPHONE BATTERY PROBABILITY ANALYSIS
// Dynamic Frontend Logic
// =========================================================


// =========================================================
// DYNAMIC EXAMPLE GENERATOR
// =========================================================

function loadExample() {

    // Random number of observations
    const observationCount =
        Math.floor(Math.random() * 6) + 7;

    // Random starting battery
    const startingBattery =
        Math.floor(Math.random() * 11) + 90;

    // Random battery drain rate
    const drainRate =
        Math.random() * 4 + 3;

    const times = [];
    const batteries = [];

    let currentBattery = startingBattery;

    for (let i = 0; i < observationCount; i++) {

        times.push(i + 1);

        // Small random variation
        const randomVariation =
            (Math.random() - 0.5) * 3;

        currentBattery =
            currentBattery -
            drainRate +
            randomVariation;

        // Keep battery inside realistic range
        currentBattery =
            Math.max(
                5,
                Math.min(100, currentBattery)
            );

        batteries.push(
            Math.round(currentBattery * 10) / 10
        );
    }


    // Random threshold
    const minimumBattery =
        Math.min(...batteries);

    const maximumBattery =
        Math.max(...batteries);

    let threshold =
        Math.floor(
            Math.random() *
            (Math.max(15, Math.floor(maximumBattery - 20)) -
            10 + 1)
        ) + 10;

    // Make sure threshold is below
    // the starting battery
    threshold =
        Math.min(
            threshold,
            Math.floor(startingBattery * 0.4)
        );


    // Put generated values into form

    document.getElementById("times").value =
        times.join(", ");

    document.getElementById("batteries").value =
        batteries.join(", ");

    document.getElementById("threshold").value =
        threshold;

}


// =========================================================
// CLEAR FORM
// =========================================================

function clearForm() {

    document.getElementById("times").value = "";

    document.getElementById("batteries").value = "";

    document.getElementById("threshold").value = "20";

}


// =========================================================
// CHART CONFIGURATION
// =========================================================

document.addEventListener(
    "DOMContentLoaded",
    function () {


        // -------------------------------------------------
        // BATTERY VS TIME CHART
        // -------------------------------------------------

        const batteryCanvas =
            document.getElementById("batteryChart");


        if (
            batteryCanvas &&
            times.length > 0
        ) {

            new Chart(
                batteryCanvas,
                {

                    type: "line",

                    data: {

                        labels: times,

                        datasets: [

                            {
                                label: "Actual Battery (%)",

                                data: batteries,

                                borderWidth: 3,

                                tension: 0.35,

                                pointRadius: 4,

                                pointHoverRadius: 7
                            },

                            {
                                label: "Predicted Battery (%)",

                                data: predictedBattery,

                                borderWidth: 2,

                                borderDash: [
                                    8,
                                    5
                                ],

                                tension: 0.35,

                                pointRadius: 2
                            }

                        ]

                    },

                    options: {

                        responsive: true,

                        maintainAspectRatio: false,

                        interaction: {
                            mode: "index",
                            intersect: false
                        },

                        plugins: {

                            legend: {
                                labels: {
                                    color: "#cbd5e1"
                                }
                            },

                            tooltip: {
                                enabled: true
                            }

                        },

                        scales: {

                            x: {

                                title: {
                                    display: true,
                                    text: "Time (hours)",
                                    color: "#94a3b8"
                                },

                                ticks: {
                                    color: "#94a3b8"
                                },

                                grid: {
                                    color:
                                        "rgba(148,163,184,0.08)"
                                }

                            },

                            y: {

                                min: 0,

                                max: 100,

                                title: {
                                    display: true,
                                    text: "Battery (%)",
                                    color: "#94a3b8"
                                },

                                ticks: {
                                    color: "#94a3b8"
                                },

                                grid: {
                                    color:
                                        "rgba(148,163,184,0.08)"
                                }

                            }

                        }

                    }

                }
            );

        }


        // -------------------------------------------------
        // PROBABILITY DISTRIBUTION CHART
        // -------------------------------------------------

        const probabilityCanvas =
            document.getElementById(
                "probabilityChart"
            );


        if (
            probabilityCanvas &&
            probabilityLabels.length > 0
        ) {

            new Chart(
                probabilityCanvas,
                {

                    type: "bar",

                    data: {

                        labels: probabilityLabels,

                        datasets: [

                            {

                                label:
                                    "Probability Density",

                                data:
                                    probabilityValues,

                                borderWidth: 1,

                                borderRadius: 6

                            }

                        ]

                    },

                    options: {

                        responsive: true,

                        maintainAspectRatio: false,

                        plugins: {

                            legend: {
                                labels: {
                                    color: "#cbd5e1"
                                }
                            }

                        },

                        scales: {

                            x: {

                                title: {
                                    display: true,
                                    text: "Battery (%)",
                                    color: "#94a3b8"
                                },

                                ticks: {
                                    color: "#94a3b8"
                                },

                                grid: {
                                    color:
                                        "rgba(148,163,184,0.08)"
                                }

                            },

                            y: {

                                title: {
                                    display: true,
                                    text:
                                        "Probability Density",
                                    color: "#94a3b8"
                                },

                                ticks: {
                                    color: "#94a3b8"
                                },

                                grid: {
                                    color:
                                        "rgba(148,163,184,0.08)"
                                }

                            }

                        }

                    }

                }
            );

        }

    }
);