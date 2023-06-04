#!../venv/bin/python
from Front import webapp

# Port 5000 for FrontEnd and Port 5001 for MemCache
webapp.run('0.0.0.0', 5000, debug=True)
