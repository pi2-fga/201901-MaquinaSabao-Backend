#### Pre-requisites:
- docker

### To construct docker image:
```
$ docker build . maquina-sabao
```

### To run docker:
```
docker run maquina-sabao --name maquina-sabao
```

### To execute migrations:
```
docker exec --it maquina-sabao python manage.py makemigrations
```

```
docker exec --it maquina-sabao python manage.py migrate
```

### To run docker bash:
```
docker run -it maquina-sabao bash
```
