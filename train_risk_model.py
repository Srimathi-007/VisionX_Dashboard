import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib

dataset_name = "labeled_flight_telemetry.csv"

try:
    df = pd.read_csv(dataset_name)
    print(f"✅ {dataset_name} loaded.")
    
    # Force print what columns are actually inside your file
    print("📢 Your CSV Columns are:", list(df.columns))
    
    # Lowercase stripping engine to map columns robustly
    col_mapping = {str(c).lower().strip(): c for c in df.columns}
    
    accel_col = next((col_mapping[k] for k in col_mapping if 'accel' in k), None)
    alt_col = next((col_mapping[k] for k in col_mapping if 'alt' in k), None)
    bat_col = next((col_mapping[k] for k in col_mapping if 'bat' in k or 'volt' in k), None)
    state_col = next((col_mapping[k] for k in col_mapping if 'state' in k or 'risk' in k or 'label' in k), None)
    
    if not (accel_col and alt_col and bat_col):
        # Fallback to index positions if names mismatch completely
        print("⚠️ Exact names mismatch. Mapping by column sequence indices [0, 1, 2]...")
        accel_col, alt_col, bat_col = df.columns[0], df.columns[1], df.columns[2]
        
    print(f"🎯 Mapped Columns -> Accel: '{accel_col}', Altitude: '{alt_col}', Battery: '{bat_col}'")
    
    df = df.rename(columns={accel_col: 'Accel', alt_col: 'Altitude', bat_col: 'Battery'})
    if state_col:
        df = df.rename(columns={state_col: 'Risk_State'})

except Exception as e:
    print(f"⚠️ Creating fallback matrix: {e}")
    np.random.seed(42)
    df = pd.DataFrame({
        'Accel': np.random.normal(1.0, 0.2, 100),
        'Altitude': np.random.uniform(10, 500, 100),
        'Battery': np.random.uniform(3.5, 4.2, 100),
        'Risk_State': np.random.choice([0, 1, 2, 3], size=100)
    })

if 'Risk_State' not in df.columns:
    df['Risk_State'] = 0
    df.loc[df['Accel'] > 2.5, 'Risk_State'] = 1
    df.loc[df['Altitude'] < 20, 'Risk_State'] = 2
    df.loc[df['Battery'] < 3.4, 'Risk_State'] = 3

X = df[['Accel', 'Altitude', 'Battery']]
y = df['Risk_State']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y if len(np.unique(y)) > 1 else None)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

model = RandomForestClassifier(n_estimators=50, max_depth=8, random_state=42)
model.fit(X_train_scaled, y_train)

y_pred = model.predict(X_test_scaled)
print("\n=== 🛸 TEAM VISIONX ML RISK MATRIX REPORT ===")
print(classification_report(y_test, y_pred, zero_division=0))

joblib.dump(model, 'visionx_risk_model.pkl')
joblib.dump(scaler, 'visionx_scaler.pkl')
print("\n🎉 Model weights mapped safely to 'visionx_risk_model.pkl'")
