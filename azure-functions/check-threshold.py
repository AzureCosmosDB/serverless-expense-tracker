import os
import yaml
from azure.cosmos import CosmosClient
import azure.functions as func
from azure.functions.decorators import FunctionApp
from azure.functions.decorators.timer import TimerTrigger
import httpx
import asyncio
from . import app

class ExpenseTracker:
    def __init__(self):
        config_file_path = os.path.join(os.path.dirname(__file__), "config.yaml")
        with open(config_file_path, "r") as file:
            config = yaml.safe_load(file)
            COSMOS_DB_ENDPOINT = config['cosmos_db_endpoint']
            COSMOS_DB_KEY = os.environ['cosmos_db_key']
            DATABASE_NAME = config['database_name']
            self.client = CosmosClient(COSMOS_DB_ENDPOINT, COSMOS_DB_KEY)
            self.db = self.client.create_database_if_not_exists(DATABASE_NAME)

expense_tracker = ExpenseTracker()

async def send_notification(message):
    async with httpx.AsyncClient() as client:
        await client.post(f"{WEBSOCKET_URL}/broadcast", json={"message": message})

@app.function_name(name="CheckThreshold")
@app.timer_trigger(schedule="0 */5 * * * *")
def check_threshold(timer: func.TimerRequest) -> None:
    client = expense_tracker.client
    db = client.get_database_client(DATABASE_NAME)
    transactions = db.get_container_client(TRANSACTIONS_CONTAINER)
    thresholds = db.get_container_client(THRESHOLDS_CONTAINER)

    users = thresholds.read_all_items()
    for user in users:
        global_threshold = user.get("globalThreshold", 0)
        category_thresholds = user.get("categoryThresholds", {})
        
        user_transactions = transactions.query_items(
            query="SELECT * FROM Transactions t WHERE t.userId = @userId",
            parameters=[{"name": "@userId", "value": user["userId"]}]
        )
        
        for txn in user_transactions:
            category = txn.get("category", "General")
            amount = txn["amount"]
            threshold = category_thresholds.get(category, global_threshold)
            
            if amount > threshold:
                message = f"🚨 Impulse Buy Alert! User: {user['userId']} Category: {category}, Amount: ${amount}"
                asyncio.run(send_notification(message))
