# SESHIA-

Seshia es una aplicación web desarrollada con Django que permite a las usuarias realizar el seguimiento de su ciclo menstrual y administrar sus finanzas personales desde una única plataforma.

El sistema integra información relacionada con los ciclos menstruales, síntomas diarios, ingresos y gastos para generar información útil que permita identificar posibles relaciones entre el comportamiento financiero y las diferentes fases del ciclo menstrual.

El proyecto está desarrollado siguiendo una arquitectura modular basada en dominios de negocio, facilitando el mantenimiento, la escalabilidad y el trabajo colaborativo.

## Cómo se ejecuta?
```bash
docker compose up --build -d
```

si hiciste cambios
```bash
# paso 1 
docker compose down 

# paso 2
docker compose up
```

---

# Características

- Registro e inicio de sesión mediante correo electrónico.
- Gestión de perfiles de usuario.
- Registro de ciclos menstruales.
- Seguimiento diario de síntomas, estado de ánimo y nivel de energía.
- Administración de ingresos y gastos.
- Clasificación mediante categorías financieras.
- Asociación automática de transacciones con el ciclo y la fase correspondiente.
- Generación de insights personalizados.
- Interacciones asíncronas utilizando AJAX (Fetch API).

---

# Tecnologías utilizadas

## Backend

- Python 3.13
- Django 5.1
- Django ORM

## Frontend

- HTML5
- CSS3
- JavaScript (Vanilla JS)
- AJAX (Fetch API)
- Django Templates

## Base de datos

- PostgreSQL 17

## Contenedores

- Docker
- Docker Compose

---

# Requisitos

Antes de ejecutar el proyecto es necesario contar con:

- Docker
- Docker Compose
- Git

---

# Instalación

Clonar el repositorio:

```bash
git clone <URL_DEL_REPOSITORIO>
```

Ingresar al directorio del proyecto:

```bash
cd SESHIA-
```

Construir las imágenes:

```bash
docker compose build
```

Levantar los contenedores:

```bash
docker compose up
```

Aplicar las migraciones:

```bash
docker compose exec django-web python manage.py migrate
```

Crear un superusuario (opcional):

```bash
docker compose exec django-web python manage.py createsuperuser
```

La aplicación estará disponible en:

```
http://localhost:8000
```

---

# Variables de entorno

Crear un archivo `.env` en la raíz del proyecto con las siguientes variables:

```env
DJANGO_SECRET_KEY=

DEBUG=

DJANGO_LOGLEVEL=

DJANGO_ALLOWED_HOSTS=

DATABASE_ENGINE=

DATABASE_NAME=

DATABASE_USERNAME=

DATABASE_PASSWORD=

DATABASE_HOST=

DATABASE_PORT=
```

Estas variables permiten configurar el proyecto sin exponer información sensible dentro del código fuente.

---

# Base de datos

Seshia utiliza PostgreSQL 17 como sistema gestor de base de datos.

La base de datos se ejecuta dentro de un contenedor Docker y expone el puerto **5433** del equipo anfitrión hacia el puerto **5432** del contenedor PostgreSQL.

Toda la estructura de la base de datos es administrada mediante el sistema de migraciones de Django.

Comandos útiles:

Crear migraciones:

```bash
docker compose exec django-web python manage.py makemigrations
```

Aplicar migraciones:

```bash
docker compose exec django-web python manage.py migrate
```

---

# Arquitectura

El proyecto implementa la arquitectura **MVT (Model - View - Template)** propia de Django y organiza el código siguiendo un enfoque **Domain-Driven Design (DDD)**.

Cada dominio del negocio se encuentra aislado dentro de una aplicación independiente, permitiendo una mejor organización del código, desarrollo paralelo entre equipos y una mayor facilidad para escalar el sistema.

Los dominios principales son:

- Users
- Cycles
- Finances
- Insights

La lógica de negocio se encuentra desacoplada de las vistas mediante una capa de servicios.

El flujo principal de una petición es:

```
URL
    │
    ▼
View
    │
    ▼
Form
    │
    ▼
Service
    │
    ▼
Model
    │
    ▼
PostgreSQL
```

De esta manera:

- **Forms** validan los datos recibidos.
- **Views** coordinan la solicitud HTTP.
- **Services** contienen la lógica del negocio.
- **Models** representan las entidades persistentes.
- **PostgreSQL** almacena la información.

---

# Estructura del proyecto

```text
seshia/
│
├── manage.py                          # Punto de entrada de Django
│
├── seshia/                            # Configuración principal del proyecto
│   ├── settings.py                    # Configuración global
│   ├── urls.py                        # Rutas principales
│   ├── wsgi.py                        # Servidor WSGI
│   └── asgi.py                        # Servidor ASGI
│
├── apps/                              # Aplicaciones del dominio
│   │
│   ├── base/                          # Configuración compartida
│   │
│   ├── users/                         # Gestión de usuarios y autenticación
│   │   ├── forms/
│   │   ├── managers/
│   │   ├── migrations/
│   │   └── models/
│   │
│   ├── cycles/                        # Gestión de ciclos menstruales
│   │   ├── forms/
│   │   ├── migrations/
│   │   ├── models/
│   │   ├── services/
│   │   ├── urls.py
│   │   └── views.py
│   │
│   ├── finances/                      # Gestión financiera
│   │   ├── forms/
│   │   ├── migrations/
│   │   ├── models/
│   │   ├── services/
│   │   ├── urls.py
│   │   └── views.py
│   │
│   └── insights/                      # Generación de insights
│       ├── migrations/
│       ├── models/
│       ├── services/
│       ├── tests/
│       ├── urls.py
│       └── views.py
│
├── static/                            # Recursos estáticos
│   ├── css/
│   ├── js/
│   └── img/
│
├── templates/                         # Plantillas HTML
│
├── .env                               # Variables de entorno
├── Dockerfile                         # Imagen de la aplicación
├── docker-compose.yml                 # Orquestación de contenedores
├── requirements.txt                   # Dependencias
└── .gitignore
```

---

# Organización del proyecto

Cada dominio del negocio se encuentra encapsulado dentro de su propia aplicación Django.

Cada dominio del negocio (usuarios, ciclos, finanzas, insights) vive en su propia app dentro de apps/. Esto permite desarrollo en paralelo,
aislamiento de responsabilidades y la posibilidad de extraer una app a un microservicio en el futuro si fuera necesario.

A diferencia de la estructura tradicional de Django, donde todos los modelos se almacenan en un único archivo `models.py`, este proyecto implementa un enfoque modular donde cada entidad posee su propio archivo dentro del directorio `models/`. Esto evita conflictos en git cuando varias personas trabajan en distintos
modelos de la misma app.
Esta decisión permite:

- Mejor legibilidad del código.
- Menor cantidad de conflictos durante el desarrollo colaborativo.
- Mayor facilidad para localizar entidades específicas.
- Escalabilidad conforme aumenta el tamaño del proyecto.

Asimismo, la lógica de negocio se centraliza en la carpeta `services`, evitando sobrecargar las vistas y favoreciendo la reutilización de código.

---

# Autenticación

El proyecto utiliza un modelo de usuario personalizado basado en `AbstractUser`.

La autenticación se realiza mediante la dirección de correo electrónico en lugar del nombre de usuario tradicional de Django.

---

# Autoras
- Luisa de la Rosa
- Melissa Garrido
- Yesica Rodriguez
