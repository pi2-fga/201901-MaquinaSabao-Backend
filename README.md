## API Máquina de Sabão

#### Pre-requisites:
- docker

### To construct docker image:
```
$ docker build . -t maquina-sabao
```

### To run docker:
```
$ docker run --name maquina-sabao -d maquina-sabao
```

### To execute migrations:
```
$ docker exec -it maquina-sabao python manage.py makemigrations
```

```
$ docker exec -it maquina-sabao python manage.py migrate
```

### To run docker bash:
```
$ docker run -it maquina-sabao bash
```
