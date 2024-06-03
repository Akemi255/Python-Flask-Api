from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from decimal import Decimal

db = SQLAlchemy()

class Venta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    folio = db.Column(db.String(50), unique=True, nullable=False)
    fecha = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    cantidad = db.Column(db.Float, nullable=False)
    total = db.Column(db.Numeric, nullable=False)

    def to_dict(self):
        return {
            'folio': self.folio,
            'fecha': self.fecha.strftime('%Y-%m-%d %H:%M:%S'),
            'cantidad': self.cantidad,
            'total': float(self.total)
        }

    def __repr__(self):
        return f'<Venta {self.folio}>'
