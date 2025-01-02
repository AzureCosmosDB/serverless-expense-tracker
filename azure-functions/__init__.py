from azure.functions import FunctionApp

app = FunctionApp()

# Import your function modules to register them
from . import submit_transactions
from . import set_threshold
from . import check_threshold