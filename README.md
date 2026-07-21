# SESHIA

Seshia es una aplicación web desarrollada con Django que permite a las usuarias realizar el seguimiento de su ciclo menstrual y administrar sus finanzas personales desde una única plataforma. El sistema integra información relacionada con los ciclos menstruales, síntomas diarios, ingresos y gastos para generar información útil que permita identificar posibles relaciones entre el comportamiento financiero y las diferentes fases del ciclo menstrual.

Su objetivo es ayudar a entender como el ciclo influye en el estado de animo, la energia y los patrones de gasto a traves de insights generados automaticamente.

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

- Docker Desktop instalado y corriendo
- Git

---

# Instalación

### Con Docker (recomendado)

1. Clonar el repositorio:

```bash
git clone <URL_DEL_REPOSITORIO>
```

Ingresar al directorio del proyecto:

```bash
cd SESHIA-
```

2. Configurar variables de entorno:
```bash
   cp .env.example .env
```

Abre .env y define tus propios valores. Como mínimo debes cambiar DATABASE_USERNAME y DATABASE_PASSWORD por unos propios, el motor de base de datos debe ser siempre PostgreSQL.

3. Levantar los contenedores
```bash
   docker compose up --build -d
```

4. Aplicar las migraciones

```bash
   docker compose exec django-web python manage.py migrate
```

5. Crear un superusuario (opcional):

```bash
docker compose exec django-web python manage.py createsuperuser
```

6. La aplicación estará disponible en:

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

### Sin Docker

bash
# Clonar
git clone https://github.com/LaoraSad/SESHIA-.git
cd SESHIA-

# Entorno virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Dependencias
pip install -r requirements.txt

# Base de datos
python manage.py migrate
python manage.py seed_data

# Servidor
python manage.py runserver


### seed_data

El comando `seed_data` crea:

- Un **superusuario** (`admin` / `admin123`)
- Las **categorias financieras** por defecto (Alimentacion, Transporte, Ocio, Cuidado menstrual, etc.)
- Un `AppSettings` con la **fecha actual simulada**
- Sintomas y fases del ciclo predefinidos



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


## Arquitectura del proyecto


