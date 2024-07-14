# TP1 - Bookly
## Install
```bash
python3 -m venv venv
source venv/bin/activate
pip install flask

sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" &gt; /etc/apt/sources.list.d/pgdg.list'
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add - s

sudo apt-get -y install postgresql

pip install Flask-cors

pip install sqlalchemy
```

## Run
Terminal 1:
```bash
cd backend
source venv/bin/activate
python3 main.py
```

Terminal 2:
```bash
cd frontend
python3 -m http.sever
```

Terminal 3:
```bash
sudo -u [your_username] psql [database_name]
```
