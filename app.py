from flask import Flask, render_template
from nbconvert import HTMLExporter
import nbformat
import os

app = Flask(__name__, template_folder='view', static_folder='view')

# Ruta que lista todos los notebooks disponibles
@app.route('/')
def index():
    NOTEBOOKS_DIR = 'notebooks'
    # Obtener los nombres de los notebooks y ordenarlos alfabéticamente
    notebooks = sorted([f.replace('.ipynb', '') for f in os.listdir(NOTEBOOKS_DIR) if f.endswith('.ipynb')])
    return render_template('index.html', notebooks=notebooks)

@app.route('/notebook/<notebook_name>')
def view_notebook(notebook_name):
    notebook_path = os.path.join('notebooks', notebook_name + '.ipynb')
    
    if not os.path.exists(notebook_path):
        return "Notebook no encontrado", 404

    try:
        # Leer el archivo notebook
        with open(notebook_path, 'r', encoding='utf-8') as file:
            notebook_content = nbformat.read(file, as_version=4)

        # Usar nbconvert para convertir el notebook a HTML
        html_exporter = HTMLExporter()
        body, resources = html_exporter.from_notebook_node(notebook_content)

        # Incluir los recursos necesarios (como CSS)
        resources['output_files'] = {
            'stylesheet': 'https://cdnjs.cloudflare.com/ajax/libs/jupyter-notebook/5.7.8/css/notebook.min.css',
        }

        # Crear el HTML completo con los recursos de Jupyter Notebook
        complete_html = f"""
        <html>
            <head>
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <link rel="stylesheet" type="text/css" href="{resources['output_files']['stylesheet']}">
                <style>
                    pre {{
                        background-color: #f5f5f5;
                        padding: 10px;
                        border-radius: 5px;
                        overflow-x: auto;
                    }}

                    code {{
                        font-family: Consolas, Monaco, monospace;
                        font-size: 1rem;
                    }}

                    body {{
                        font-family: Arial, sans-serif;
                        margin: 0;
                        padding: 0;
                        display: flex;
                        flex-direction: column;
                        min-height: 100vh;  /* Asegura que el contenido ocupe toda la altura de la página */
                    }}

                    .container {{
                        flex-grow: 1; /* Hace que el contenedor principal ocupe el espacio disponible */
                        padding: 20px;
                    }}

                    footer {{
                        background-color: #333;
                        color: white;
                        text-align: center;
                        padding: 10px 0;
                        position: relative;
                        width: 100%;
                        bottom: 0;
                        margin-top: auto;
                    }}

                    footer p {{
                        margin: 0;
                        font-size: 14px;
                    }}

                    .back-button {{
                        display: inline-block;
                        padding: 10px 20px;
                        background-color: #007bff;
                        color: white;
                        text-decoration: none;
                        border-radius: 5px;
                        font-size: 16px;
                        margin-bottom: 20px;
                    }}

                    .back-button:hover {{
                        background-color: #0056b3;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <a href="/" class="back-button">Regresar</a>
                    {body}
                </div>
                <footer>
                    <p class="copy"> ISIC - 3501 &copy; 2025 - Ismael</p>
                </footer>
            </body>
        </html>

        """

        return complete_html

    except Exception as e:
        return f"<p>ERROR: {str(e)}</p>", 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
