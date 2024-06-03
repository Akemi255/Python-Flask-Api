from flask import Flask, request, jsonify
from models import db, Venta
from datetime import datetime

app = Flask(__name__)
app.config.from_object('config.Config')
db.init_app(app)

@app.route('/ventas', methods=['GET'])
def get_ventas():
    ventas = Venta.query.all()
    return jsonify([venta.to_dict() for venta in ventas])

@app.route('/ventas/<string:folio>', methods=['GET'])
def get_venta(folio):
    venta = Venta.query.filter_by(folio=folio).first()
    if venta:
        return jsonify(venta.to_dict())
    return jsonify({"error": "Venta no encontrada"}), 404

@app.route('/ventas', methods=['POST'])
def create_venta():
    data = request.get_json()
    new_venta = Venta(
        folio=data['folio'],
        fecha=datetime.strptime(data['fecha'], '%Y-%m-%d %H:%M:%S'),
        cantidad=data['cantidad'],
        total=data['total']
    )
    db.session.add(new_venta)
    db.session.commit()
    return jsonify(new_venta.to_dict()), 201

@app.route('/ventas/<string:folio>', methods=['PUT'])
def update_venta(folio):
    venta = Venta.query.filter_by(folio=folio).first()
    if not venta:
        return jsonify({"error": "Venta no encontrada"}), 404

    data = request.get_json()
    venta.fecha = datetime.strptime(data['fecha'], '%Y-%m-%d %H:%M:%S')
    venta.cantidad = data['cantidad']
    venta.total = data['total']
    db.session.commit()
    return jsonify(venta.to_dict())

@app.route('/ventas/<string:folio>', methods=['DELETE'])
def delete_venta(folio):
    venta = Venta.query.filter_by(folio=folio).first()
    if not venta:
        return jsonify({"error": "Venta no encontrada"}), 404

    db.session.delete(venta)
    db.session.commit()
    return jsonify({"message": "Venta eliminada"})

@app.route('/ventas/ordenadas', methods=['GET'])
def get_ventas_ordenadas():
    ventas = Venta.query.order_by(Venta.total.desc()).all()
    return jsonify([venta.to_dict() for venta in ventas])

@app.route('/ventas/mayores', methods=['GET'])
def get_ventas_mayores():
    ventas = Venta.query.filter(Venta.total > 1000).all()
    return jsonify([venta.to_dict() for venta in ventas])

@app.route('/ventas/ano/<int:ano>', methods=['GET'])
def get_ventas_ano(ano):
    ventas = Venta.query.filter(db.extract('year', Venta.fecha) == ano).all()
    return jsonify([venta.to_dict() for venta in ventas])

@app.route('/ventas/maximo', methods=['GET'])
def get_venta_maximo():
    venta = Venta.query.order_by(Venta.total.desc()).first()
    return jsonify(venta.to_dict()) if venta else jsonify({"error": "No hay ventas"}), 404

if __name__ == '__main__':
    app.run(debug=True)
