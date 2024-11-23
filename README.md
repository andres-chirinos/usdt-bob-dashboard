# Historial de Precio del Dólar contra el Boliviano

## Descripción

Este proyecto busca almacenar y analizar información de las ofertas y el mercado respecto al precio del Dólar evaluado a través de USDT (Tether Dollar) y otras criptomonedas al Boliviano (BOB). El objetivo es encontrar el valor real del Boliviano en el mercado internacional y presentar los resultados en un dashboard interactivo.

## Autores

- **Andres Humberto Chirinos Lizondo**

  - Sociedad Científica de Estudiantes de Estadística - UMSA
  - Email: ahchirinos@umsa.bo
  - ORCID: 0009-0004-1628-6135

- **Kevin Barrientos Carrasco**
  - Universidad Mayor de San Andrés

## Estructura del Proyecto

- `index.qmd`: Documento principal que contiene la introducción, objetivos, hipótesis, materiales y métodos, resultados, discusión y conclusiones del estudio.
- `index.ipynb`: Notebook de Jupyter que contiene el código para procesar los datos y generar los gráficos interactivos.
- `publish.yml`: Archivo de configuración de GitHub Actions para automatizar la publicación del dashboard.

## Requisitos

- Python 3.10 o superior
- Librerías de Python:
  - `pandas`
  - `plotly`
  - `pytz`

## Instalación

1. Clona el repositorio:

   ```sh
   git clone https://github.com/tu_usuario/tu_repositorio.git
   cd tu_repositorio
   ```

2. Crea un entorno virtual y activa:

   ```sh
   python -m venv .venv
   .venv\Scripts\activate  # En Windows
   source .venv/bin/activate  # En macOS/Linux
   ```

3. Instala las dependencias:
   ```sh
   pip install -r requirements.txt
   ```

## Uso

1. Abre el notebook index.ipynb en Jupyter y ejecuta las celdas para procesar los datos y generar los gráficos interactivos.

2. Publica el dashboard utilizando GitHub Actions configurado en publish.yml.

## Contribución

¡Las contribuciones son bienvenidas! Para contribuir, sigue estos pasos:

1. Haz un fork del repositorio.
2. Crea una nueva rama (git checkout -b feature/nueva-funcionalidad).
3. Realiza tus cambios y haz commit (git commit -am 'Añadir nueva funcionalidad').
4. Sube tus cambios a tu fork (git push origin feature/nueva-funcionalidad).
5. Abre un Pull Request en el repositorio original.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT. Consulta el archivo LICENSE para más detalles.
