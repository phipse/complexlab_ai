# About

Use src/main.py to start the programm. The --help text explains the usage.

#Setup

On Fedora 17:
```bash
sudo pip-python install -r requirements.txt
sudo systemctl start mongod  # run mongodb daemon
src/main.py --help  # read usage
```

On Ubuntu:
```bash
sudo pip install -r requirements.txt
sudo service mongod start  # run mongodb daemon
src/main.py --help  # read usage
```
