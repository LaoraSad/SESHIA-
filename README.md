# SESHIA-
Aplicación web que integra el seguimiento del ciclo menstrual con la gestión y el análisis de finanzas personales.


GUIA DE PUSH Y PULL PARA GIT HUB

Desde el terminal van a hacer lo siguiente:

1. Crean una carpeta o eligen una carpeta donde quieran guardar lo que van a trabajar 
2. Le dan click derecho a la carpeta y abren el terminal 
3. Desde el terminal van a CLONAR el repositorio 

 	 	git clone https://github.com/LaoraSad/SESHIA-.git

4. Esto descarga el proyecto completo a tu computador y les creará una carpeta llamada 

   		SESHIA

6. Se van a ella via terminal con el comando:

   		cd SHESIA


  Para crear una rama van a utilizar el siguiente comando, esto con el fin de revisar los push request, al final el SRCUM va a revisar cada commit que decidan       enviar y sera quien apruebe o niegue el push  

  # esto le dice a git, básicamente créame esta rama chamo y cambiate directamente a ella 
  git checkout -b feature/inicio 


  
Las ramas ya están creadas en el main voy a dejar la base, así que van a hacer el primer clone desde main, después en sus computadores 
van a ir trabajando lo que les corresponda, una vez que ya tengan un cambio realizado y funcional pueden hacer el push 

7. Antes de tocar cualquier archivo, el dev se mueve a developer y se asegura de tener la versión mas reciente del 
proyecto, simplemente usa el comando:

	# Te mueve a la rama developer. Es como cambiar de pestaña o cambiar de hoja
		git checkout development

8. Lo siguiente es tener los cambios más recientes del proyecto, para eso, usamos SIEMPRE el comando:

	# descarga los cambios mas recientes que otros hayan subido, siempre háganlo antes de empezar a trabajar para no quedar desactualizados.

		git pull origin development


9. Cada vez que avancen en algo, deben guardar su progreso, por el momento trabajaremos todos los avances en la rama secondary, para guardarlo, usan estos comandos:

 # Añadir los archivos, el comando de toda la vida
	git add .
	
Si lo hacen desde el vs code les pide un commit que es opcional (tengan mucho cuidado cuando hagan los push desde vs code porque se pueden guardar duplicados y eso es una demora para arreglarlo TTnTT)

# Básicamente le decimos a git, envíame los cambios desde mi pc hasta la rama X
	git push origin development


# Guía de Contribución

## Estrategia de Ramas

Con el nombre nos guiaremos para saber que equipo desarrollo la rama, el prefijo UI será para los frontends y el prefijo API por los backends

	main
	└── develop
	    ├── feature/api-auth
	    ├── feature/api-users
	    ├── feature/api-products
	    ├── feature/ui-login
	    ├── feature/ui-dashboard
	    ├── feature/ui-profile
	    ├── fix/api-pagination
	    ├── fix/ui-navbar
	    └── refactor/database

#### Estructura

- **tipo:** Indica el propósito de la rama.
- feature → nueva funcionalidad
- fix → corrección de errores
- refactor → mejora interna sin cambiar comportamiento

- **prefijo:** Identifica el área del proyecto.
  - `ui` → Frontend
  - `api` → Backend (Django API)
- **descripción-corta:** Nombre breve en kebab-case que describa la funcionalidad o cambio.

| Tipo | Prefijo (ui/api) | Descripción | Ejemplo |
|------|-------------------|-------------|---------|
| `feature` | `api` | Nueva funcionalidad del backend | `feature/api/auth-jwt` |
| `feature` | `api` | Nuevo endpoint | `feature/api/users-crud` |
| `fix` | `api` | Corrección de errores del backend | `fix/api/pagination` |
| `fix` | `ui` | Corrección de errores del frontend | `fix/ui/navbar` |
| `refactor` | `api` | Mejora del código sin cambiar funcionalidad | `refactor/api/database` |
| `refactor` | `ui` | Reorganización de componentes | `refactor/ui/sidebar` |
| `docs` | `api` | Documentación del backend | `docs/api/swagger` |
| `test` | `ui` | Pruebas del frontend | `test/ui/login` |
| `hotfix` | `api` | Corrección urgente en producción | `hotfix/api/login-error` |


