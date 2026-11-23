# AI attribution: OpenAI ChatGPT generated this results export cell.
from pathlib import Path
import json

results = {
    "start_date": str(test["target_date"].min().date()),
    "end_date": str(test["target_date"].max().date()),
    "test_days": int(len(test)),
    "rain_cutoff_mm": float(RAIN_CUTOFF_MM),
    "scores": {
        model: {metric: float(value) for metric, value in metrics.items()}
        for model, metrics in scores.to_dict(orient="index").items()
    },
    "matrices": {model: matrix.tolist() for model, matrix in matrices.items()},
}

results_file = Path("results.json")
results_file.write_text(json.dumps(results, indent=2, allow_nan=False), encoding="utf-8")
print(f"Exported {len(results['scores'])} models evaluated on {results['test_days']} test days.")

from google.colab import files
files.download(str(results_file))
