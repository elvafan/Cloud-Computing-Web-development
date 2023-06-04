#!../venv/bin/python
from Front import webapp

# Port 5000 for FrontEnd
webapp.run('0.0.0.0', 5000, debug=True, use_reloader=False)
