# certIZDAT-web

## Running

Run the following command in the POSIX-compatible shell

```bash
git clone https://github.com/CertIZDAT/certIZDAT-web.git
cd certIZDAT-web/
git submodule update --init
python3 -m venv env
source env/bin/activate
pip3 install -r requirements.txt 
cd backend/
gunicorn app:app --workers=$((2 * $(getconf _NPROCESSORS_ONLN))) --bind 0.0.0.0:80
```

See detailed technical documentation [here](https://github.com/CertIZDAT/russian-trusted-root-ca-analyzer).
