# config.py

import multiprocessing

workers = 2 * multiprocessing.cpu_count()

bind = '0.0.0.0:443'

certfile = '/etc/letsencrypt/live/certizdat.org/fullchain.pem'

keyfile = '/etc/letsencrypt/live/certizdat.org/privkey.pem'

forwarded_allow_ips = '*'
