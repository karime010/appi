from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import requests

app = Flask(__name__)
app.secret_key = "tu_clave"
API = "https://world.openfoodfacts.org/api/v0/product/"
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/search', methods=['POST']) 
def search_Open():
    producto = request.form.get('barcode','').strip().lower()
    
    if not producto:
        flash('por favor ingresa un producto','error')
        return redirect(url_for('index'))
    
    try:
        resp = requests.get(f"{API}{producto}.json")
        if resp.status_code == 200:
            pokemon = resp.json()
            pokemon_info= {
    'name' : producto.get['name'].title(),
    'id' : producto.get['id'],
    'height' : producto.get['height'] /10,
    'weight' : producto.get['weight'] /10,
    'image' : producto.get['sprites']['front_default'],
    'types' : [t['type']['name'].title() for t in producto.get['types']],
    'abilities' : [a['ability']['name'].title() for a in producto.get['abilities']],
    'stats' : {}
}
            return render_template('pokemon.html', pokemon=pokemon_info)
        else:
            flash(f'Producto "{producto}"no encontrado', 'error')
            return redirect(url_for('index'))
    except requests.exceptions.RequestException as e:
        flash('Error al buscar el producto','error')
        return redirect(url_for('index'))


if __name__=='__main__':
    app.run(debug=True)