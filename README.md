# DockGuardian -  Monitor de Contenedores Docker - Backend + UI

Este proyecto tiene como objetivo monitorear contenedores Docker de forma automática. 
Detecta cuando un contenedor cambia a un estado crítico (como exited, paused, o dead) 
y notifica al administrador a través de una interfaz web amigable. 
Además, permite consultar el estado actual de los contenedores y visualizar sus logs.


#  Desarrollado por 

    Proyecto desarrollado de forma individual


## Tecnologías usadas

- **Backend:** FastAPI + Docker SDK para Python  
- **UI:** Streamlit  
- **Contenedores:** Docker + Docker Compose  


## Funcionalidades

- Visualización del estado de los contenedores activos e inactivos.
- Alertas automáticas cuando un contenedor se detiene. 
- Refresco automático de estado (cada 10 segundos). 
- Notificación sonora (en UI) cuando se detectan fallos.


