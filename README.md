#### update requirements.txt
```shell
pipx install creosote
creosote --deps-file requirements.txt --path . --venv .venv
pip3 freeze > requirements.txt
```

#### build docker image
`docker build -t stackit .`

#### run docker image

`docker run -p 8501:8501 stackit`
`docker run --rm -p 8501:8501 stackit`
