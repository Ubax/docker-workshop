from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import requests
import os


app = Flask(__name__)

port = os.getenv('PORT', 5000)
host = os.getenv('HOST', "127.0.0.1")

dbUsername = os.getenv('POSTGRES_USER')
dbPassword = os.getenv('POSTGRES_PASSWORD')
dbHost = os.getenv('POSTGRES_HOST')
dbPort = os.getenv('POSTGRES_PORT')
dbName = os.getenv('POSTGRES_DB')

if not dbUsername or not dbPassword or not dbHost or not dbPort or not dbName:
    raise ValueError('Missing required environment variables for db connection. Current configuration: '
                     f'dbUsername={dbUsername}, dbPassword={dbPassword}, dbHost={dbHost}, dbPort={dbPort}, dbName={dbName}')

serviceBaseUrl = os.getenv('SERVICE_BASE_URL')

if not serviceBaseUrl:
    raise ValueError('Missing required environment variable SERVICE_BASE_URL')

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{dbUsername}:{dbPassword}@{dbHost}:{dbPort}/{dbName}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Item(db.Model):
    __tablename__ = 'item'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    done = db.Column(db.Boolean, default=False)


with app.app_context():
    db.create_all()


@app.route('/api/item', methods=['GET'])
def get_items():
    items_db = Item.query.all()
    items = [{'id': item.id, 'name': item.name, 'done': item.done}
             for item in items_db]
    return jsonify(items)


@app.route('/api/item', methods=['POST'])
def add_item():
    new_item_name = request.json.get('name')
    if not new_item_name:
        return jsonify({'error': 'Item name is required'}), 400

    if db.session.query(Item).filter_by(name=new_item_name).first() is not None:
        return jsonify({'error': 'Item already exists'}), 400

    new_item = Item(name=new_item_name)
    db.session.add(new_item)
    db.session.commit()

    return jsonify({'message': 'Item added successfully'}), 201


@app.route('/api/item/toggle/<id>', methods=['POST'])
def toggle_item(id):
    item_to_check = Item.query.get(id)
    if not item_to_check:
        return jsonify({'error': 'Item not found'}), 404

    db.session.query(Item).filter_by(id=id).update(
        {Item.done: not item_to_check.done})
    db.session.commit()

    return jsonify({'message': 'Item deleted successfully'}), 200


@app.route('/api/item/<id>', methods=['DELETE'])
def delete_item(id):
    item_to_delete = Item.query.get(id)
    if not item_to_delete:
        return jsonify({'error': 'Item not found'}), 404

    db.session.delete(item_to_delete)
    db.session.commit()

    return jsonify({'message': 'Item deleted successfully'}), 200


@app.route('/api/report', methods=['GET'])
def get_report():
    # Replace with actual service URL
    external_service_url = f"{serviceBaseUrl}/report"

    try:
        # Fetch the report from the external service
        response = requests.get(external_service_url)
        response.raise_for_status()  # Check for HTTP errors
    except requests.RequestException as e:
        return jsonify({'error': 'Failed to fetch report', 'details': str(e)}), 500

    # Forward the JSON response
    return jsonify(response.json())


if __name__ == '__main__':
    app.run(debug=True, port=port, host=host)
