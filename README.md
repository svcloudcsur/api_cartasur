# API Cartasur

## Introducción

## Instalación / Docker [development]

La API está montada sobre dos máquinas Docker corriendo Flask framework y PostgreSQL. El proceso de instalación se explica para Linux / MacOS, ya que ambos sistemas operativos deberían funcionar de manera similar. Se aclara que esto sólo funciona para modo desarrollo porque en producción seguramente se requiera otro tipo de instalación de acuerdo al cloud elegido o el tipo de instalación que se realice.

**1. Instalar Docker**: Como primera medida hay que instalar Docker para el sistema operativo host.

**2. Configurar el archivo `.env`**: En el directorio se encuentra un archivo `.env.sample` que tiene las variables de entorno para cada uno de los containers de docker.

**2. Levantar los servicios**: En development se trabajó con `docker-compose` con lo cual una vez instalado docker y configuradas las variables de entorno lo único que habría que correr es:

``` shell
docker-compose up
```

# Accediendo a la base de datos

Una vez que levantan los containers, es posible acceder a la base de datos haciendo lo siguiente:

``` shell
docker-compose exec database bash

```

y dentro del container se puede ejecutar:

``` shell
$ mongo -u $MONGO_INITDB_ROOT_USERNAME -p $MONGO_INITDB_ROOT_PASSWORD
```

Posteriormente hay que ejecutar esto para poder acceder a la base de datos propiamente dicha:

``` shell
> use db_cartasur
switched to db db_cartasur
```

# API Endpoints

La aplicación cuenta con varios endpoints en su API divididos por versión. Si bien al momento de escribir esta documentación sólo existe la `v1` (versión 1) de la API, potencialmente si hay cambios en las versiones y estas no fueran retrocompatibles habría que utilizar un versionado posterior.

## GET /ping

Este endpoint es un chequeo de que la aplicación está ejecutando. La respuesta debe ser 200 y el cuerpo puede o no tener una respuesta.


## GET /api/v1/ping

Este endpoint es otro chequeo de que la aplicación está funcionando. Se agrega sólo a efectos de probar la v1. Puede deprecarse posteriormente.

## POST /api/v1/clientes

Este endpoint recibe un solo parámetro "file" que tiene que contener el archivo de _clientes_ que desea reemplazar los cuotas de la base de datos.

## POST /api/v1/creditos

Este endpoint recibe un solo parámetro "file" que tiene que contener el archivo de _creditos_ que desea reemplazar los cuotas de la base de datos.

## POST /api/v1/cuotas

Este endpoint recibe un solo parámetro "file" que tiene que contener el archivo de _cuotas_ que desea reemplazar los cuotas de la base de datos.

## POST /api/v1/pagos

Este endpoint recibe un solo parámetro "file" que tiene que contener el archivo de _pagos_ que desea reemplazar los pagos de la base de datos.

## PUT /api/v1/train

Este endpoint gatilla el proceso de predicción. Este proceso puede ser largo, con lo cual generará un proceso asincrónico dentro del servidor para entrenar el modelo.

## POST /api/v1/predict

Este endpoint tomará datos de variables independientes sobre las cuales se desea obtener algún tipo de predicción basadas en el modelo entrenado.
