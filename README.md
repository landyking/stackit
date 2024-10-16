#### update requirements.txt
use command `pipreqs $PWD`.

#### build docker image
`docker build -t stackit .`

#### run docker image

`docker run -p 8501:8501 stackit`
`docker run --rm -p 8501:8501 stackit`
