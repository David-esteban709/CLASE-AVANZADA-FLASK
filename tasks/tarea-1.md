# Tarea 1 - Levantar una aplicacion Flask desde cero

## Objetivo tecnico

Poner en marcha el proyecto en tu entorno local, entender para que sirve cada pieza minima del setup y verificar que la aplicacion responde en el navegador.

En esta primera clase no alcanza con "hacerlo andar". Tienes que empezar a distinguir que problema resuelve cada paso: aislamiento del entorno, instalacion de dependencias, arranque del servidor y renderizado de una plantilla HTML.

## Preparacion

Para instalar dependencias y ejecutar el proyecto, sigue el `README.md`.

## Consigna

1. Instala las dependencias y levanta la aplicacion siguiendo el `README.md`.

2. Abre la aplicacion en el navegador y comprueba que responde correctamente.

3. Modifica la vista base y verifica el cambio:

   Edita `templates/index.html`, cambia al menos el `<title>` y el `<h1>`, guarda y recarga la pagina.

   Este paso existe para que veas la relacion concreta entre archivo fuente, servidor y resultado en navegador. Codigo que no observas, no lo entendes.

## Preguntas de reflexion tecnica

1. Que problema concreto resuelve el entorno virtual en un proyecto Python?
Evita que se te arme un sancocho con las versiones. Te crea una carpeta separada para que lo que instales en esta tarea no te tire los proyectos viejos.

2. Que diferencia hay entre instalar `Flask` globalmente y hacerlo dentro de `.venv`?
Global es meterlo en el sistema de toda la compu del colegio (y despues se traba). Dentro de .venv es dejarlo guardadito solo en la carpeta de tu proyecto para que no estorbe.

3. Por que `requirements.txt` forma parte del proyecto y no de tu maquina personal?
Porque es la lista del mercado del codigo. Si subes la tarea a GitHub o me la pasas a mi por USB, yo necesito ver ese archivo para saber que instalar y que me corra igual que a ti.

4. Cuando ejecutas `python app.py`, que archivo actua como punto de entrada y por que?
El mismo app.py, porque es el archivo principal que tu estas llamando desde la terminal para que encienda el servidor de una.

5. Que relacion hay entre la ruta `/`, la funcion `inicio()` y el archivo `templates/index.html`?
Es el orden de llegada: tu entras al link principal (/), eso llama a la funcion inicio() en Python, y esa funcion te dispara en la pantalla el index.html.

6. Que evidencia te da la terminal de que el servidor arranco correctamente?
Que se queda quieta y te bota el link de siempre: el http://127.0.0.1:5000 para que entres a probar.

7. Si cambias el HTML y el navegador muestra otra cosa, que te demuestra eso sobre el flujo entre backend y frontend en este proyecto?
Que el frontend (la pagina) no se manda solo. Si el backend (Flask) no procesa y le manda el HTML actualizado cuando hundes F5, el navegador te va a seguir mostrando la version vieja.

## Entregable

La tarea se considera completa si puedes demostrar estas cuatro cosas:

1. El entorno virtual esta creado y activado.
2. Las dependencias se instalaron desde `requirements.txt`.
3. La aplicacion corre en tu maquina y responde en el navegador.
4. Modificaste `templates/index.html` y podes señalar exactamente donde se refleja ese cambio.

## Cierre

No estas aprendiendo a tipear comandos. Estas empezando a construir criterio tecnico. Si hoy entiendes que levanta el servidor, de donde salen las dependencias y por que Flask encuentra esa plantilla, entonces arrancaste bien. Simple no significa superficial.
