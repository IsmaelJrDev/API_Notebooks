from flask import Flask, render_template
from nbconvert import HTMLExporter
import nbformat
import os

app = Flask(__name__, template_folder='view', static_folder='view/css')

# Ruta que lista todos los notebooks disponibles
@app.route('/')
def index():
    NOTEBOOKS_DIR = 'notebooks'
    # Obtener los nombres de los notebooks y ordenarlos alfabéticamente
    notebooks = sorted([f.replace('.ipynb', '') for f in os.listdir(NOTEBOOKS_DIR) if f.endswith('.ipynb')])
    return render_template('index.html', notebooks=notebooks)

# Ruta para ver un notebook específico
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
                <link rel="stylesheet" type="text/css" href="{resources['output_files']['stylesheet']}">
            </head>
            <body>
                {body}
            </body>
        </html>
        """

        return complete_html

    except Exception as e:
        return f"<p>ERROR: {str(e)}</p>", 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)