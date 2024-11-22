import pandas as pd
from flask import Blueprint, jsonify, request, render_template

crecimiento_bp = Blueprint("crecimiento", __name__, template_folder="templates")

# Ruta al archivo CSV
CSV_PATH = "data/births-and-deaths.csv"
data = pd.read_csv(CSV_PATH)

# Filtrar filas donde 'Code' no sea 'REG' (por regiones)
data = data[data["Code"] != "REG"]

# Filtrar filas donde 'Code' no sea 'OWID_WRL' (por conteo mundial)
crecimiento_data = data[data["Code"] != "OWID_WRL"]

crecimiento_data_full = data[["Entity", "Year", "Births", "Deaths"]]  # Para mantener datos completos

@crecimiento_bp.route('/crecimiento', methods=['GET'])
def crecimiento():
    paises = sorted(crecimiento_data["Entity"].unique())
    anios = sorted(crecimiento_data["Year"].unique())
    return render_template('crecimiento_natural.html', paises=paises, anios=anios)

@crecimiento_bp.route('/crecimiento/grafico', methods=['POST'])
def crecimiento_grafico():
    content = request.get_json()
    pais = content.get("pais")
    anio = content.get("anio")

    if pais:
        # Filtrar datos por país
        filtered_data = crecimiento_data_full[crecimiento_data_full["Entity"] == pais]
        if filtered_data.empty:
            return jsonify({"error": f"No hay datos disponibles para {pais}."}), 404

        # Calcular el crecimiento natural (births - deaths)
        filtered_data["Crecimiento Natural"] = filtered_data["Births"] - filtered_data["Deaths"]

        years = filtered_data["Year"].tolist()
        crecimiento_natural = filtered_data["Crecimiento Natural"].tolist()

        # Crear los datos del gráfico para el país
        graph_data = {
            "data": [
                {
                    "x": years,
                    "y": crecimiento_natural,
                    "type": "scatter",
                    "mode": "lines+markers",
                    "name": f"Crecimiento Natural en {pais}",
                    "line": {"color": "green"},
                }
            ],
            "layout": {
                "title": f"Crecimiento Natural en {pais} a lo largo del tiempo",
                "xaxis": {"title": "Año"},
                "yaxis": {"title": "Crecimiento Natural (Births - Deaths)"},
            },
        }
    elif anio:
        # Filtrar datos por año y calcular crecimiento natural
        filtered_data = crecimiento_data_full[crecimiento_data_full["Year"] == int(anio)]
        if filtered_data.empty:
            return jsonify({"error": f"No hay datos disponibles para el año {anio}."}), 404

        # Calcular el crecimiento natural (births - deaths)
        filtered_data["Crecimiento Natural"] = filtered_data["Births"] - filtered_data["Deaths"]

        sorted_data = filtered_data.sort_values("Crecimiento Natural", ascending=False)

        # Crear los datos del gráfico para los países por año
        countries = sorted_data["Entity"].tolist()
        crecimiento_natural = sorted_data["Crecimiento Natural"].tolist()

        graph_data = {
            "data": [
                {
                    "x": countries,
                    "y": crecimiento_natural,
                    "type": "bar",
                    "name": f"Crecimiento Natural en {anio}",
                    "marker": {"color": "green"},
                }
            ],
            "layout": {
                "title": f"Crecimiento Natural por países en {anio}",
                "xaxis": {"title": "País"},
                "yaxis": {"title": "Crecimiento Natural (Births - Deaths)"},
            },
        }
    else:
        return jsonify({"error": "No se especificó el país o el año."}), 400

    return jsonify(graph_data)
