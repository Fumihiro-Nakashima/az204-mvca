import logging, os, json, datetime, uuid
import azure.functions as func
from azure.cosmos import CosmosClient

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        body = req.get_json()
    except:
        body = {}
    name = body.get("name")
    if not name:
        return func.HttpResponse(json.dumps({"error":"name required"}), status_code=400)

    client = CosmosClient.from_connection_string(os.getenv("COSMOS_CONNSTR"))
    container = client.get_database_client(os.getenv("DB_NAME")).get_container_client(os.getenv("CONTAINER_NAME"))

    item = {
        "id": str(uuid.uuid4()),
        "pk": "default",
        "name": name,
        "createdAt": datetime.datetime.utcnow().isoformat()
    }
    container.create_item(item)
    return func.HttpResponse(json.dumps(item), status_code=201, mimetype="application/json")
