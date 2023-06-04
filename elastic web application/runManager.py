#!../venv/bin/python
from ManagerApp import webapp

# Port 5002 for Manager
webapp.run('0.0.0.0', 5002, debug=True, use_reloader=False)
