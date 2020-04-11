"""Controller"""

# Flask
from flask import Flask, jsonify, request

# Flask SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

# Flask MarshMallow
from flask_marshmallow import Marshmallow

app = Flask(__name__)  # Creamos una instancia de Flask.
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///database/products.db'
db=SQLAlchemy(app)
ma = Marshmallow(app)

class Product(db.Model):
    """Modelo de Clase para la tabla Product"""
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(20))
    price=db.Column(db.Integer)
    cantidad=db.Column(db.Integer)

    def __init__(self,name,price,cantidad):
        self.name=name
        self.price=price
        self.cantidad=cantidad
db.create_all()
class ProductSchema(ma.Schema):
    class Meta:
        fields =('id','name','price','cantidad')

productSchema=ProductSchema()
productsSchema=ProductSchema(many=True)

@app.route('/ping')
def ping():
    """Ruta de Prueba"""
    return jsonify({
        'mensaje':'pong'
    })  # Serializamos la salida a Json

@app.route('/products', methods=['GET'])
def getProducts():
    """Listar Productos"""
    products = Product.query.all()
    result = productsSchema.dump(products)
    return jsonify(result)

@app.route('/products/<string:product_name>')
def retrieveProduct(product_name):
    """Recupera un Producto por su nombre"""
    product=Product.query.filter_by(name=product_name).first()
    """Si queremos buscar un producto por su id podemos usar el metodo get
    que esta especificamente hecho para eso
    product=Product.query.get(id=product_id)
    """
    if(product):
        result = productSchema.dump(product)
        return jsonify(result)
    return jsonify({'mensaje':'producto no encontrado'})

@app.route('/products',methods=['POST'])
def createProduct():
    name = request.json['name']
    price = request.json.get('price',0)  # Otra forma de obtener los datos. En caso que no contenga el dato colocamos el valor vacio o cualquiera valor por defecto.
    cantidad = int(request.json.get('cantidad',0))
    product = Product(name=name, price=price, cantidad=cantidad)
    db.session.add(product)
    db.session.commit()
    return productSchema.jsonify(product)

@app.route('/products/<string:name>', methods=['PUT'])
def updateProduct(name):
    product=Product.query.filter_by(name=name).first()
    if(product):
        aux=productSchema.dump(product)
        product.name = request.json['name']
        product.price = request.json.get('price',aux['price'])
        product.cantidad = request.json.get('cantidad',aux['cantidad'])
        db.session.commit()
        result = productSchema.dump(product)
        return jsonify({
            'mensaje':'Producto actualizado exitosamente',
            'product':result
        })
    return jsonify({'mensaje':'producto no encontrado'})

@app.route('/products/<string:name>', methods=['DELETE'])
def deleteProduct(name):
    product=Product.query.filter_by(name=name).first()
    if(product):
        result=productSchema.dump(product)
        Product.query.filter_by(name=name).delete()
        db.session.commit()
        return jsonify({'mensaje':'Producto eliminado exitosamente','product':result})
    return jsonify({'mensaje':'producto no encotrado'})
    
if __name__ == "__main__":
    app.run(debug=True, port= 4000)  # Por defecto se ejecuta en el puerto 5000
