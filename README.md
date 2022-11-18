# Librator

Proyecto para la práctica de RIWS con la implementación del *crawler* sobre la información de libros de las webs www.planetadelibros.com y www.agapea.com

## Ejecución mediante Docker

Para ejecutar el proyecto en su totalidad mediante Docker (versión 20), basta con utilizar el fichero docker-compose de la raíz:

```bash
docker-compose up -d
```

Esto levantará los servicios de ElasticSearch, Kibana, Splash, ambos *crawlers* y el cliente web.

**NOTA: El cliente web puede tardar varios minutos (sobre 10 minutos) en estar disponible, al tener que descargar todas las dependencias utilizadas dentro del contenedor.**

## Ejecución manual

Si por el contrario, se prefiere lanzar todos los servicios a mano, habría que seguir los siguientes pasos para cada uno de ellos:

### ElasticSearch

Se puede levantar este servicio mediante docker-compose, aunque se pueden descargar los ejecutables y establecer las configuración de seguridad y de CORS de la misma forma que en el docker-compose.yml.

### Kibana

Mismo caso que para el servicio anterior.

### Splash

Se puede utilizar el servicio definido en el docker-compose o simplemente descargar y lanzar la imagen de DockerHub.

### Crawler

El funcionamiento del *web crawler* está probado con Python 3.9, por lo que se recomienda tener esta versión instalada. Además, habría que instalar las siguientes dependencias (para Windows se recomienda utilizar el entorno Anaconda):

```bash
pip install scrapy
pip install scrapy_splash
pip install elasticsearch
```

**NOTA: Si se elige esta forma de despliegue, se deben cambiar las URLs de los hosts de ElasticSearch y Splash a http://localhost:9200 y http://localhost:8050 respectivamente, en el fichero de configuración settings.py**

A continuación, desde terminales diferentes en el directorio /scrapper, se pueden iniciar ambos *spiders*:

```bash
scrapy crawl agapea
scrapy crawl planetadelibros
```

### Cliente

Para ejecutar el cliente se recomienda utilizar la versión de Node 14.15, fácilmente obtenible a través de la herramienta **nvm**.

A continuación, se deben instalar las dependencias del sistema:

```bash
npm install
```

Por último, ya se puede lanzar el cliente, que estará disponible en la máquina local en el puerto 1234.

```bash
npm run serve
```
