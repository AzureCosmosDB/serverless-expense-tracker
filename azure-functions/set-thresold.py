import azure.functions as func
from azure.functions.decorators import FunctionApp
from azure.functions.decorators.http import HttpTrigger
from . import app

COSMOS_ENDPOINT = "https://expense-tracker.documents.azure.com:443/"
COSMOS_KEY = ""
DATABASE_NAME = "ExpenseTracker"
THRESHOLDS_CONTAINER = "Thresholds"

@app.function_name(name="SetThreshold")
@app.route(route="set-threshold", methods=["POST"])
def set_threshold(req: func.HttpRequest) -> func.HttpResponse:
    req_body = req.get_json()
    category = req_body.get('category')
    threshold = req_body.get('threshold')

    # Logic for setting threshold in Cosmos DB or any other service

    client = CosmosClient(COSMOS_ENDPOINT, COSMOS_KEY)
    db = client.get_database_client(DATABASE_NAME)
    thresholds = db.get_container_client(THRESHOLDS_CONTAINER)

    try:
        threshold_data = req.get_json()
        thresholds.upsert_item(threshold_data)
        return func.HttpResponse("Threshold set successfully.", status_code=200)
    except Exception as e:
        return func.HttpResponse(f"Error: {str(e)}", status_code=500)
