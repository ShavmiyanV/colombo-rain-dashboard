"""Display held-out Colombo rain experiment results exported from Colab.

AI attribution: OpenAI ChatGPT generated this dashboard code.
"""
import json
from pathlib import Path

import plotly.graph_objects as go
import streamlit as st

METRICS = ("Accuracy", "Precision", "Recall", "F1")
COLORS = ("#276174", "#B76931", "#188577", "#7457A8")
RESULTS_FILE = Path(__file__).with_name("results.json")

st.set_page_config(page_title="Colombo Rain | Ensemble Dashboard", layout="wide")
st.title("Next-day rain in Colombo")

try:
    results = json.loads(RESULTS_FILE.read_text(encoding="utf-8"))
    scores = results["scores"]
    matrices = results["matrices"]
    test_days = results["test_days"]
    start_date = results["start_date"]
    end_date = results["end_date"]
    rain_cutoff = results["rain_cutoff_mm"]

    if not scores or scores.keys() != matrices.keys():
        raise ValueError("The model names in the metrics and matrices must match.")
    for model, values in scores.items():
        if any(not 0 <= values[metric] <= 1 for metric in METRICS):
            raise ValueError(f"The scores for {model} must be between zero and one.")
        matrix = matrices[model]
        if len(matrix) != 2 or any(len(row) != 2 for row in matrix):
            raise ValueError(f"The confusion matrix for {model} must have two rows and two columns.")
        if sum(map(sum, matrix)) != test_days:
            raise ValueError(f"The confusion matrix for {model} must account for every test day.")
except (OSError, KeyError, TypeError, ValueError) as exc:
    st.error("Upload a fresh results.json exported from the Colab notebook. See README.md for the export steps.")
    st.caption(str(exc))
    st.stop()

st.caption(f"Held-out results · {start_date} to {end_date} · {test_days:,} days · Rain ≥ {rain_cutoff:g} mm")
models = list(scores)
comparison, error_view = st.columns([3, 2], gap="large")

with comparison:
    st.subheader("Compare models")
    chart = go.Figure()
    for metric, color in zip(METRICS, COLORS):
        chart.add_bar(
            name=metric,
            x=models,
            y=[scores[model][metric] for model in models],
            marker_color=color,
            hovertemplate="%{x}<br>" + metric + " %{y:.1%}<extra></extra>",
        )
    chart.update_layout(
        barmode="group",
        height=380,
        margin=dict(l=8, r=8, t=4, b=45),
        legend=dict(orientation="h", y=-0.22),
        yaxis=dict(title="Score", range=[0, 1.03], tickformat=".0%"),
    )
    st.plotly_chart(chart, width="stretch", config={"displayModeBar": False})
    rows = [
        {"Model": model, **{metric: f"{scores[model][metric]:.2%}" for metric in METRICS}}
        for model in models
    ]
    st.dataframe(rows, hide_index=True, width="stretch")

with error_view:
    st.subheader("Inspect prediction errors")
    selected = st.selectbox("Model", models, index=models.index("Stacking") if "Stacking" in models else 0)
    matrix = matrices[selected]
    missed, alarms = st.columns(2)
    missed.metric("Missed rainy days", matrix[1][0])
    alarms.metric("False alarms", matrix[0][1])

    labels = [f"Below {rain_cutoff:g} mm", f"At least {rain_cutoff:g} mm"]
    heatmap = go.Figure(
        go.Heatmap(
            x=labels,
            y=labels,
            z=matrix,
            text=matrix,
            texttemplate="%{text}",
            zmin=0,
            zmax=max(max(row) for values in matrices.values() for row in values),
            colorscale="Blues",
            showscale=False,
            hovertemplate="Actual: %{y}<br>Predicted: %{x}<br>Days: %{z}<extra></extra>",
        )
    )
    heatmap.update_layout(
        height=300,
        margin=dict(l=4, r=4, t=5, b=5),
        xaxis_title="Predicted",
        yaxis_title="Actual",
        yaxis_autorange="reversed",
    )
    st.plotly_chart(heatmap, width="stretch", config={"displayModeBar": False})

st.divider()
st.caption(
    "Model evaluation from Google Colab · "
    "[Weather source: ECMWF ERA5 via Open-Meteo](https://open-meteo.com/en/docs/historical-weather-api)"
)
