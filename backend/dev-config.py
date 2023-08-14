# gunicorn config

# The address to bind to (change this to your desired host and port)
bind = '0.0.0.0:80'

# Number of worker processes to spawn
workers = 4

# Number of threads per worker process
threads = 2

# Enable auto-reloading when code changes are detected
reload = True

# Logging configuration
accesslog = '-'  # '-' means log to stdout
errorlog = '-'   # '-' means log to stderr
loglevel = 'info'
