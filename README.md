# melp_python_backend

API REST CRUD para restaurantes y búsqueda en un área circular de todos los restaurantes registrados en la base de datos.
Esta API funciona pasando la latitud y radio para buscar cuántos restaurantes se encuentran en el área, el promedio de la calificación de todos los restaurantes encontrados y la desviación estándar de las calificaciones de cada restaurante.

Esta aplicación cuenta con una imagen alojada en Docker Hub: https://hub.docker.com/r/christianleon/melp_backend
<br>

Colección de Postman: https://elements.getpostman.com/redirect?entityId=15002794-70a99fa5-fc20-420c-9e03-28aa6a744a85&entityType=collection

Los endpoints son:

* Obtener un restaurante por ID: `/restaurant/:restaurant_id`
* Crear un restaurante: `/restaurant/`
* Actualizar un restaurante: `/restaurants/:restaurant_id/`
* Eliminar un restaurante: `/restaurants/:restaurant_id/`
* Obtener restaurantes en un radio: `/restaurant/statistics?latitude=x&longitude=y&radius=z`
* Importar restaurantes desde CSV: `/restaurant/import`
   * Es muy importante que para que el import CSV funcione las columnas del CSV estén nombradas correctamente: 
      * id
      * rating
      * name
      * site
      * email
      * phone
      * street
      * city
      * state
      * latitude
      * longitude
    *  Se debe enviar el archivo mediante POST con el body de tipo form-data bajo el nombre de csv-file

## Requisitos para levantar la API
* Tener instalado Docker
* Tener instalado Docker Compose
* Contar con una cuenta en Docker Hub e iniciar sesión a través de la consola con el comando "docker login"

## Instrucciones para levantar la API para pruebas 
* Una vez cumplidos los requisitos simplemente se debe ejecutar el comando <b>docker-compose -f ./docker-compose.test.yml up melp</b> y este se encargará de recuperar las imágenes y levantar la API en conjunto a la base de datos.

## Instrucciones para levantar la API para desarrollo 
* Una vez cumplidos los requisitos simplemente se debe ejecutar el comando <b>docker-compose -f docker-compose.yml  up --build</b> y este se encargará de construir la imagen para levantar el contenedor basado en los cambios que se hayan realizado en el código.
## Posibles errores
  * En ocasiones, la creación del contenedor de la API se adelanta y trata de ejecutar comandos cuando el contenedor de la base de datos aún no está listo. Tras el error, basta con volver a ejecutar el comando para levantar la aplicación, ya sea en modo de prueba o desarrollo y funcionará con normalidad.
