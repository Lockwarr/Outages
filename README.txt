#install hug in your venv

Running the API:
    hug -f main.py

Running tests:
    python -m unittest tests/services_status_test.py

Example body for '/add_outage' request:
    {"service_id": 2561, "duration": 12312312, "timestamp": 1606579200}