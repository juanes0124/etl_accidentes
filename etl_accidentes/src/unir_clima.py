import pandas as pd
from pathlib import Path

base_path = Path("data/clima/raw")

variables_data = {
    "hum_relativa": [],
    "precipitacion": [],
    "temperatura": [],
    "vel_viento": []
}

for file in base_path.rglob("*.csv"):

    print(f"✅ Archivo leído: {file.name}")

    df = pd.read_csv(file)

    nombre = file.name.lower()

    if "humedad" in nombre:
        variable = "hum_relativa"

    elif "precipitacion" in nombre:
        variable = "precipitacion"

    elif "temperatura" in nombre:
        variable = "temperatura"

    elif "viento" in nombre:
        variable = "vel_viento"

    else:
        continue

    df = df[["departamento", "fecha", "valor"]].copy()

    df = (
        df.groupby(["departamento", "fecha"], as_index=False)
        .mean(numeric_only=True)
    )

    df = df.rename(columns={"valor": variable})

    variables_data[variable].append(df)

# unir todos los departamentos de cada variable
for variable in variables_data:

    variables_data[variable] = pd.concat(
        variables_data[variable],
        ignore_index=True
    )

# dataframe base
clima_final = variables_data["hum_relativa"]

# unir variables
for variable in ["precipitacion", "temperatura", "vel_viento"]:

    clima_final = clima_final.merge(
        variables_data[variable],
        on=["departamento", "fecha"],
        how="outer"
    )

clima_final = clima_final.drop_duplicates()

clima_final = clima_final.sort_values(
    ["departamento", "fecha"]
)

output_path = "data/clima/processed/clima_unificado.csv"

clima_final.to_csv(output_path, index=False)

print("\n🔥 clima_unificado.csv generado correctamente")
print(clima_final.head())

print("\nDepartamentos encontrados:")
print(clima_final["departamento"].unique())