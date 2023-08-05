# xtapi
xtapi base on FastAPI

## Install

```bash
pip install xtapi
```

## demo

```python
# main.py
from xtapi import MainApp

app = MainApp()

if __name__ == '__main__':
    app.run(name='main:app', reload=True)
```

## first api

```python
from xtapi import MainApp

app = MainApp()


@app.get("/")
async def root():
    return {"message": "Hello World"}
```


**Run server**

```bash
python main.py
```
