"""Controller"""

# Flask
from flask import Flask, jsonify, request

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

@app.route('/products',methods=['POST'])
def createProduct():
    newProduct = {
        "name": request.json['name'],
        "price": request.json.get('price',''),  # Otra forma de obtener los datos. En caso que no contenga el dato colocamos el valor vacio o cualquiera valor por defecto.
        'cantidad':request.json.get('cantidad','')
        }
    products.append(newProduct)
    return jsonify({
        'product': newProduct
    })

@app.route('/products/<string:name>', methods=['PUT'])
def updateProduct(name):
    product = [product for product in products if product['name']==name]
    if(len(product)>0):
        product[0]['name'] = request.json.get('name',product[0]['name'])
        product[0]['price'] = request.json.get('price',product[0]['price'])
        product[0]['cantidad'] = request.json.get('cantidad',product[0]['cantidad'])
        return jsonify({
            'mensaje':'Producto actualizado exitosamente',
            'product':product[0]
        })
    return jsonify({'mensaje':'producto no encontrado'})

@app.route('/products/<string:name>', methods=['DELETE'])
def deleteProduct(name):
    product=[p for p in products if p['name']==name]
    if(len(product)>0):
        products.remove(product[0])
        return jsonify({'mensaje':'Producto eliminado exitosamente','product':product[0]})
    return jsonify({'mensaje':'producto no encotrado'})
    
if __name__ == "__main__":
    app.run(debug=True, port= 4000)  # Por defecto se ejecuta en el puerto 5000
