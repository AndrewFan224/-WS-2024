from flask import Flask
from flask_restful import Resource, Api
import json
from pymongo import MongoClient
from bson.json_util import dumps, loads
from bson.objectid import ObjectId
from flask_restful import reqparse
from flask import request

app = Flask(__name__)
api = Api(app)

class GetProducts(Resource):
    def get(self):

        client = MongoClient("mongodb://root:example@localhost:27017/")
        db = client.Products
        collection = db.Products_data       
        
        results = dumps(collection.find())
        return json.loads(results)
       
        
 
             
api.add_resource(GetProducts, '/getProducts')

API_KEY = "login"
class InsertProducts(Resource):
    def get(self):
        api_key = request.args.get('api_key')
        if api_key != API_KEY:
            # If the error is a set, convert it to a list before returning
            error_message = {"Error": "This is an Invalid API Key. Failed."}
            return error_message, 401
        

        client = MongoClient("mongodb://root:example@localhost:27017/")
        db = client.Products
        collection = db.Products_data
        collection.insert_one(
              {
                "id": 1,
                "title": "Jam",
                "price": 1.50,
                "quantity": 2
            },
            {
                "id": 2,
                "title": "Coffee",
                "price": 2.30,
                "quantity": 1
            },
            {
                "id": 3,
                "title": "Cola",
                "price": 11.20,
                "quantity": 2
            },
            {
                "id": 4,
                "title": "Tea",
                "price": 4.50,
                "quantity": 3
            }
        )

        #return
        return {"status":"inserted"}
 
             
api.add_resource(InsertProducts, '/InsertProducts')


class GetTitles(Resource):
    def get(self):
        client = MongoClient("mongodb://root:example@localhost:27017/")
        db = client.Products
        collection = db.Products_data
        # ID of the object
        id = '65fc1f54cc51f00a65a4efb3'
        query = {"_id": ObjectId(id)}
        filter = {"_id": 0, "ProductId": 1}
        # find it
        result = collection.find_one(query, filter)
        # Convert to JSON
        result = dumps(result)
        # Return the JSON result
        return json.loads(result)
        
 
             
api.add_resource(GetTitles, '/GetTitles')

class InsertOne(Resource):
    def get(self):
        client = MongoClient("mongodb://root:example@localhost:27017/")
        db = client.Products
        collection = db.Products_data
        try:
            sale_id = request.args.get('SaleId')
            order_id = request.args.get('OrderId')
            product_id = request.args.get('ProductId')
            quantity = request.args.get('Quantity')

            sale_id = int(sale_id)
            order_id = int(order_id)
            product_id = int(product_id)
            quantity = int(quantity)

            new_record = {"SaleId": sale_id, "OrderId": order_id, "ProductId": product_id, "Quantity": quantity}

            result = collection.insert_one(new_record)

            return {"status": "inserted"}, 200
        except Exception as e:
            return {"error": str(e)}, 500

api.add_resource(InsertOne, '/insertOne')



class route(Resource):
    def get(self):
        return [
                {
                    "url": "/InsertProducts",
                    "description": "Inserts a product into the database. Requires an API key."
                },
                {
                    "url": "/GetProducts",
                    "description": "Gets all the products."
                },
        ]
 
             
api.add_resource(route, '/')




            
if __name__ == '__main__':
    app.run(debug=True)
