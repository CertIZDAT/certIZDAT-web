# config.py

import multiprocessing

workers = 2 * multiprocessing.cpu_count() + 1

bind = '0.0.0.0:443'

certfile = '/etc/letsencrypt/live/certizdat.org/fullchain.pem'
keyfile = '/etc/letsencrypt/live/certizdat.org/privkey.pem'

# Security
forwarded_allow_ips = '127.0.0.1'  # Limit to localhost for security reasons

# Performance
worker_class = 'gevent'  # Use gevent workers for handling long-polling or WebSockets
worker_connections = 1000  # Increase worker connections if using gevent or eventlet workers
timeout = 30  # Adjust depending on your application's requirements
keepalive = 2  # Adjust depending on your application's requirements

# Logging
accesslog = 'access.log'  # Adjust path as needed
errorlog = 'error.log'  # Adjust path as needed
loglevel = 'info'  # Adjust log level as needed
