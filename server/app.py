#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    all_bakeries = []
    for bakery in Bakery.query.all():
        all_bakeries.append(bakery.to_dict())

    response = make_response(jsonify(all_bakeries), 200)
    return response

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    current_bakery = Bakery.query.filter(Bakery.id==id).first()
    response = make_response(jsonify(current_bakery.to_dict()))
    return response

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    all_bakeries_by_price = []
    for bake in BakedGood.query.order_by((BakedGood.price).desc()).all():
        all_bakeries_by_price.append(bake.to_dict())
    response = make_response(jsonify(all_bakeries_by_price))
    return response

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive_baked_good = BakedGood.query.order_by((BakedGood.price).desc()).first()
        
    response = make_response(jsonify(most_expensive_baked_good.to_dict()))
    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
