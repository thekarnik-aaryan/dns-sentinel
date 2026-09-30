import os, joblib, numpy as np, pandas as pd
from sklearn.ensemble import IsolationForest

def train_and_save():
    np.random.seed(42)
    df = pd.DataFrame({
        "domain_length": np.random.randint(8, 22, size=1000),
        "subdomain_length": np.random.choice([0, 3, 5], size=1000),
        "entropy": np.random.normal(3.1, 0.4, size=1000),
        "digit_ratio": np.random.beta(0.5, 5, size=1000),
        "unique_character_ratio": np.random.uniform(0.3, 0.6, size=1000),
        "query_frequency": np.random.poisson(3, size=1000),
        "nxdomain_frequency": np.random.beta(0.1, 5, size=1000)
    })
    model = IsolationForest(n_estimators=100, contamination=0.03, random_state=42)
    model.fit(df)
    out_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../ml/models"))
    os.makedirs(out_dir, exist_ok=True)
    joblib.dump(model, os.path.join(out_dir, "isolation_forest.joblib"))
    print("ML model trained and saved successfully!")

if __name__ == "__main__": train_and_save()
