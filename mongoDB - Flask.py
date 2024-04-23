from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client['userData']
collection = db['Customer']

# Default route to serve the HTML page
@app.route('/')
def index():
    return render_template('index.html')

# Write Data
@app.route('/add_customer', methods=['POST'])
def add_customer():
    data = request.get_json()
    result = collection.insert_one(data)
    return jsonify({'message': 'Customer added successfully', 'id': str(result.inserted_id)})

from bson import ObjectId

# Fetch Data
@app.route('/get_customers', methods=['GET'])
def get_customers():
    customers = list(collection.find())
    # Convert ObjectId to string
    for customer in customers:
        customer['_id'] = str(customer['_id'])
    return jsonify(customers)

# Update Data
@app.route('/update_customer/<string:id>', methods=['PUT'])
def update_customer(id):
    data = request.get_json()
    result = collection.update_one({'_id': ObjectId(id)}, {'$set': data})
    if result.modified_count == 1:
        return jsonify({'message': 'Customer updated successfully'})
    else:
        return jsonify({'message': 'Customer not found'}), 404

# Delete Data
@app.route('/delete_customer/<string:id>', methods=['DELETE'])
def delete_customer(id):
    result = collection.delete_one({'_id': ObjectId(id)})
    if result.deleted_count == 1:
        return jsonify({'message': 'Customer deleted successfully'})
    else:
        return jsonify({'message': 'Customer not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
