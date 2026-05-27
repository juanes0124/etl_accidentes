import great_expectations as gx


def validate_fact_table(df):

    print("\n[GX] Ejecutando validaciones de calidad...")

    errores = []

    # ======================
    # VALIDACIONES CRÍTICAS
    # ======================

    if df["tiempo_id"].isnull().sum() > 0:
        errores.append("tiempo_id contiene valores nulos")

    if df["ubicacion_id"].isnull().sum() > 0:
        errores.append("ubicacion_id contiene valores nulos")

    if df["vehiculo_id"].isnull().sum() > 0:
        errores.append("vehiculo_id contiene valores nulos")

    if df["gravedad_id"].isnull().sum() > 0:
        errores.append("gravedad_id contiene valores nulos")

    if len(df) == 0:
        errores.append("fact_accidentes está vacía")

    # ======================
    # VALIDACIONES CLIMA
    # ======================

    if "clima_id" in df.columns:

        if (
            df["clima_id"]
            .dropna()
            .astype(int)
            .lt(1)
            .any()
        ):
            errores.append(
                "clima_id contiene valores inválidos"
            )

    if "cantidad" in df.columns:

        if (df["cantidad"] < 0).any():
            errores.append(
                "cantidad contiene valores negativos"
            )

    # ======================
    # RESULTADO
    # ======================

    if errores:

        print("\n❌ VALIDACIÓN FALLIDA")

        for e in errores:
            print("-", e)

        raise Exception(
            "Pipeline detenido por errores críticos"
        )

    print("✅ Great Expectations superado")

    return True