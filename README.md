# Path of Light (Fermat's Principle)

This project is a Streamlit app that demonstrates the classic **fish-underwater to eye-in-air** refraction example from Feynman Lectures, using Fermat's principle (minimum travel time).

## Install

### 1) Create and activate a virtual environment

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows (PowerShell)**

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2) Install dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Run the app

```bash
streamlit run app.py
```

Then open the local URL shown in the terminal (usually `http://localhost:8501`).

## Troubleshooting

- If `streamlit` is not found, activate your virtual environment again and reinstall dependencies.
- If installation fails behind a proxy/firewall, configure your pip proxy/index settings and retry.
- If port `8501` is in use, run:

```bash
streamlit run app.py --server.port 8502
```
