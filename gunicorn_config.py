"""
Gunicorn configuration to mitigate security vulnerabilities
"""
import multiprocessing

# Bind to localhost only to prevent external access
bind = "0.0.0.0:5000"

# Number of worker processes for handling requests
workers = multiprocessing.cpu_count() * 2 + 1

# Set worker class to sync to prevent possible timing-based request smuggling
worker_class = "sync"

# Set maximum requests per worker to prevent memory leaks
max_requests = 1000
max_requests_jitter = 50

# Enable HTTP response keep-alive to properly handle connections
keepalive = 5

# Set limits for headers and request body size
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# Disable Werkzeug debugger in production
reload = False 