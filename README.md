# Colombo Rain Ensemble Dashboard

This Streamlit app compares the held-out results for a majority baseline, bagging, gradient boosting, and stacking. It reads the scores and confusion matrices exported from the companion Colab notebook. Training and evaluation run in Colab. The app presents the exported results.

## Export your Colab run

1. Open your existing Colombo rain notebook in Colab.
2. Add a code cell below the dashboard and paste the contents of `colab_export.py` into it.
3. Run all cells. The export cell downloads `results.json`. If the download does not start, open Colab's Files pane, find `results.json`, and download it there.
4. Put your downloaded `results.json` next to `app.py`, replacing the included reference snapshot. Verify the scores against your notebook.

## Deploy

1. Create a GitHub repository, for example `colombo-rain-dashboard`. Upload the individual files at the repository root and commit them.
2. Sign in at [Streamlit Community Cloud](https://share.streamlit.io/) with GitHub and choose **Create app → Yup, I have an app**.
3. Select your repository, your branch (usually `main`), and `app.py` as the main file path. Choose **Deploy**.
4. Open the Streamlit URL and switch between models. Check the selected model's error counts against Colab. If sharing publicly, confirm that the link opens in a private browser window.

[Streamlit deployment documentation](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy)

## Run locally

From the folder with `app.py` and `results.json`:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

## Dataset and attribution

[ECMWF ERA5 historical weather data via the Open-Meteo Historical Weather API](https://open-meteo.com/en/docs/historical-weather-api), requested for the Colombo area.

OpenAI ChatGPT generated the starter dashboard and the Colab export code. Add the AI reference details required by your course and describe your own modifications and verification in the submission notebook.
