import pandas as pd
from flask import Blueprint, jsonify, request, render_template
import glob

class CrecimientoNatural:
    def __init__(self, csv_path):
        self.data = pd.read_csv(csv_path)
        self.data = self.data[self.data["Code"] != "REG"]
        self.data = self.data[self.data["Code"] != "OWID_WRL"]
        self.data["Growth"] = self.data["Births"] - self.data["Deaths"]
        self.crecimiento_data_full = self.data[["Entity", "Year", "Growth"]]

    def obtener_paises(self):
        return sorted(self.data["Entity"].unique())

    def obtener_anios(self):
        return sorted(self.data["Year"].unique())

    def filtrar_por_pais(self, pais):
        return self.crecimiento_data_full[self.crecimiento_data_full["Entity"] == pais]

    def filtrar_por_anio(self, anio):
        return self.crecimiento_data_full[self.crecimiento_data_full["Year"] == int(anio)]

csv_files = glob.glob('**/births-and-deaths.csv', recursive=True)
csv_path = csv_files[0]
crecimiento_manager = CrecimientoNatural(csv_path)

crecimiento_bp = Blueprint("crecimiento_natural", __name__, template_folder="templates")

@crecimiento_bp.route('/crecimiento', methods=['GET'])
def crecimiento():
    """Renderiza la página principal de consulta de crecimiento natural."""
    paises = crecimiento_manager.obtener_paises()
    anios = crecimiento_manager.obtener_anios()
    return render_template('crecimiento_natural.html', paises=paises, anios=anios)

@crecimiento_bp.route('/crecimiento/grafico', methods=['POST'])
def crecimiento_grafico():
    """Devuelve los datos del gráfico según el país o año seleccionado."""
    content = request.get_json()
    pais = content.get("pais")
    anio = content.get("anio")

    if pais:
        filtered_data = crecimiento_manager.filtrar_por_pais(pais)
        if filtered_data.empty:
            return jsonify({"error": f"No hay datos disponibles para {pais}."}), 404

        years = filtered_data["Year"].tolist()
        growth = filtered_data["Growth"].tolist()

        graph_data = {
            "data": [
                {
                    "x": years,
                    "y": growth,
                    "type": "scatter",
                    "mode": "lines+markers",
                    "name": f"Crecimiento natural en {pais}",
                    "line": {"color": "sky blue"},
                }
            ],
            "layout": {
                "title": f"Crecimiento natural de {pais} a lo largo del tiempo",
                "xaxis": {"title": "Año"},
                "yaxis": {"title": "Crecimiento natural (Nacimientos - Muertes)"},
            },
        }
    elif anio:
        filtered_data = crecimiento_manager.filtrar_por_anio(anio)
        if filtered_data.empty:
            return jsonify({"error": f"No hay datos disponibles para el año {anio}."}), 404

        sorted_data = filtered_data.sort_values("Growth", ascending=False)
        countries = sorted_data["Entity"].tolist()
        growth = sorted_data["Growth"].tolist()

        graph_data = {
            "data": [
                {
                    "x": countries,
                    "y": growth,
                    "type": "bar",
                    "name": f"Crecimiento natural en {anio}",
                    "marker": {"color": "sky blue"},
                }
            ],
            "layout": {
                "title": f"Crecimiento natural por países en {anio}",
                "xaxis": {"title": "País"},
                "yaxis": {"title": "Crecimiento natural (Nacimientos - Muertes)"},
            },
        }
    else:
        return jsonify({"error": "No se especificó el país o el año."}), 400

    return jsonify(graph_data)
