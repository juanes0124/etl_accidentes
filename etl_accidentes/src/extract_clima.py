import pandas as pd

def extract_climate(path):

    print("\n[EXTRACT] Leyendo datos climáticos...")

    df = pd.read_csv(path)

    print(f"✅ Clima cargado: {len(df):,} filas")

    return df