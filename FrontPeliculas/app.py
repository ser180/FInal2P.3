from flask import Flask, render_template, request, redirect, url_for, flash
import requests

app = Flask(__name__)
app.secret_key = 'clave_secreta'

API_URL = "http://localhost:5000/peliculas"

@app.route('/')
def index():
    try:
        response = requests.get(API_URL)
        peliculas = response.json()
        return render_template('index.html', peliculas=peliculas)
    except Exception as e:
        flash(f"Error al conectar con la API: {e}", "danger")
        return render_template('index.html', peliculas=[])

@app.route('/buscar')
def buscar():
    titulo = request.args.get('titulo')
    if titulo:
        res = requests.get(f"{API_URL}/{titulo}")
        if res.status_code == 200:
            pelicula = res.json()
            return render_template('index.html', peliculas=[pelicula])
        else:
            flash("Película no encontrada.", "warning")
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))

@app.route('/agregar', methods=['GET', 'POST'])
def agregar():
    if request.method == 'POST':
        data = {
            "Titulo": request.form['Titulo'],
            "Genero": request.form['Genero'],
            "año": int(request.form['año']),
            "Clasificacion": request.form['Clasificacion']
        }
        res = requests.post(API_URL + '/', json=data)
        if res.status_code == 200 or res.status_code == 201:
            flash("Película agregada correctamente.", "success")
            return redirect(url_for('index'))
        else:
            flash(f"Error: {res.json().get('detail', res.text)}", "danger")
    return render_template('agregar.html')

@app.route('/detalle/<string:titulo>')
def detalle(titulo):
    res = requests.get(f"{API_URL}/{titulo}")
    if res.status_code == 200:
        return render_template('detalle.html', pelicula=res.json())
    else:
        flash("Película no encontrada.", "danger")
        return redirect(url_for('index'))

@app.route('/editar/<string:titulo>', methods=['GET', 'POST'])
def editar(titulo):
    if request.method == 'POST':
        data = {
            "Titulo": request.form['Titulo'],
            "Genero": request.form['Genero'],
            "año": int(request.form['año']),
            "Clasificacion": request.form['Clasificacion']
        }
        res = requests.put(f"{API_URL}/{titulo}", json=data)
        if res.status_code == 200:
            flash("Película actualizada correctamente.", "success")
            return redirect(url_for('index'))
        else:
            flash(f"Error: {res.json().get('detail', res.text)}", "danger")
    else:
        res = requests.get(f"{API_URL}/{titulo}")
        if res.status_code == 200:
            return render_template('editar.html', pelicula=res.json())
        else:
            flash("Película no encontrada.", "danger")
            return redirect(url_for('index'))

@app.route('/eliminar/<string:titulo>')
def eliminar(titulo):
    res = requests.delete(f"{API_URL}/{titulo}")
    if res.status_code == 200:
        flash("Película eliminada correctamente.", "success")
    else:
        flash("No se pudo eliminar la película.", "danger")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=8001)
