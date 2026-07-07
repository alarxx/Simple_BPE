# Simple_BPE

## Setup

Install python:
```sh
apt install python3 python3-full python3-pip python3-venv
#sudo apt install python3.8
python3 --version
```

Set up python venv:
```sh
python3 -m venv .venv
. .venv/bin/activate
pip install -e .
# deactivate
```
Or set up with uv:
```sh
# install python
uv python install 3.13
uv init --python 3.13
uv venv
uv pip install pip
. .venv/bin/activate
pip install -e .
```

---

