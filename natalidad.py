import pandas as pd
from flask import Blueprint, jsonify, request, render_template

natalidad_bp = Blueprint("natalidad", __name__, template_folder="templates")

# Ruta al archivo CSV
CSV_PATH = "data/births-and-deaths.csv"
data = pd.read_csv(CSV_PATH)

# Filtrar filas donde 'Code' no sea 'REG' (por regiones)
data = data[data["Code"] != "REG"]

# Filtrar filas donde 'Code' no sea 'OWID_WRL' (por conteo mundial)
natalidad_data = data[data["Code"] != "OWID_WRL"]

natalidad_data_full = data[["Entity", "Year", "Births"]]  # Para mantener datos completos

@natalidad_bp.route('/natalidad', methods=['GET'])
def natalidad():
    paises = sorted(natalidad_data["Entity"].unique())
    anios = sorted(natalidad_data["Year"].unique())
    return render_template('natalidad.html', paises=paises, anios=anios)

@natalidad_bp.route('/natalidad/grafico', methods=['POST'])
def natalidad_grafico():
    content = request.get_json()
    pais = content.get("pais")
    anio = content.get("anio")

    if pais:
        # Filtrar datos por país
        filtered_data = natalidad_data_full[natalidad_data_full["Entity"] == pais]
        if filtered_data.empty:
            return jsonify({"error": f"No hay datos disponibles para {pais}."}), 404

        # Crear los datos del gráfico para el país
        years = filtered_data["Year"].tolist()
        births = filtered_data["Births"].tolist()

        graph_data = {
            "data": [
                {
                    "x": years,
                    "y": births,
                    "type": "scatter",
                    "mode": "lines+markers",
                    "name": f"Tasas de natalidad en {pais}",
                    "line": {"color": "blue"},
                }
            ],
            "layout": {
                "title": f"Natalidad de {pais} a lo largo del tiempo",
                "xaxis": {"title": "Año"},
                "yaxis": {"title": "Nacimientos"},
            },
        }
    elif anio:
        # Filtrar datos por año y ordenar por nacimientos, sin contar "OWID_WRL"
        filtered_data = natalidad_data[natalidad_data["Year"] == int(anio)]
        if filtered_data.empty:
            return jsonify({"error": f"No hay datos disponibles para el año {anio}."}), 404

        sorted_data = filtered_data.sort_values("Births", ascending=False)

        # Crear los datos del gráfico para los países por año
        countries = sorted_data["Entity"].tolist()
        births = sorted_data["Births"].tolist()

        graph_data = {
            "data": [
                {
                    "x": countries,
                    "y": births,
                    "type": "bar",
                    "name": f"Natalidad en {anio}",
                    "marker": {"color": "blue"},
                }
            ],
            "layout": {
                "title": f"Natalidad por países en {anio}",
                "xaxis": {"title": "País"},
                "yaxis": {"title": "Nacimientos"},
            },
        }
    else:
        return jsonify({"error": "No se especificó el país o el año."}), 400

    return jsonify(graph_data)