### Reglas
1. Protección de ramas principales
- **Nunca hacer push directo a `main`.** Todos los cambios a `main` deben venir de un pull request.
- **Nunca hacer push directo a `dev`.** Todos los cambios a `dev` deben venir de un pull request.
- Cualquier commit pusheado directamente a `main` será eliminado.
  
2. Rama de destino según el tipo de PR
- feature/*, fix/*, refactor/* → el PR debe apuntar a develop. Nunca a main.
- develop → main solo se hace en releases/versiones estables, mediante un PR dedicado.
- No se permite abrir un PR desde una rama feature/* o fix/* directamente hacia main.


## Conventional Commits

Cada mensaje de commit debe seguir la especificación **Conventional Commits**.

### Formato

```
<tipo>(<alcance>): <descripción>
```

### Tipos

| Tipo | Cuándo usarlo |
|------|---------------|
| `feat` | Una nueva funcionalidad |
| `fix` | Corrección de un error |
| `refactor` | Cambio que no corrige error ni agrega funcionalidad |
| `style` | Formato, punto y coma faltante, etc. (sin cambio en código de producción) |
| `docs` | Solo cambios en documentación |
| `chore` | Proceso de build, dependencias o herramientas |
| `test` | Agregar o modificar tests |
| `perf` | Mejora de rendimiento |

### Alcance (Scope)

El alcance indica **qué área** afecta el cambio.
	
	Alcances frontend: `router`, `store`, `pages`, `components`, `services`, `styles`, `utils`, `layout`
	Alcances backend: `routes`, `models`, `services`, `schemas`, `middleware`, `mongo`, `config`
	Transversales: `deps`, `config`, `ci`, `docs`

### Ejemplos

```
feat(reports): add community voting on reports
feat(router): implement route guards for authenticated pages
fix(services): handle 401 response and redirect to login
refactor(store): replace manual event emit with Proxy-based reactivity
chore(deps): upgrade tailwindcss to v4
docs(api): document report status transition endpoints
style(components): format Button.js with consistent spacing
test(models): add unit tests for Report status transitions
```

### Reglas

- **La descripción debe estar en inglés.**
- **La descripción debe ser imperativa, en presente:** "add" no "added" ni "adds".
- **La descripción debe ser concisa** — menos de 72 caracteres si es posible.
- **No capitalizar la primera letra** de la descripción.
- **Sin punto al final.**

> Cualquier commit que no siga esta convención será **eliminado**.
> Usa `git rebase` para corregir mensajes antes de pushear.

---

Flujo de Pull Request


1. Crea una rama feature/fix/refactor desde develop:

		bash   
		git checkout develop
   		git pull
   		git checkout -b feature/api-auth


2. Haz commits siguiendo el formato Conventional Commits.
3. Pushea y abre un PR apuntando a develop (nunca a main).
4. Asegúrate de que la descripción del PR explique qué y por qué.
5. Después de revisión y aprobación, la rama se fusiona en develop.
6. Periódicamente, cuando develop esté estable, se abre un PR de develop a main para release.

## Tamaño de los Commits

### Pautas

- **Un commit por cambio lógico.** Si corriges dos errores no relacionados, haz dos commits.
- **Un archivo por commit** es aceptable cuando los archivos no están relacionados.
- **Agrupa archivos relacionados** en un solo commit solo cuando los cambios compartan el mismo propósito y no puedan funcionar independientemente.
- **Commits grandes están fuertemente desaconsejados.** Si cambiaste 20+ archivos, reconsidera si se pueden dividir.

### Ejemplos correctos

```
feat(auth): add login form component
    - src/components/domain/LoginForm.js (nuevo)

feat(auth): wire login form to auth service
    - src/pages/auth/login.js (modificado)
    - src/services/auth.service.js (modificado)
    - src/store/auth.store.js (modificado)
```

Son dos commits separados porque el componente puede existir independientemente de la conexión con el servicio.

### Ejemplos incorrectos

```
feat: add lots of stuff
    - 35 archivos cambiados, 1200 adiciones

fix(styles): fix style
    - Todos los archivos CSS del proyecto modificados "porque lo necesitaban"
