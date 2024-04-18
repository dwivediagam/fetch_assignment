from flask import Flask, request, jsonify, render_template, redirect
import uuid
import re
import math
import json

app = Flask(__name__)

# In-memory storage for processed receipts
processed_receipts = {}

data = {
  "retailer": "M&M Corner Market",
  "purchaseDate": "2022-03-20",
  "purchaseTime": "14:33",
  "items": [
    {
      "shortDescription": "Gatorade",
      "price": "2.25"
    },{
      "shortDescription": "Gatorade",
      "price": "2.25"
    },{
      "shortDescription": "Gatorade",
      "price": "2.25"
    },{
      "shortDescription": "Gatorade",
      "price": "2.25"
    }
  ],
  "total": "9.00"
}

@app.route('/', methods=['GET'])
def home():
     return redirect('/receipts/process')

@app.route('/receipts/process', methods=['GET', 'POST'])
def process_receipts():
	if request.method=='POST':
		json_data = request.form['json_data']
		json_data = json.loads(json_data)
		# data = request.json
		try:
			receipt_id = str(uuid.uuid4())
			# Your code to process the receipt and calculate points
			print(json_data)
			points = calculate_points(json_data)
			response = {"id": receipt_id}
			# Save the receipt ID and points (in-memory solution)
			processed_receipts[receipt_id] = points
			return jsonify(response)
		except json.JSONDecodeError:
			return jsonify({'error': 'Invalid JSON format'})
	return render_template('index.html')

@app.route('/receipts/<string:receipt_id>/points', methods=['GET'])
def get_points(receipt_id):
    if receipt_id not in processed_receipts:
        return jsonify({"error": "Receipt ID not found"}), 404
    points = processed_receipts[receipt_id]
    return jsonify({"points": points})

def calculate_points(data):
    points = 0
    #One point for every alphanumeric character in the retailer name
    points += sum(1 for char in data['retailer'] if char.isalnum())
    #50 points if the total is a round dollar amount with no cents
    if data['total'].endswith('.00'):
        points += 50
    #25 points if the total is a multiple of 0.25
    if float(data['total']) % 0.25 == 0:
        points += 25
    #5 points for every two items on the receipt
    points += len(data['items']) // 2 * 5
    #Multiply the price by 0.2 and round up to the nearest integer if the trimmed length of the item description is a multiple of 3
    for item in data['items']:
        trimmed_length = len(item['shortDescription'].strip())
        if trimmed_length % 3 == 0:
            points += math.ceil(float(item['price']) * 0.2)
    #6 points if the day in the purchase date is odd
    if int(data['purchaseDate'].split('-')[2]) % 2 != 0:
        points += 6
    #10 points if the time of purchase is after 2:00pm and before 4:00pm
    purchase_time = int(data['purchaseTime'].split(':')[0])
    if 14 <= purchase_time < 16:
        points += 10
    return points

