import logging, os, json
import azure.functions as func
from azure.cosmos import CosmosClient

def main(req: func.HttpRequest) -> func.HttpResponse:
    client = CosmosClient.from_connection_string(os.getenv("COSMOS_CONNSTR"))
    container = client.get_database_client(os.getenv("DB_NAME")).get_container_client(os.getenv("CONTAINER_NAME"))

    query = "SELECT TOP 50 * FROM c WHERE c.pk = @pk ORDER BY c.createdAt DESC"
    items = list(container.query_items(query=query,
                                       parameters=[{"name":"@pk","value":"default"}],
                                       enable_cross_partition_query=True))
    return func.HttpResponse(json.dumps(items), status_code=200, mimetype="application/json")
