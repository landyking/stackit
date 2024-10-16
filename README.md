#### update requirements.txt
```shell
pipx install creosote
creosote --deps-file requirements.txt --path . --venv .venv
pip3 freeze > requirements.txt
```

#### build docker image
```shell
docker build -t landykingdom/stackit .
```

#### run docker image

```shell
docker run -p 8501:8501 stackit
# or
docker run --rm -p 8501:8501 stackit
```
