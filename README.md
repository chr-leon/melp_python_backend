# melp_python_backend


API REST CRUD para restaurantes y búsqueda en un área circular de todos los restaurantes registrados en la base de datos.
Esta API funciona pasando la latitud y radio para buscar cuántos restaurantes se encuentran en el área, el promedio de la calificación de todos los restaurantes encontrados y la desviación estándar de las calificaciones de cada restaurante.

Esta aplicación cuenta con una imagen alojada en docker hub: https://hub.docker.com/r/christianleon/melp_backend
<br>

Postman collection: https://elements.getpostman.com/redirect?entityId=15002794-70a99fa5-fc20-420c-9e03-28aa6a744a85&entityType=collection

Los endpoints son:

* Obtener un restaurante por id: /restaurant/:restaurant_id
* Crear un restaurante: /restaurant/
* Actualizar un restaurante: /restaurants/:restaurant_id/
* Eliminar un restaurante: /restaurants/:restaurant_id/
* Obtener restaurantes en un radio: /restaurant/statistics?latitude=x&longitude=y&radius=z
* Importar restaurantes desde CSV: /restaurant/import
   * Es muy importante que para que el import CSV funcione las columnas del CSV esten nombradas correctamente: 
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
    *  Se debe enviar el archiv mediante post con el body de tipo form-data bajo el nombre de csv-file

## Requisitos para levantar la API
* Tener instalado docker
* Tener instalado docker compose
* Contar con una cuenta en Docker hub e iniciar session atravez de consola con el comando "docker login"

## Instrucciones para Levanta la API para pruebas 
* Una vez cumplido los requisitos simplemente se debe ejecutar el comando "docker-compose up melp -f docker-compose.test.yml" y este se encargará de recuperar las images y levantar la API en conjunto a la base de datos.

## Instrucciones para Levanta la API para desarrollo 
* Una vez cumplido los requisitos simplemente se debe ejecutar el comando "docker-compose up melp --build -f docker-compose.yml" y este se encargará de construir la imagen para levantar el container basado en los cambios que se hayan realizado en codigo.
