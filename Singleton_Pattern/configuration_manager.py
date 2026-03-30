import json
from typing import Any


# 1. The Singleton Configuration Manager

class ConfigManager:
    """Singleton class to manage application configuration."""
    
    # The single, shared instance is stored at the class level
    _instance = None

    def __init__(self):
        """Private constructor. Prevents direct instantiation."""
        if ConfigManager._instance is not None:
            raise RuntimeError("This is a Singleton! Use ConfigManager.get_instance() instead.")
        
        # Load the configuration into memory upon creation
        self._config = self._load_config()

    @classmethod
    def get_instance(cls) -> 'ConfigManager':
        """Returns the shared instance, creating it if it doesn't exist yet."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def _load_config(self) -> dict:
        """Internal method to read the file. We add a print to prove it runs once."""
        print(">>> ⚙️ [SYSTEM] Reading config.json from disk... (This should only happen ONCE) <<<\n")
        try:
            # Note: In a real scenario, make sure 'config.json' exists in your directory
            with open("config.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            print("Warning: config.json not found. Returning empty config.")
            return {}

    def get(self, key_path: str, default: Any = None) -> Any:
        """
        Retrieves a value using dot notation (e.g., 'database.host').
        Returns the `default` value if the key doesn't exist.
        """
        keys = key_path.split('.')
        value = self._config
        
        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default



# 2. Refactored Services


# database.py
def connect_database():
    config = ConfigManager.get_instance()
    db_host = config.get("database.host")
    db_port = config.get("database.port")
    print(f"Connecting to database at {db_host}:{db_port}")


# email_service.py
def send_email(to: str, subject: str):
    config = ConfigManager.get_instance()
    smtp_host = config.get("email.smtp_host")
    sender = config.get("email.sender")
    print(f"Sending email '{subject}' to {to} from {sender} via {smtp_host}")


# payment_service.py
def process_payment(amount: float):
    config = ConfigManager.get_instance()
    api_key = config.get("payment.api_key")
    environment = config.get("payment.environment")
    print(f"Processing {amount}€ in {environment} mode (Key: {api_key[:7]}...)")


# app.py
def start_application():
    config = ConfigManager.get_instance()
    app_name = config.get("app.name")
    debug = config.get("app.debug")
    print(f"Starting {app_name} (debug={debug})")



# 3. Usage

if __name__ == "__main__":
    # Simulate a mock config.json creation for the sake of making this script runnable 
    # (You wouldn't include this in production)
    sample_json = {
        "app": {"name": "PaymentPlatform", "debug": True},
        "database": {"host": "localhost", "port": 5432},
        "email": {"smtp_host": "smtp.company.com", "sender": "no-reply@company.com"},
        "payment": {"api_key": "sk_test_123456", "environment": "sandbox"}
    }
    with open("config.json", "w") as f:
        json.dump(sample_json, f)

    # Watch the console output carefully: 
    # The file read print statement will only trigger ONE time!
    start_application()
    connect_database()
    send_email("user@test.com", "Welcome")
    process_payment(99.99)