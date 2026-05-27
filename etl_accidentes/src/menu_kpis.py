import pandas as pd
from src.db_connection import get_engine
import src.queries as q


def ejecutar_query(engine, query):

    with engine.connect() as conn:
        df = pd.read_sql(query, conn)

    print("\n📊 RESULTADO:\n")
    print(df)


def menu():

    engine = get_engine()

    while True:

        print("\n" + "=" * 50)
        print("📊 MENÚ DE KPIs")
        print("=" * 50)

        print("\n--- KPIs GENERALES ---")
        print("1. Accidentes por año")
        print("2. Accidentes por municipio")
        print("3. Accidentes por tipo de vehículo")
        print("4. Accidentes por gravedad")
        print("5. Accidentes por rango de años")
        print("6. Top 10 municipios")
        print("7. Accidentes por departamento")
        print("8. Accidentes por marca")

        print("\n--- KPIs CLIMÁTICOS ---")
        print("9. Accidentes con lluvia")
        print("10. Temperatura promedio en accidentes graves")
        print("11. Accidentes bajo lluvia fuerte")
        print("12. Humedad promedio")
        print("13. Velocidad promedio del viento en accidentes con muertos")

        print("\n0. Salir")

        opcion = input("\nSelecciona una opción: ")

        if opcion == "1":
            ejecutar_query(engine, q.accidentes_por_anio())

        elif opcion == "2":
            ejecutar_query(engine, q.accidentes_por_municipio())

        elif opcion == "3":
            ejecutar_query(engine, q.accidentes_por_vehiculo())

        elif opcion == "4":
            ejecutar_query(engine, q.accidentes_por_gravedad())

        elif opcion == "5":

            inicio = input("Año inicial: ")
            fin = input("Año final: ")

            ejecutar_query(
                engine,
                q.accidentes_por_rango_anios(inicio, fin)
            )

        elif opcion == "6":
            ejecutar_query(engine, q.top_municipios())

        elif opcion == "7":
            ejecutar_query(engine, q.accidentes_por_departamento())

        elif opcion == "8":
            ejecutar_query(engine, q.accidentes_por_marca())

        elif opcion == "9":
            ejecutar_query(engine, q.accidentes_con_lluvia())

        elif opcion == "10":
            ejecutar_query(engine, q.temperatura_promedio_graves())

        elif opcion == "11":
            ejecutar_query(engine, q.accidentes_lluvia_fuerte())

        elif opcion == "12":
            ejecutar_query(engine, q.humedad_promedio())

        elif opcion == "13":
            ejecutar_query(engine, q.viento_promedio_muertos())

        elif opcion == "0":
            print("\n👋 Saliendo...")
            break

        else:
            print("\n❌ Opción inválida")


if __name__ == "__main__":
    menu()