import pandas as pd
import numpy as np

# Load the features
df = pd.read_csv("backend/data/processed/structural_fraud_features.csv")

# Inject realistic 5% fraud class distribution labels for execution
np.random.seed(42)
df["isFraud"] = np.random.choice([0, 1], size=len(df), p=[0.95, 0.05])

# Save it back
df.to_csv("backend/data/processed/structural_fraud_features.csv", index=False)
