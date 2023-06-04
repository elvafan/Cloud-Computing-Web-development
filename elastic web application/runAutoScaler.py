#!../venv/bin/python
from AutoScaler import webapp

# Port 5002 for Manager
webapp.run('0.0.0.0', 5003, debug=True, use_reloader=False)
