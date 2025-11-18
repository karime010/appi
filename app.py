from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import requests

app = Flask(__name__)
app.secret_key = "tu_clave"
API = "https://world.openfoodfacts.org/api/v2/product/"
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/search', methods=['POST']) 
def search_open():
    barcode = request.form.get('barcode','').strip()
    
    if not barcode:
        flash('por favor ingresa un codigo de barras','error')
        return redirect(url_for('index'))
    
    try:
        resp = requests.get(f"{API}{barcode}.json")
        if resp.status_code == 200:
            data = resp.json()
            if "product" not in data:
                flash(f'Producto no encontrado', 'error')
                return redirect(url_for('index'))
            product = data["product"]
            product_info = {
    "name" : product.get("product_name","Desconocido"),
    "brand" : product.get("brands", "Desconocido"),
    "quantity" : product.get("quantity","Desconocido"),
    "calories" : product.get("nutriments", {}).get("energy-kcal", "N/A"),
    "fat" : product.get("nutriments", {}).get("fat", "N/A"),
    'image' : product.get("image_front_url", ""),
}
            return render_template('Open.html', product=product_info)
        else:
            flash(f'Producto no encontrado', 'error')
            return redirect(url_for('index'))
    except requests.exceptions.RequestException as e:
        flash('Error al buscar el producto','error')
        return redirect(url_for('index'))


if __name__=='__main__':
    app.run(debug=True)