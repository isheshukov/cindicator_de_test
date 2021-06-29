# Cindicator Data Engineer test

## Usage

```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

To run the program

```
python -m src
```

To run the tests
```
python -m src.tests
```

To run the program in Docker
```
docker build -t cindicator .
docker run -v ./logs:/app/logs --rm cindicator
```

To run the tests
```
docker run --rm cindicator python3 -m src.tests
```