from flask import Flask, render_template, request, session, redirect, url_for
import pandas as pd
import re

app = Flask(__name__)
app.secret_key = 'Villomax'  # Clave secreta para la sesión

datos = pd.read_excel("datospersonales.xlsx")

def search_nombre(patron):
    datos[['Clave', 'Nombre', 'Correo', 'Telefono']] = datos[['Clave', 'Nombre', 'Correo', 'Telefono']].fillna('')
    coincidence = datos[datos['Nombre'].str.contains(patron, flags=re.IGNORECASE, regex=True)]
    return coincidence[['Clave', 'Nombre', 'Correo', 'Telefono']]

def verificar_credenciales(usuario, contrasena):
    return usuario == 'David' and contrasena == 'Pr!ncesa29'

@app.route('/')
def index():
    if 'usuario' in session:
        return render_template('Formulario.html')
    else:
        return redirect(url_for('login'))

@app.route('/index', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        contrasena = request.form['contrasena']
        if verificar_credenciales(usuario, contrasena):
            session['usuario'] = usuario
            return redirect(url_for('index'))
        else:
            return render_template('index.html', mensaje='Usuario o contraseña incorrectos')
    return render_template('index.html')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('usuario', None)
    return redirect(url_for('login'))

@app.route('/Lista', methods=['POST'])
def lista():
    searchnombres = request.form['nombre']
    result = search_nombre(searchnombres)
    if not result.empty:
        resultados = result.to_dict(orient='records')
    else:
        resultados = None
    return render_template('Formulario.html', resultados=resultados)

if __name__ == '__main__':
    app.run(debug=True)