SESHIA/
│
├── seshia/                          # Configuracion del proyecto Django
│   ├── settings.py                  # Configuracion general
│   ├── urls.py                      # Rutas raiz (monta las apps)
│   ├── wsgi.py / asgi.py            # Entry points de produccion
│   └── ...
│
├── apps/                            # Codigo de la aplicacion
│   │
│   ├── base/                        # Utilidades transversales
│   │   ├── services/
│   │   │   └── date_service.py      # Sistema de fecha simulada
│   │   │       ├── get_current_date()    # Obtiene la fecha actual simulada
│   │   │       ├── next_day()            # Avanza un dia
│   │   │       └── previous_day()        # Retrocede un dia
│   │   ├── context_processors.py    # Expone current_date a todas las templates
│   │   ├── views.py                 # HomeView (inicio + generacion de insight)
│   │   └── urls.py
│   │
│   ├── users/                       # Autenticacion y perfil
│   │   ├── models/
│   │   │   └── user.py              # User model personalizado (email, full_name)
│   │   ├── managers/
│   │   │   └── user_manager.py      # QuerySet manager con create_user, create_superuser
│   │   ├── forms/
│   │   │   ├── register_form.py     # Registro con email unico
│   │   │   ├── login_form.py        # Autenticacion por email
│   │   │   └── profile_form.py      # Edicion de perfil
│   │   └── views.py                 # RegisterView, LoginView, ProfileView
│   │
│   ├── cycles/                      # Ciclo menstrual y registros diarios
│   │   ├── models/
│   │   │   ├── cycle.py             # Ciclo: start_date, end_date, status (ACTIVE/COMPLETED)
│   │   │   ├── cycle_phase.py       # Relacion muchos a muchos: Ciclo -> Fase (con fechas)
│   │   │   ├── daily_log.py         # Registro diario: energia, animo, notas, sintomas
│   │   │   ├── phase.py             # Catalogo de fases (menstrual, folicular, ovulatoria, lutea)
│   │   │   ├── symptom.py           # Catalogo de sintomas
│   │   │   └── symptom_category.py  # Categorias de sintomas
│   │   ├── services/
│   │   │   ├── cycles_service.py    # CRUD ciclos, get_active_cycle, register_period
│   │   │   └── daily_log_service.py # CRUD daily logs
│   │   ├── forms/
│   │   │   ├── cycle_form.py        # Registro de nuevo periodo
│   │   │   └── daily_log_form.py    # Registro diario (energia, animo, sintomas, notas)
│   │   └── views.py
│   │
│   ├── finances/                    # Transacciones financieras
│   │   ├── models/
│   │   │   ├── transaction.py       # Transaccion: monto, fecha, categoria, ciclo, fase
│   │   │   └── category.py          # Categoria: nombre, tipo (income/expense), icono
│   │   ├── services/
│   │   │   ├── transaction_service.py # CRUD transacciones + filtros por ciclo/usuario
│   │   │   └── category_service.py    # CRUD categorias
│   │   ├── forms/
│   │   │   ├── expense_form.py      # Formulario de gasto
│   │   │   ├── income_form.py       # Formulario de ingreso
│   │   │   └── category_form.py     # Formulario de categoria
│   │   └── views.py                 # TransactionListView (+ selector de ciclo)
│   │
│   ├── insights/                    # Motor de insights
│   │   ├── models/
│   │   │   └── insight.py           # Insight: tipo, codigo, titulo, mensaje, fase, ciclo
│   │   ├── services/
│   │   │   ├── rules.py             # Catalogo de reglas (dataclasses inmutables)
│   │   │   │   ├── CYCLE_RULES      # Reglas de historial de ciclos
│   │   │   │   ├── DAILY_LOG_RULES  # Reglas de registros diarios
│   │   │   │   ├── FINANCE_RULES    # Reglas de finanzas
│   │   │   │   └── MIXED_RULES      # Reglas de patrones cruzados
│   │   │   ├── conditions.py        # Evaluacion de condiciones (cada funcion = 1 condicion)
│   │   │   └── insight_service.py   # Generacion, seleccion y creacion de insights
│   │   │       ├── generate_insight()    # Punto de entrada: evalua y genera
│   │   │       ├── _get_applicable_rules() # Filtra reglas cuya condicion es True
│   │   │       ├── _select_best_rule()    # Elige la de mayor prioridad
│   │   │       ├── _resolve_insight_phase() # Asigna la fase actual del ciclo
│   │   │       └── _create_insight()      # Persiste el insight en DB
│   │   ├── tests/                   # Tests del motor de insights
│   │   └── views.py                 # InsightView (listado), InsightHistoryView
│   │
│   └── templatetags/                # Tags personalizados de Django
│
├── templates/                       # Templates HTML agrupadas por app
│   ├── base.html                    # Layout base con Tailwind + barra de navegacion
│   ├── home.html                    # Pagina de inicio con fecha simulada e insight
│   ├── cycles/                      # Templates de ciclos
│   │   ├── form.html               # Registro de nuevo periodo
│   │   ├── log_list.html           # Historial de daily logs
│   │   └── log_form.html           # Formulario de daily log
│   ├── finances/                    # Templates de finanzas
│   │   ├── list.html               # Lista de transacciones + selector de ciclo
│   │   ├── form.html               # Formulario de gasto/ingreso
│   │   ├── partials/               # Fragmentos reutilizables
│   │   └── categories/             # CRUD de categorias
│   └── insights/                    # Templates de insights
│       ├── detail.html             # Ultimos 5 insights del ciclo activo
│       └── history.html            # Historial completo de insights
│
├── statics/                         # Archivos estaticos
│   ├── css/
│   ├── js/
│   └── img/
│
├── manage.py                        # Entry point de Django
├── Dockerfile                       # Imagen de produccion/desarrollo
├── docker-compose.yml               # Servicios (web + db opcional)
├── requirements.txt                 # Dependencias Python
└── README.md


## Sistema de fecha simulada

En desarrollo, Seshia no usa `date.today()` sino una fecha almacenada en DB (`AppSettings.current_date`). Esto permite:

- **Avanzar rapido** para probar insights, fases del ciclo y tendencias financieras
- **Retroceder** si es necesario
- **Tests deterministas** que no dependen del dia real

El boton para avanzar/retroceder el dia esta en la esquina superior derecha de la pagina de inicio.


HomeView
  └── next_day()  →  AppSettings.current_date += 1 dia
                      → se persiste en DB
                      → todos los servicios usan get_current_date()


## Sistema de insights

### Que es un insight

Un insight es una observacion personalizada que correlaciona los datos del usuario. Por ejemplo:

- *"Llevas 5 dias sin registrar tu dia a dia"*
- *"En este ciclo tus gastos aumentaron respecto al ciclo anterior"*
- *"En los dias con poca energia, tus gastos se concentran en Alimentacion"*

### Catalogo de reglas

Las reglas se definen en `rules.py` como dataclasses inmutables:

