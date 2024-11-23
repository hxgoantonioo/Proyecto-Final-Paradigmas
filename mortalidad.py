import pandas as pd
from flask import Blueprint, jsonify, request, render_template
import glob

class Mortalidad:
    def __init__(self, csv_path):
        self.data = pd.read_csv(csv_path)

        # Filtrar datos
        self.data = self.data[self.data["Code"] != "REG"]  # Eliminar regiones
        self.mortalidad_data = self.data[self.data["Code"] != "OWID_WRL"]  # Eliminar conteo mundial
        self.mortalidad_data_full = self.data[["Entity", "Year", "Deaths"]]

    def obtener_paises(self):
        """Devuelve la lista de países únicos en orden alfabético."""
        return sorted(self.mortalidad_data["Entity"].unique())

    def obtener_anios(self):
        """Devuelve la lista de años únicos en orden ascendente."""
        return sorted(self.mortalidad_data["Year"].unique())

    def filtrar_por_pais(self, pais):
        """Filtra los datos por país."""
        return self.mortalidad_data_full[self.mortalidad_data_full["Entity"] == pais]

    def filtrar_por_anio(self, anio):
        """Filtra los datos por año."""
        return self.mortalidad_data[self.mortalidad_data["Year"] == int(anio)]


# Crear un objeto para manejar los datos de mortalidad
csv_files = glob.glob('**/births-and-deaths.csv', recursive=True)
csv_path = csv_files[0]
mortalidad_manager = Mortalidad(csv_path)

# Crear el Blueprint de Flask
mortalidad_bp = Blueprint("mortalidad", __name__, template_folder="templates")

@mortalidad_bp.route('/mortalidad', methods=['GET'])
def mortalidad():
    """Renderiza la página principal de consulta de mortalidad."""
    paises = mortalidad_manager.obtener_paises()
    anios = mortalidad_manager.obtener_anios()
    return render_template('mortalidad.html', paises=paises, anios=anios)

@mortalidad_bp.route('/mortalidad/grafico', methods=['POST'])
def mortalidad_grafico():
    """Devuelve los datos del gráfico según el país o año seleccionado."""
    content = request.get_json()
    pais = content.get("pais")
    anio = content.get("anio")

    if pais:
        filtered_data = mortalidad_manager.filtrar_por_pais(pais)
        if filtered_data.empty:
            return jsonify({"error": f"No hay datos disponibles para {pais}."}), 404

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
        filtered_data = mortalidad_manager.filtrar_por_anio(anio)
        if filtered_data.empty:
            return jsonify({"error": f"No hay datos disponibles para el año {anio}."}), 404

        sorted_data = filtered_data.sort_values("Deaths", ascending=False)
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
