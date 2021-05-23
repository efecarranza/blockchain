# Getting Started

1. Activate the virtual environment:
```
source blockchain-env/bin/activate
```
2. Install all packages:
```
pip3 install -r requirements.txt
```

3. Running Tests

```
python3 -m pytest tests/
```

4. Run the application and API

Make sure to activate the virtual environment.

```
python -m backend.app
```

# Running a Perr Instance

Make sure to activate the virtual environment.

```
export PEER=True && python -m backend.app
```

# Run the Front-End

In the frontend directory:
```
npm run start
```

# Seed the backend with data

```
export SEED_DATA=True && python3 -m backend.app
```
