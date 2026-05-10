import pandas as pd
import subprocess
from utils.drift_detector import compare_datasets

# Load reference (training) data
reference_df = pd.read_csv("risk_data.csv")

# Simulate current production data by slightly shifting the data
current_df = reference_df.copy()

# Introduce artificial drift in one numeric column
numeric_cols = current_df.select_dtypes(include=["number"]).columns
if len(numeric_cols) > 0:
    current_df[numeric_cols[0]] = current_df[numeric_cols[0]] * 1.5

# Run drift detection
results = compare_datasets(reference_df, current_df)

print("\n📊 Drift Detection Results\n")

drift_found = False

for column, result in results.items():
    status = "⚠️ Drift Detected" if result["drift_detected"] else "✅ No Drift"
    print(
        f"{column}: {status} "
        f"(p-value = {result['p_value']:.6f})"
    )

    if result["drift_detected"]:
        drift_found = True

# Trigger retraining if any drift detected
if drift_found:
    print("\n🚨 Data drift detected! Triggering retraining...\n")
    subprocess.run(["python", "scripts/retrain.py"])
else:
    print("\n✅ No significant drift detected.")
    