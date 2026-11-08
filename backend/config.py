# config.py

import multiprocessing

workers = 2 * multiprocessing.cpu_count() + 1

bind = "0.0.0.0:443"

# root user
# certfile = "/etc/letsencrypt/live/certizdat.org/fullchain.pem"
# keyfile = "/etc/letsencrypt/live/certizdat.org/privkey.pem"

certfile = "/etc/ssl/certizdat/fullchain.pem"
keyfile = "/etc/ssl/certizdat/privkey.pem"

# or for non-root user /etc/ssl/certizdat/fullchain.pem and /etc/ssl/certizdat/privkey.pem

# Security
# This listener terminates TLS itself and must not trust client scheme headers
forwarded_allow_ips = ""
reload = False

# Performance
worker_class = "gevent"  # Use gevent workers for handling long-polling or WebSockets
worker_connections = (
    1000  # Increase worker connections if using gevent or eventlet workers
)
timeout = 30  # Adjust depending on your application's requirements
keepalive = 2  # Adjust depending on your application's requirements

# Logging
accesslog = "access.log"  # Adjust path as needed
errorlog = "error.log"  # Adjust path as needed
loglevel = "info"  # Adjust log level as needed
