# Sistema de Biblioteca – API REST con FastAPI
Este proyecto es una API RESTful con una interfaz integrada que cumple la funcion de una libreria virtual abierta, donde el objetivo es simular una biblioteca personal donde cada usuario puede guardar libros, calificarlos y reseñarlos y donde un usuario administrador toma el control sobre el catálogo.

Todo está construido con FastAPI, usando modelos Pydantic, manejo de roles, autenticación con tokens tipo Bearer y un pequeño patrón Observer para registrar eventos importantes.

# 👉 caracteristicas

##  Usuarios comunes

- Registro de usuarios.

- Inicio de sesión con token Bearer.

- Rol de administrador con permisos especiales (editar, crear,eliminar del catalogo global)

- Biblioteca personal para cada usuario (excepto el administrador)
## usario administrador
al inicializar el servidor, se genera un usuario administrador por defecto:

| usuario             | contraseña                                                             |
| ----------------- | ------------------------------------------------------------------ |
| admini@biblioteca.com | admin123 |

## 📘 Libros

- catalogo de libros disponible en la interfaz principal

- Los usuarios pueden ver contenido y agregar libros a su biblioteca.

- Los administradores pueden agregar, editar y eliminar libros.

## ⭐ Reseñas

- Reseñas y calificaciones (1 a 5 estrellas)

- los libros muestran las reseñas dejadas por el usuario

## 🔔 Sistema de eventos 

Cada accion del usuario dentro del programa genera un evento, como por ejemplo:

- USUARIO_REGISTRADO

- LIBRO_CREADO

- RESEÑA_AGREGADA

El sistema del modelo observer generan logs y “notificaciones” dentro del programa

# 📂 Estructura general del proyecto
El proyecto se basa en un único archivo principal main.py, dentro de este archivo se encuentran:

- Modelos Pydantic
- Endpoints de FastAPI
- Lógica central mediante el LibraryFacade
- Observadores de eventos
- La interfaz HTML 
- Configuración de seguridad y autenticación

## ☁️despliegue en Azure
actualmente este proyecto ceunta con una version desplegada en azure:

[mipri.azurewebsites.net](mipri.azurewebsites.net)


## ▶️ instalacion local 

- clonar repositorio 

`git clone https://github.com/DAYANAOVALLE/calculadora-.git`

`cd calculadora-`
- Crear el entorno virtual

`python -m venv venv`

`source venv/bin/activate` (para linux/mac)

`source venv\Scripts\activate` (para windows)


- instalar dependencias 

`pip install fastapi uvicorn`

- Ejecutar el servidor

`uvicorn main:app --reload`

- entrar a la interfaz de fastapi
abre chrome (o cualquier otro navegador de confianza) y abre este link: 
http://127.0.0.1:8000

# 🗂️ Endpoints
- usuario (solo el usuario comun puede visualizarlo)
- admin (solo el administrador puede visualizarlo)
- publico(tanto el usuario comun como el administrador pueden visualizarlo)

| Método | Ruta                                  | Descripción       | Roles     |
| ------ | ------------------------------------- | ----------------- | ------- |
| GET    | `/api/v1/libros`                      | Lista libros      | publico |
| POST   | `/api/v1/libros`                      | Crear libro       | Admin   |
| GET    | `/api/v1/libros/{id}`                 | Ver un libro         | publico |
| PUT    | `/api/v1/libros/{id}`                 | Editar libro      | Admin   |
| DELETE | `/api/v1/libros/{id}`                 | Eliminar libro    | Admin   |
| POST   | `/api/v1/auth/login`                  | Iniciar sesión    | publico |
| POST   | `/api/v1/usuarios`                    | Registrar usuario | publico |
| GET    | `/api/v1/usuarios/me/biblioteca`      | biblioteca personal    | Usuario |
| POST   | `/api/v1/usuarios/me/biblioteca/{id}` | Agregar libro     | Usuario |
| DELETE | `/api/v1/usuarios/me/biblioteca/{id}` | Quitar libro      | Usuario |


## 🧩Autores

- [DayanaOvalle :3](https://github.com/DAYANAOVALLE)

- [Fernando1215](https://github.com/Fernando1215)

- [Santiago0242](https://github.com/Santiago0242)