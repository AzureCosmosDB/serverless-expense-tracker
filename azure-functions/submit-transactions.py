import azure.functions as func
from azure.functions.decorators import FunctionApp
from azure.functions.decorators.http import HttpTrigger
from azure.cosmos import CosmosClient
from . import app

COSMOS_ENDPOINT = "your-cosmos-db-endpoint"
COSMOS_KEY = "your-cosmos-db-key"
DATABASE_NAME = "ExpenseTracker"
TRANSACTIONS_CONTAINER = "Transactions"

@app.function_name(name="SubmitTransactions")
@app.route(route="submit-transactions", methods=["POST"])
def submit_transaction(req: func.HttpRequest) -> func.HttpResponse:
    req_body = req.get_json()
    user_id = req_body.get('userId')
    amount = req_body.get('amount')
    category = req_body.get('category')

    # You would insert logic here to store the transaction in Cosmos DB or trigger notifications
    client = CosmosClient(COSMOS_ENDPOINT, COSMOS_KEY)
    db = client.get_database_client(DATABASE_NAME)
    transactions = db.get_container_client(TRANSACTIONS_CONTAINER)
    try:
        transaction_data = req.get_json()
        transactions.upsert_item(transaction_data)
        return func.HttpResponse("Transaction submitted successfully.", status_code=200)
    except Exception as e:
        return func.HttpResponse(f"Error: {str(e)}", status_code=500)
