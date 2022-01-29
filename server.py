from flask import Flask, Response, request
import pymongo
import json
from bson.objectid import ObjectId

app = Flask(__name__) 

#Conectar com MongoDB
try:
    mongo = pymongo.MongoClient(
        host="localhost", 
        port=27017,
        serverSelectionTimeoutMS = 1000       
    )
    db = mongo.freshmania
    mongo.server_info()#trigger exceção se não conectar com banco
except:
    print("ERROR - Conexão com MongoDB deu erro!")

##################################################################

#GET Endpoint - consultar dados dos produtos no banco
@app.route("/products", methods=["GET"])
def get_all_products():
    try:
        data = list(db.products.find())

        for product in data:
            product["_id"] = str(product["_id"])
        
        return Response(
            response=json.dumps(data),
            status=200,
            mimetype="application/json"
        )

    except Exception as ex:
        print(ex) 
        return Response(
            response=json.dumps({ "message": "Error ao consultar dados dos produtos!" }),
            status=500,
            mimetype="application/json"
        )

##################################################################

#POST Endpoint - Criar produto no banco
@app.route("/products", methods=["POST"])
def create_product():
    try:
        product = { "name": request.form["name"], "price": request.form["price"]}
        dbResponse = db.products.insert_one(product)

        return Response(
            response=json.dumps({ "message": "Produto criado com sucesso!", "id": f"{dbResponse.inserted_id}"}),
            status=200,
            mimetype="application/json"
        )
    except Exception as ex:
        print(ex)  

##################################################################

if __name__ == "__main__":
    app.run(port=80, debug=True)