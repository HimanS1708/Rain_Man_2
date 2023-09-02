# FastAPI
The *app.py* uses **FastAPI** for receiving the inputs and sending the solutions (solved using *algorithm.py*)
## Installation
For installing **FastAPI**, run the following commands:
* Installing **FastAPI** using *pip* command
```bash
python -m pip install fastapi
```
* Installing **uvicorn[standard]**, a server for running **FastAPI**
```bash
python -m pip install uvicorn[standard]
```
## Running
For running *app.py* use the **uvicorn[standard]** server
```bash
uvicorn app:app --reload
```