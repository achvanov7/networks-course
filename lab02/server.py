#!flask/bin/python
from flask import Flask, request, abort, send_file
import json

app = Flask(__name__)

products = []
id_cnt = 1

@app.route("/product", methods = ["POST"])
def add_product():
  global products, id_cnt
  try:
    data = json.loads(request.get_data())
    name = data["name"]
    desc = data["description"]
  except:
    abort(406)
  products.append({
    "id": id_cnt,
    "name": name,
    "description": desc
  })
  id_cnt += 1
  return json.dumps(products[-1])

def find_product(id):
  global products
  for product in products:
    if product['id'] == id:
      return product
  return None

@app.route("/product/<int:product_id>", methods = ["GET"])
def get_product(product_id):
  global products
  product = find_product(product_id)
  if product is None:
    abort(404)
  return json.dumps(product)

@app.route("/product/<int:product_id>", methods = ["PUT"])
def change_product(product_id):
  global products
  data = json.loads(request.get_data())
  product = find_product(product_id)
  if product is None:
    abort(404)
  if "name" in data:
    product["name"] = data["name"]
  if "description" in data:
    product["description"] = data["description"]
  return json.dumps(product)

@app.route("/product/<int:product_id>", methods = ["DELETE"])
def delete_product(product_id):
  global products
  product = find_product(product_id)
  if product is None:
    abort(404)
  json_response = json.dumps(product)
  products.remove(product)
  return json_response

@app.route("/products", methods = ["GET"])
def get_all_products():
  global products
  return json.dumps(products)

@app.route("/product/<int:product_id>/image", methods = ["POST"])
def post_product_image(product_id):
  global products
  product = find_product(product_id)
  if product is None:
    abort(404)
  if len(request.files) != 1:
    abort(406)
  for icon in request.files:
    request.files[icon].save(icon)
    product["icon"] = icon
  return "Success"

@app.route("/product/<int:product_id>/image", methods = ["GET"])
def get_product_image(product_id):
  global products
  product = find_product(product_id)
  if product is None or "icon" not in product:
    abort(404)
  return send_file(product["icon"])
  