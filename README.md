# SESHIA-
Aplicación web que integra el seguimiento del ciclo menstrual con la gestión y el análisis de finanzas personales.


GUIA DE PUSH Y PULL PARA GIT HUB

Desde el terminal van a hacer lo siguiente:

1. Crean una carpeta o eligen una carpeta donde quieran guardar lo que van a trabajar 
2. Le dan click derecho a la carpeta y abren el terminal 
3. Desde el terminal van a CLONAR el repositorio 

 	 	git clone https://github.com/YesRv/SHESIA-FINANCIAL-APP.git

4. Esto descarga el proyecto completo a tu computador y les creará una carpeta llamada 
	SHESIA FINANCIAL APP

5. Se van a ella via terminal con el comando:

   		cd SHESIA-FINANCIAL-APP


  Para crear una rama van a utilizar el siguiente comando, esto con el fin de revisar los push request, al final el SRCUM va a revisar cada commit que decidan       enviar y sera quien apruebe o niegue el push  

  # esto le dice a git, básicamente créame esta rama chamo y cambiate directamente a ella 
  git checkout -b feature/inicio 


  
Las ramas ya están creadas en el main voy a dejar la base, así que van a hacer el primer clone desde main, después en sus computadores 
van a ir trabajando lo que les corresponda, una vez que ya tengan un cambio realizado y funcional pueden hacer el push 

7. Antes de tocar cualquier archivo, el dev se mueve a developer y se asegura de tener la versión mas reciente del 
proyecto, simplemente usa el comando:

	# Te mueve a la rama developer. Es como cambiar de pestaña o cambiar de hoja
		git checkout dev

8. Lo siguiente es tener los cambios más recientes del proyecto, para eso, usamos SIEMPRE el comando:

	# descarga los cambios mas recientes que otros hayan subido, siempre háganlo antes de empezar a trabajar para no quedar desactualizados.

		git pull origin dev


9. Cada vez que avancen en algo, deben guardar su progreso, por el momento trabajaremos todos los avances en la rama secondary, para guardarlo, usan estos comandos:

 # Añadir los archivos, el comando de toda la vida
	git add .
	
Si lo hacen desde el vs code les pide un commit que es opcional (tengan mucho cuidado cuando hagan los push desde vs code porque se pueden guardar duplicados y eso es una demora para arreglarlo TTnTT)

# Básicamente le decimos a git, envíame los cambios desde mi pc hasta la rama X
	git push origin secondary

