# FastAPI Project

## Descripción
Este es un proyecto desarrollado en **FastAPI** que implementa una API para gestionar clientes, transacciones y planes. Utiliza **SQLModel** como ORM y se conecta a una base de datos SQLite.

## Requisitos Previos
Antes de ejecutar el proyecto, asegúrate de tener instalado:
- Python 3.10+
- pip (gestor de paquetes de Python)

## Instalación
Clona el repositorio y navega hasta el directorio del proyecto:

```sh
# Clonar el repositorio
git clone https://github.com/NovaPage/fastapi-proyect
cd curso-fastapi-proyect
```

Instala las dependencias necesarias:

```sh
pip install -r requirements.txt
```

## Configuración de la Base de Datos
El proyecto usa **SQLite** como base de datos. Para crear las tablas necesarias, asegúrate de ejecutar la aplicación por primera vez, ya que la función `create_all_tables` generará automáticamente la estructura de la base de datos.

## Ejecución del Proyecto
Para ejecutar la aplicación, usa el siguiente comando:

```sh
fastapi dev app/main.py
```

Esto iniciará el servidor de FastAPI en el puerto **8000** por defecto.

### Acceder a la API
Una vez que la aplicación se esté ejecutando, puedes acceder a la documentación interactiva en los siguientes enlaces:
- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Redoc UI**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## Endpoints Principales

### Raíz
- `GET /` → Devuelve un mensaje de bienvenida

### Gestión de Clientes
- `POST /customers/` → Crear un nuevo cliente
- `GET /customers/{id}` → Obtener datos de un cliente específico
- `PUT /customers/{id}` → Actualizar datos de un cliente
- `DELETE /customers/{id}` → Eliminar un cliente

### Gestión de Transacciones
- `POST /transactions/` → Crear una nueva transacción
- `GET /transactions/{id}` → Obtener una transacción específica

### Gestión de Planes
- `POST /plans/` → Crear un nuevo plan
- `GET /plans/{id}` → Obtener información de un plan

### Información de Hora por País
- `GET /time/{iso_code}` → Devuelve la hora actual según el código de país (ISO 3166-1 Alpha-2)
  - Ejemplo: `/time/CO` → Devuelve la hora actual en Colombia

### Gestión de Facturas
- `POST /Invoices/` → Crear una nueva factura

## Estructura del Proyecto

```
.
├── app/
│   ├── main.py        # Archivo principal con la configuración de la API
│   ├── routers/
│   │   ├── customers.py     # Endpoints relacionados con clientes
│   │   ├── transactions.py  # Endpoints relacionados con transacciones
│   │   ├── plans.py         # Endpoints relacionados con planes
├── requirements.txt   # Dependencias del proyecto
├── models.py      # Modelos de datos con SQLModel
├── db.py          # Configuración de la base de datos y dependencias
├── README.md          # Este archivo
```

## Dependencias
El proyecto usa las siguientes dependencias:
```txt
fastapi['standard']==0.115.8
sqlmodel==0.0.22
```
Puedes instalarlas con:
```sh
pip install -r requirements.txt
```

## Desarrollo y Contribución
Si deseas contribuir, sigue estos pasos:
1. Crea un **fork** del repositorio.
2. Crea una nueva rama con una mejora o corrección:
   ```sh
   git checkout -b feature/nueva-mejora
   ```
3. Realiza tus cambios y confírmalos:
   ```sh
   git commit -m "Descripción de la mejora"
   ```
4. Sube los cambios a tu repositorio remoto:
   ```sh
   git push origin feature/nueva-mejora
   ```
5. Abre un **Pull Request** en el repositorio principal.

## Licencia
Este proyecto está bajo la licencia **MIT**. Puedes ver más detalles en el archivo `LICENSE`.