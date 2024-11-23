# Proyecto Final - "Vitalytic"
_Autor del proyecto: Hugo González_

Vitalytic es un proyecto que proporciona una interfaz web para analizar la natalidad, la mortalidad y el crecimiento natural (diferencia entre natalidad y mortalidad) de diferentes países a lo largo de los años, mostrando datos reales aproximados entre los años 1950 y 2023, y desde el 2024 hasta 2100 seran datos sobre un posible escenario medio a futuro. El proyecto utiliza estos datos provenientes de un archivo CSV. La aplicación está desarrollada en Python utilizando Flask, Pandas y Plotly.

## Estructura del proyecto

```
Proyecto-Final-Paradigmas/ 
├── data/ 
│ └── births-and-deaths.csv "Archivo CSV con los datos necesarios"
├── templates/ 
│ ├── crecimiento_natural.html "Plantilla HTML de la seccion de crecimiento natural"
│ ├── index.html "Plantilla HTML de la pagina principal"
│ ├── mortalidad.html "Plantilla HTML de la seccion de mortalidad"
│ └── natalidad.html "Plantilla HTML de la seccion de natalidad"
├── static/
│ ├── background.gif "GIF usado para el fondo de la pagina"
│ └── style.css "Archivo de estilo"
├── crecimiento_natural.py "Logica sobre crecimiento natural"
├── main.py "Entrada principal de la aplicacion Flask"
├── mortalidad.py "Logica sobre mortalidad"
├── natalidad.py "Logica sobre natalidad"
└── README.md
```

## Requisitos para ejecutar el programa

- Python 3.12 o superior.
- Bibliotecas necesarias:
    - Flask
    - Pandas
    - Glob

## Instalacion

1. **Clonar el repositorio**
Para clonar el repositorio, se necesita iniciar el git en el terminal y clonar el repositorio, para esto, se usaran los siguientes comandos para tener el proyecto en tu editor de codigo favorito (en este caso, Visual Studio Code):
```
git init
git clone https://github.com/hxgoantonioo/Proyecto-Final-Paradigmas
cd Proyecto-Final-Paradigmas
```

2. **Instalar las bibliotecas**
En el mismo terminal, en caso de no tener las librerias instaladas, para instalar las bibliotecas usaremos el instalador de paquetes _pip_ con el siguiente comando.
```
pip install flask pandas
```

3. **Iniciar el programa _main.py_**
Para empezar a usar el programa, hay que iniciar el codigo en el archivo _main.py_ y el programa estara listo para usar. En caso de no saber, en el terminar se puede escribir el siguiente comando:
```
python main.py
python Proyecto-Final-Paradigmas\main.py "Solo en caso de no funcionar el primer comando"

```

## Uso
- Al iniciar el programa, se abrira un navegador web (o indicara un servidor tipo "http://127.0.0.1:5000/" en el terminal para acceder en caso de que no abra automaticamente) en el cual se encontrara la pagina principal, donde se pueden ver las tres secciones que se pueden explorar: _Crecimiento natural, natalidad y mortalidad_.
- Al seleccionar alguna de las secciones, se mostrara dos menus desplegables, en el primero se debe seleccionar el modo que se desea ver: 
    - En el modo **por pais** se veran todos los paises disponibles en el segundo menu desplegable, que al seleccionarlo y dar al boton _consultar_, se mostrara el grafico de todos los años con los datos reales aproximados y la proyeccion al futuro de escenario medio (1950-2100).
    - En el modo **por años** se veran todos los años entre los intervalos _1950-2100_, donde al elegir algun año y hacer la consulta, se pueden ver los paises ordenados de mayor a menor de la seccion elegida en un grafico.
- **OJO: Hay un pequeño error que no pudo ser resuelto. Pasa que al elegir uno de los modos la primera vez y elegir una de las opciones disponibles de ese modo, al darle consultar, no se mostrara el grafico, quedandose como una "consulta fantasma", para arreglar esto, simplemente si ya se hizo la consulta, al cambiar al otro modo, las consultas volveran a funcionar bien. Por ejemplo, si se desea ver el modo por pais, se debe hacer una consulta en el modo por año (seleccionar el modo y alguno de los años), darle a consultar y no se mostrara nada, de ahi cambiar al modo por pais, y funcionara correctamente, y viceversa para el otro caso. Esto sucede en las tres secciones lamentablemente.** [Video del error mencionado](error.mp4)

Espero sea agradable la experiencia con el proyecto, muchas gracias por leer. :)