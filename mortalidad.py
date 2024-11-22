import pandas as pd
from flask import Blueprint, jsonify, request, render_template

mortalidad_bp = Blueprint("mortalidad", __name__, template_folder="templates")

# Ruta al archivo CSV
CSV_PATH = "data/births-and-deaths.csv"
data = pd.read_csv(CSV_PATH)

# Filtrar filas donde 'Code' no sea 'REG' (por regiones)
data = data[data["Code"] != "REG"]

# Filtrar filas donde 'Code' no sea 'OWID_WRL' (por conteo mundial)
mortalidad_data = data[data["Code"] != "OWID_WRL"]

mortalidad_data_full = data[["Entity", "Year", "Deaths"]]  # Para mantener datos completos

@mortalidad_bp.route('/mortalidad', methods=['GET'])
def mortalidad():
    paises = sorted(mortalidad_data["Entity"].unique())
    anios = sorted(mortalidad_data["Year"].unique())
    return render_template('mortalidad.html', paises=paises, anios=anios)

@mortalidad_bp.route('/mortalidad/grafico', methods=['POST'])
def mortalidad_grafico():
    content = request.get_json()
    pais = content.get("pais")
    anio = content.get("anio")

    if pais:
        # Filtrar datos por país
        filtered_data = mortalidad_data_full[mortalidad_data_full["Entity"] == pais]
        if filtered_data.empty:
            return jsonify({"error": f"No hay datos disponibles para {pais}."}), 404

        # Crear los datos del gráfico para el país
        years = filtered_data["Year"].tolist()
        deaths = filtered_data["Deaths"].tolist()

        graph_data = {
            "data": [
                {
                    "x": years,
                    "y": deaths,
                    "type": "scatter",
                    "mode": "lines+markers",
                    "name": f"Tasas de mortalidad en {pais}",
                    "line": {"color": "red"},
                }
            ],
            "layout": {
                "title": f"Mortalidad de {pais} a lo largo del tiempo",
                "xaxis": {"title": "Año"},
                "yaxis": {"title": "Muertes"},
            },
        }
    elif anio:
        # Filtrar datos por año y ordenar por muertes, sin contar "OWID_WRL"
        filtered_data = mortalidad_data[mortalidad_data["Year"] == int(anio)]
        if filtered_data.empty:
            return jsonify({"error": f"No hay datos disponibles para el año {anio}."}), 404

        sorted_data = filtered_data.sort_values("Deaths", ascending=False)

        # Crear los datos del gráfico para los países por año
        countries = sorted_data["Entity"].tolist()
        deaths = sorted_data["Deaths"].tolist()

        graph_data = {
            "data": [
                {
                    "x": countries,
                    "y": deaths,
                    "type": "bar",
                    "name": f"Mortalidad en {anio}",
                    "marker": {"color": "red"},
                }
            ],
            "layout": {
                "title": f"Mortalidad por países en {anio}",
                "xaxis": {"title": "País"},
                "yaxis": {"title": "Muertes"},
            },
        }
    else:
        return jsonify({"error": "No se especificó el país o el año."}), 400

    return jsonify(graph_data)
