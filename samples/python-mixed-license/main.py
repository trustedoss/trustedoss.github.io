"""
Sample app that demonstrates mixed licenses.

It is a minimal example that imports dependencies under MIT, Apache-2.0,
BSD, and GPL licenses.
"""

import yaml          # PyYAML, MIT
import requests      # requests, Apache-2.0
import celery        # celery, BSD

# mysql.connector is GPL-2.0 (Oracle MySQL Connector/Python).
# The import only succeeds when it is installed.
try:
    import mysql.connector  # mysql-connector-python - GPL-2.0
    print("mysql.connector imported (GPL-2.0)")
except ImportError:
    print("mysql.connector is not installed (expected in this exercise)")


def main():
    print("=== mixed license sample app ===")

    # PyYAML (MIT)
    data = yaml.safe_load("name: trustedoss\nversion: 1.0")
    print(f"YAML parsed (MIT): {data}")

    # requests (Apache-2.0)
    print(f"requests version (Apache-2.0): {requests.__version__}")

    # celery (BSD)
    print(f"celery version (BSD): {celery.__version__}")

    print("\nWarning: this project includes a GPL package (mysql-connector-python).")
    print("Depending on how you distribute it, you may have to publish your source.")


if __name__ == "__main__":
    main()