python
@dataclass(frozen=True)
class InsightRule:
    code: str          # Identificador unico (DAY013, FIN007, MIX001, etc.)
    type: InsightType  # CYCLE | DAILY_LOG | FINANCE | MIXED
    phase: PhaseType   # Fase del ciclo a la que aplica (o None si es general)
    title: str         # Titulo mostrado al usuario
    message: str       # Cuerpo del insight (puede contener {value}, {phase}, etc.)
    condition: str     # Nombre de la funcion en conditions.py que la evalua
    priority: int      # A mayor numero, mayor prioridad (1-6)


### Tipos de reglas y prioridades

| Tipo | Prioridad | Que detecta |
|---|---|---|
| `FINANCE` | 6 | Inactividad financiera (FIN007, FIN010), comparacion entre ciclos (FIN001, FIN002) |
| `FINANCE` | 5 | Analisis del ciclo actual (FIN008, FIN009, FIN013, FIN014), tendencias (FIN011, FIN012) |
| `DAILY_LOG` | 5 | Inactividad de registro (DAY013) |
| `DAILY_LOG` | 3 | Patrones del ciclo actual (DAY009-DAY012) |
| `MIXED` | 3 | Patrones cruzados (energia + gastos, animo + categoria) |
| `DAILY_LOG` | 2 | Patrones de ciclos anteriores (DAY001-DAY006) |
| `CYCLE` | 1 | Historial de ciclos (CYC001-CYC008) |

### Ciclo de generacion


Usuario visita Home
  │
  ├── ¿Mismo dia y sin datos nuevos?
  │     └── Si → devuelve el insight actual (no regenera)
  │
  └── No → evalua reglas:
        │
        ├── 1. _get_applicable_rules()
        │     └── Recorre ALL_RULES, ejecuta cada condicion
        │         Si la condicion devuelve True (o un valor), la regla es aplicable
        │
        ├── 2. Filtra por ultima accion:
        │     ├── Ultima accion = Log diario
        │     │     └── Solo reglas NO FINANCE (CYCLE + DAILY_LOG + MIXED)
        │     ├── Ultima accion = Transaccion
        │     │     └── Solo reglas FINANCE
        │     └── Sin acciones
        │           └── Todas las reglas compiten
        │
        ├── 3. Salta la regla del insight actual
        │     └── Evita que se repita el mismo insight si hay otra opcion valida
        │
        ├── 4. _select_best_rule()
        │     └── max(applicable, key=priority)
        │
        └── 5. _create_insight()
              └── Persiste el Insight en DB


### Anatomia de una condicion

Cada condicion es una funcion en `conditions.py` que recibe el ciclo actual (o el usuario, si es tipo CYCLE) y devuelve:

- `False` si la condicion no se cumple
- Un `string` si se cumple (se inyecta en `{value}` del mensaje)
- Un `dict` si se cumple con multiples valores (se inyectan como `{clave}`)
- `True` si se cumple pero no hay valor que inyectar

python
def days_without_logging_streak(cycle):
    """DAY013: Devuelve los dias desde el ultimo daily log (>= 3)."""
    today = get_current_date()
    last_log = cycle.daily_logs.order_by("-log_date").first()
    if last_log is None:
        days_since = (today - cycle.start_date).days
    else:
        days_since = (today - last_log.log_date).days
    if days_since >= 3:
        return str(days_since)  # Se inyecta en {value}
    return False


## Modelo de datos


User (1) ──── (N) Cycle
  │                  │
  │                  ├── (N) CyclePhase  ── Phase
  │                  │
  │                  ├── (N) DailyLog  ── (M) Symptom
  │                  │
  │                  └── (N) Transaction  ── Category
  │
  └── (N) Insight  ── Phase


- **Cycle**: Representa un ciclo menstrual (inicio, fin, duracion esperada/real, estado)
- **CyclePhase**: Asigna una fase (menstrual, folicular, etc.) a un rango de fechas dentro del ciclo
- **DailyLog**: Registro diario con energia, animo, notas, y sintomas asociados
- **Transaction**: Gasto o ingreso con monto, fecha, categoria, y asociacion al ciclo/fase
- **Category**: Categoriza transacciones como ingreso o gasto, con icono emoji
- **Insight**: Insight generado con tipo, codigo, titulo, mensaje, fase y ciclo
- **AppSettings**: Almacena la fecha simulada global

## Comandos utiles

```bash

# Resetear base de datos
docker compose down
Remove-Item data/db.sqlite3  # Windows
docker compose up --build
```

# Autoras
- Luisa de la Rosa
- Melissa Garrido
- Yesica Rodriguez
