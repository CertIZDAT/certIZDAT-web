# certIZDAT-web

## Running the development server

Use Python 3.11 or newer


Run the following commands in a POSIX-compatible shell:
```bash
git clone https://github.com/CertIZDAT/certIZDAT-web.git
cd certIZDAT-web/
git submodule update --init
python3 -m venv env
. env/bin/activate
pip3 install -r requirements.txt
cd backend/
DEBUG=1 ALLOW_INSECURE_HTTP=1 gunicorn -c dev-config.py app:app
```

Open `http://127.0.0.1:80`. The analyser database is still required to run the actual application.

`DEBUG` and `ALLOW_INSECURE_HTTP` accept `1`, `true`, `yes`, or `on` for true, and
`0`, `false`, `no`, `off`, or an empty/unset value for false (case-insensitive).
Invalid values fail startup. **Debug mode does not disable HTTPS enforcement**;
local HTTP requires the separate, explicit `ALLOW_INSECURE_HTTP=1` opt-out.
With `DEBUG=1`, allowed request from any host.

## Production

Install the requirements.txt, then run from `backend/`:

```bash
gunicorn -c config.py app:app
```

`config.py` terminates TLS on port 443 using the configured Let's Encrypt
certificate paths; provision those files and restrict private-key permissions.


- Flask's `TRUSTED_HOSTS` allows only `certizdat.org` in production. Requests
  with other Host values return HTTP 400, including before an HTTPS redirect.
- Both bundled Gunicorn configurations ignore forwarded scheme headers. Direct
  clients cannot use `X-Forwarded-Proto` to bypass HTTPS enforcement.
- HTTPS responses include one-year HSTS. All application responses include CSP,
  `nosniff`, framing protection, and a referrer policy. CSP permits the existing
  inline styles but not inline scripts or event handlers.
