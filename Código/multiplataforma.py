import os
import subprocess

def detectar_so():
    sistema = os.name #Detectamos que sistema operativo se utiliza.

    if sistema == "nt":
        return "Windows"
    else:
        return "Linux/Unix"

def realizar_ping(servidor, parametro_ping):
    #Realizamos el comando "ping"
    comando = ["ping", parametro_ping, "1", servidor]
    try:
        #Ejecutamos los comandos.
        resultado = subprocess.run(
            comando,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=3 #Evia que el programa se quede congelado si el sistema tarda demasiado.
            )
        return resultado.returncode == 0
    except subprocess.TimeoutExpired:
        #Si el programa tarda mas de 3 segundos, lo corta de forma segura.
        return False
    except Exception as e:
        #Esto captura cualquier otro error raro que pueda aparecer.
        return False

def optener_ip_router(sistema):
    try:
        if sistema == "Windows":
            resultado = subprocess.run(["ipconfig"], capture_output=True, text=True, check=True)

            #Buscamos la linea de la puerta de enlace. (Recorremos linea por linea con un for)
            for linea in resultado.stdout.split("\n"):
                if "Puerta de enlace predeterminada" in linea or "Default Gateway" in linea:
                    ip = linea.split(":")
                    if len(ip) > 1 and ip[1].strip():
                        return ip[1].strip() #Devuelve la IP limpia.
                    
        else:
            resultado = subprocess.run(["ip", "route"], capture_output=True, text=True, check=True)
            #El comando ip route imprime algo asi: "default via 192.168.1.1 dev wlan0..."
            ip = resultado.stdout.split("\n")[0] #Extraemos la primera linea.
            if "default via" in ip:
                return ip.split()[2] #La tercera palabra es la ip del router.

    #Si sucede un error al ejecutar el comando, devolvemos la IP por defecto.
    except subprocess.CalledProcessError as e:
        print(f"\033[1;31mError al ejecutar el comando: {e}\033[0m")
        return "192.168.1.1"
    except Exception as e:
        print(f"\033[1;31mError: {e}\033[0m")
        return "192.168.1.1"

            

def diagnostico_red(sistema):
    print("\n--- INICIANDO DIAGNÓSTICO DE RED ---")

    if sistema == "Windows":
        parametro = "-n"
    else:
        parametro = "-c"
    
    ip_del_router = optener_ip_router(sistema)

    servidores = [
        ["Tu Router", ip_del_router],
        ["Servidor DNS de Google", "8.8.8.8"],
        ["Servidor de Cloudflare", "1.1.1.1"],
        ["Dominio Web (GitHub)", "github.com"],
    ]

    for nombre, ip in servidores:
        print(f"Comprobando {nombre} ({ip})...", end="", flush=True)
        if realizar_ping(ip, parametro):
            print(f"\033[1;32m[ OK ]\033[0m")
        else:
            print(f"\033[1;31m[ ERROR - SIN RESPUESTA ]\033[0m")

def sensor_recursos(sistema):
    print("\n--- INICIANDO SENSOR DE RECURSOS ---")
    
    try:
        if sistema == "Windows":
            cmd_cpu = ["wmic", "cpu", "get", "LoadPercentage"]
            cmd_ram = ["wmic", "OS", "get", "FreePhysicalMemory,TotalVisibleMemorySize"]

            res_cpu = subprocess.run(cmd_cpu, capture_output=True, text=True)
            res_ram = subprocess.run(cmd_ram, capture_output=True, text=True)

            print("-> Uso de CPU:")
            print(res_cpu.stdout.strip())
            print("\n-> Memoria RAM (en KB):")
            print(res_ram.stdout.strip())
        
        else:
            cmd_cpu = ["top", "-b", "-n", "1"]
            cmd_ram = ["free", "-m"]

            res_cpu = subprocess.run(cmd_cpu, capture_output=True, text=True)
            res_ram = subprocess.run(cmd_ram, capture_output=True, text=True)

            print("-> Estado general de CPU (Resumen):")
            lineas_cpu = res_cpu.stdout.split("\n")[:5]
            print("\n".join(lineas_cpu))
            print("\n-> Estado de la Memoria RAM (en MB):")
            print(res_ram.stdout.strip())

    except subprocess.CalledProcessError as e:
        print(f"\033[1;31mError al ejecutar el comando: {e}\033[0m") #Esto captura cualquier error que pueda aparecer al ejecutar los comandos.
    except Exception as e:
        print(f"\033[1;31mError: {e}\033[0m")

def menu():
    print("\n" + "=" * 41)
    print("    DIAGNÓSTICO DE RED MULTIPLATAFORMA")
    print("=" * 41)
    print("1. Ejecutar Diagnóstico de Red")
    print("2. Ver Estado de Recursos (CPU / RAM)")
    print("3. Ejecutar Ambos Diagnósticos")
    print("4. Salir")
    
    while True:
        try:
            entrada = input("\nSeleccione una opción (1-4): ")

            if not entrada:
                raise ValueError("No se ha introducido ninguna opción.")
            
            if entrada not in ["1", "2", "3", "4"]:
                raise ValueError("Entrada inválida. Seleccione una opció del 1 al 4.")

            entrada = int(entrada)
            return entrada

        except ValueError as e:
            print(f"\033[1;31m{e}\033[0m")
        except KeyboardInterrupt, EOFError:
            print("\n\nSaliendo de forma Segura...")
            return 4


def main():
    sistema_actual = detectar_so()
    print(f"\nSistema Operativo Detectado: {sistema_actual}")

    while True:
        opcion = menu()

        if opcion == 1:
            diagnostico_red(sistema_actual)
        elif opcion == 2:
            sensor_recursos(sistema_actual)
        elif opcion == 3:
            diagnostico_red(sistema_actual)
            sensor_recursos(sistema_actual)
        elif opcion == 4:
            print("\nSaliendo del Programa. ¡Hasta luego!\n")
            break

        try:
            input("\nPresiona Enter para continuar...")
        except KeyboardInterrupt, EOFError:
            print("\n\nSaliendo de forma Segura...")
            break

if __name__ == "__main__":
    main()