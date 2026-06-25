# Trabajo Practico Integrador - Diagnostico y Monitoreo Multiplataforma
Repositorio Oficial del TPI de la Materia Arquitectura y Sistemas Operativos.

# Metodología Utilizada  
El proceso de desarrollo, despliegue y testeo del software se dividió en las siguientes fases 
metodológicas:  
● Fase 1: Codificación e Inyección de Robustez: Escritura del código en un entorno de 
desarrollo integrado, implementando el manejo explícito de excepciones (ValueError, 
CalledProcessError) para blindar el menú interactivo contra entradas nulas o caracteres 
inválidos.  
● Fase 2: Despliegue en Entorno Anfitrión (Windows): Validación de la captura de datos 
a través de la herramienta instrumental de administración de Windows (WMIC) y testeo 
de la interfaz cromática mediante códigos de escape ANSI en la consola.  
● Fase 3: Configuración del Entorno Virtual (Linux): Despliegue de una máquina virtual 
en Oracle VirtualBox configurada con Ubuntu Server. Para asegurar que el módulo de 
diagnóstico de red pudiese validar el entorno real, se configuró la interfaz de red de la 
máquina virtual en Modo Bridge (Adaptador Puente). Esto otorgó al sistema operativo 
invitado una dirección IP propia dentro del mismo rango del router físico.  
● Fase 4: Ejecución e Interoperabilidad: Transferencia del script a la máquina virtual 
mediante SSH/SCP y ejecución del programa en la terminal Linux para comprobar la 
correcta bifurcación lógica orientada a comandos como ip route y free -m.  
