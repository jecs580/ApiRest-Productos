"""Controller"""

# Flask
from flask import Flask, jsonify

# Models
from product import products

app = Flask(__name__)  # Creamos una instancia de Flask.

@app.route('/ping')
def ping():
    """Ruta de Prueba"""
    return jsonify({
        'mensaje':'pong'
    })  # Serializamos la salida a Json

@app.route('/products', methods=['GET'])
def getProducts():
    """Listar Productos"""
    return jsonify(
        {'products': products,
        'mensaje':'Lista de Productos'
        })

@app.route('/products/<string:product_name>')
def retrieveProduct(product_name):
    """Recupera un Producto por su nombre"""
    product=[product for product in products if product['name']==product_name]
    if(len(product)>0):
        return jsonify({'product':product[0]})
    return jsonify({'mensaje':'producto no encontrado'})

if __name__ == "__main__":
    app.run(debug=True, port= 4000)  # Por defecto se ejecuta en el puerto 5000
