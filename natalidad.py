import pandas as pd
from flask import Blueprint, jsonify, request, render_template
import glob

class Natalidad:
    def __init__(self, csv_path):
        self.data = pd.read_csv(csv_path)

        # Filtrar datos
        self.data = self.data[self.data["Code"] != "REG"]  # Eliminar regiones
        self.natalidad_data = self.data[self.data["Code"] != "OWID_WRL"]  # Eliminar conteo mundial
        self.natalidad_data_full = self.data[["Entity", "Year", "Births"]]

    def obtener_paises(self):
        """Devuelve la lista de países únicos en orden alfabético."""
        return sorted(self.natalidad_data["Entity"].unique())

    def obtener_anios(self):
        """Devuelve la lista de años únicos en orden ascendente."""
        return sorted(self.natalidad_data["Year"].unique())

    def filtrar_por_pais(self, pais):
        """Filtra los datos por país."""
        return self.natalidad_data_full[self.natalidad_data_full["Entity"] == pais]

    def filtrar_por_anio(self, anio):
        """Filtra los datos por año."""
        return self.natalidad_data[self.natalidad_data["Year"] == int(anio)]


# Crear un objeto para manejar los datos de natalidad
csv_files = glob.glob('**/births-and-deaths.csv', recursive=True)
csv_path = csv_files[0]
natalidad_manager = Natalidad(csv_path)

# Crear el Blueprint de Flask
natalidad_bp = Blueprint("natalidad", __name__, template_folder="templates")

@natalidad_bp.route('/natalidad', methods=['GET'])
def natalidad():
    """Renderiza la página principal de consulta de natalidad."""
    paises = natalidad_manager.obtener_paises()
    anios = natalidad_manager.obtener_anios()
    return render_template('natalidad.html', paises=paises, anios=anios)

@natalidad_bp.route('/natalidad/grafico', methods=['POST'])
def natalidad_grafico():
    """Devuelve los datos del gráfico según el país o año seleccionado."""
    content = request.get_json()
    pais = content.get("pais")
    anio = content.get("anio")

    if pais:
        filtered_data = natalidad_manager.filtrar_por_pais(pais)
        if filtered_data.empty:
            return jsonify({"error": f"No hay datos disponibles para {pais}."}), 404

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
                    "line": {"color": "green"},
                }
            ],
            "layout": {
                "title": f"Natalidad de {pais} a lo largo del tiempo",
                "xaxis": {"title": "Año"},
                "yaxis": {"title": "Nacimientos"},
            },
        }
    elif anio:
        filtered_data = natalidad_manager.filtrar_por_anio(anio)
        if filtered_data.empty:
            return jsonify({"error": f"No hay datos disponibles para el año {anio}."}), 404

        sorted_data = filtered_data.sort_values("Births", ascending=False)
        countries = sorted_data["Entity"].tolist()
        births = sorted_data["Births"].tolist()

        graph_data = {
            "data": [
                {
                    "x": countries,
                    "y": births,
                    "type": "bar",
                    "name": f"Natalidad en {anio}",
                    "marker": {"color": "green"},
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
