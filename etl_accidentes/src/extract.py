import pandas as pd

# =========================
# ACCIDENTES
# =========================

def extract_accidents(path):
    print("\n[EXTRACT] Leyendo accidentes...")
    
    df = pd.read_csv(
        path,
        low_memory=False
    )

    print(f"✅ Accidentes cargados: {len(df):,} filas")
    return df


# =========================
# CLIMA
# =========================

def extract_climate(path):
    print("\n[EXTRACT] Leyendo datos climáticos...")

    df = pd.read_csv(
        path,
        low_memory=False
    )

    print(f"✅ Clima cargado: {len(df):,} filas")
    return df