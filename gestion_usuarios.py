"""
Sistema de gestión de usuarios
Proyecto Unidad 4 - Manejo de archivos, validación de datos y captura de errores

Formato de cada línea en usuarios.txt:
    nombre,edad,fecha_hora
    Ejemplo: Carlos,25,2025-06-12 14:30:05

La lectura también tolera el formato antiguo de 2 campos (nombre,edad).
"""

from datetime import datetime

ARCHIVO = "usuarios.txt"


# ---------------------------------------------------------------------------
# Funciones de validación
# ---------------------------------------------------------------------------

def validar_nombre(nombre):
    """Valida que el nombre no esté vacío.
    Devuelve (True, None) si es válido o (False, motivo) si no lo es."""
    if nombre.strip() == "":
        return False, "nombre vacío"
    return True, None


def validar_edad(edad_texto):
    """Valida que la edad sea numérica y no negativa.
    Devuelve (True, edad_int, None) o (False, None, motivo)."""
    try:
        edad = int(edad_texto)
    except ValueError:
        return False, None, "edad no numérica"
    if edad < 0:
        return False, None, "edad negativa"
    return True, edad, None


def parsear_linea(linea):
    """Analiza una línea del archivo y valida su formato (Reto 3).
    Devuelve (True, (nombre, edad, fecha), None) si es válida
    o (False, None, motivo) si está mal formada."""
    linea = linea.strip()
    if linea == "":
        return False, None, "línea vacía"

    partes = linea.split(",")
    # Aceptamos 2 campos (formato antiguo) o 3 campos (con fecha y hora).
    if len(partes) < 2 or len(partes) > 3:
        return False, None, "número de campos incorrecto"

    nombre = partes[0].strip()
    edad_texto = partes[1].strip()
    fecha = partes[2].strip() if len(partes) == 3 else ""

    ok_nombre, motivo = validar_nombre(nombre)
    if not ok_nombre:
        return False, None, motivo

    ok_edad, edad, motivo = validar_edad(edad_texto)
    if not ok_edad:
        return False, None, motivo

    return True, (nombre, edad, fecha), None


# ---------------------------------------------------------------------------
# Lectura del archivo
# ---------------------------------------------------------------------------

def leer_usuarios(mostrar_errores=True):
    """Lee el archivo y devuelve una lista de usuarios válidos: (nombre, edad, fecha).
    Si una línea está mal formada la informa pero NO detiene el programa."""
    usuarios = []
    try:
        with open(ARCHIVO, "r", encoding="utf-8") as archivo:
            for numero, linea in enumerate(archivo, start=1):
                if linea.strip() == "":
                    continue
                valido, datos, motivo = parsear_linea(linea)
                if valido:
                    usuarios.append(datos)
                elif mostrar_errores:
                    print(f"  ⚠ Línea {numero} ignorada ({motivo}): {linea.strip()}")
    except FileNotFoundError:
        # El archivo todavía no existe: no es un error grave.
        pass
    except PermissionError:
        print("No se tienen permisos para leer el archivo.")
    except Exception as error:
        print(f"Ocurrió un error inesperado al leer: {error}")
    return usuarios


def usuario_existe(nombre):
    """Indica si ya existe un usuario con ese nombre (ignorando mayúsculas)."""
    usuarios = leer_usuarios(mostrar_errores=False)
    return any(u[0].lower() == nombre.strip().lower() for u in usuarios)


# ---------------------------------------------------------------------------
# Opciones del menú
# ---------------------------------------------------------------------------

def registrar_usuario():
    """Registra un usuario con validaciones, control de duplicados (Reto 2)
    y fecha/hora de creación (Reto 5)."""
    try:
        nombre = input("Ingrese el nombre del usuario: ").strip()
        ok_nombre, _ = validar_nombre(nombre)
        if not ok_nombre:
            print("El nombre no puede estar vacío.")
            return

        # Reto 2: evitar duplicados.
        if usuario_existe(nombre):
            print(f"El usuario '{nombre}' ya está registrado. No se guardó de nuevo.")
            return

        edad_texto = input("Ingrese la edad del usuario: ")
        ok_edad, edad, motivo = validar_edad(edad_texto)
        if not ok_edad:
            if motivo == "edad negativa":
                print("La edad no puede ser negativa.")
            else:
                print("La edad debe ser numérica.")
            return

        # Reto 5: fecha y hora de creación.
        fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(ARCHIVO, "a", encoding="utf-8") as archivo:
            archivo.write(f"{nombre},{edad},{fecha_hora}\n")
        print("Usuario registrado exitosamente.")

    except PermissionError:
        print("No se tienen permisos para escribir en el archivo.")
    except Exception as error:
        print(f"Ocurrió un error inesperado: {error}")


def mostrar_usuarios():
    """Muestra todos los usuarios; informa de líneas mal formadas (Reto 3)."""
    try:
        with open(ARCHIVO, "r", encoding="utf-8") as archivo:
            lineas = archivo.readlines()
    except FileNotFoundError:
        print("No se encontró el archivo de usuarios.")
        return
    except PermissionError:
        print("No se tienen permisos para leer el archivo.")
        return
    except Exception as error:
        print(f"Ocurrió un error inesperado: {error}")
        return

    if not any(l.strip() for l in lineas):
        print("No hay usuarios registrados.")
        return

    print("\nUsuarios registrados:")
    hay_validos = False
    for numero, linea in enumerate(lineas, start=1):
        if linea.strip() == "":
            continue
        valido, datos, motivo = parsear_linea(linea)
        if valido:
            nombre, edad, fecha = datos
            if fecha:
                print(f"  Nombre: {nombre}, Edad: {edad}, Creado: {fecha}")
            else:
                print(f"  Nombre: {nombre}, Edad: {edad}")
            hay_validos = True
        else:
            print(f"  ⚠ Línea {numero} mal formada ({motivo}): {linea.strip()}")

    if not hay_validos:
        print("  (No se encontraron registros válidos.)")


def buscar_usuario():
    """Busca un usuario por nombre y muestra sus datos (Reto 1)."""
    nombre_buscado = input("Ingrese el nombre a buscar: ").strip()
    if nombre_buscado == "":
        print("Debe ingresar un nombre para buscar.")
        return

    usuarios = leer_usuarios(mostrar_errores=False)
    encontrados = [u for u in usuarios if u[0].lower() == nombre_buscado.lower()]

    if not encontrados:
        print(f"No se encontró ningún usuario con el nombre '{nombre_buscado}'.")
        return

    print("\nResultado de la búsqueda:")
    for nombre, edad, fecha in encontrados:
        if fecha:
            print(f"  Nombre: {nombre}, Edad: {edad}, Creado: {fecha}")
        else:
            print(f"  Nombre: {nombre}, Edad: {edad}")


def separar_registros():
    """Lee un archivo con errores y separa registros buenos y malos (Reto 4).
    Genera usuarios_validos.txt y errores.txt."""
    archivo_entrada = input("Nombre del archivo a procesar (ej: entrada.txt): ").strip()
    if archivo_entrada == "":
        print("Debe indicar el nombre del archivo de entrada.")
        return

    validos = []
    invalidos = []

    try:
        with open(archivo_entrada, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                if linea.strip() == "":
                    continue
                valido, _, motivo = parsear_linea(linea)
                if valido:
                    validos.append(linea.strip())
                else:
                    # Guardamos también el motivo del error para revisarlo fácil.
                    invalidos.append(f"{linea.strip()}  ({motivo})")
    except FileNotFoundError:
        print(f"No se encontró el archivo '{archivo_entrada}'.")
        return
    except PermissionError:
        print("No se tienen permisos para leer el archivo de entrada.")
        return
    except Exception as error:
        print(f"Ocurrió un error inesperado al leer: {error}")
        return

    try:
        with open("usuarios_validos.txt", "w", encoding="utf-8") as f_validos:
            for registro in validos:
                f_validos.write(registro + "\n")

        with open("errores.txt", "w", encoding="utf-8") as f_errores:
            for registro in invalidos:
                f_errores.write(registro + "\n")
    except PermissionError:
        print("No se tienen permisos para escribir los archivos de salida.")
        return
    except Exception as error:
        print(f"Ocurrió un error inesperado al escribir: {error}")
        return

    print("\nProceso terminado:")
    print(f"  {len(validos)} registro(s) válido(s)   -> usuarios_validos.txt")
    print(f"  {len(invalidos)} registro(s) con error  -> errores.txt")


# ---------------------------------------------------------------------------
# Opciones extra (puntos adicionales)
# ---------------------------------------------------------------------------

def contar_usuarios():
    """Cuenta cuántos usuarios válidos hay registrados."""
    usuarios = leer_usuarios(mostrar_errores=False)
    print(f"Hay {len(usuarios)} usuario(s) registrado(s).")


def eliminar_usuario():
    """Elimina un usuario por nombre reescribiendo el archivo."""
    nombre_objetivo = input("Ingrese el nombre del usuario a eliminar: ").strip()
    if nombre_objetivo == "":
        print("Debe ingresar un nombre.")
        return

    usuarios = leer_usuarios(mostrar_errores=False)
    quedan = [u for u in usuarios if u[0].lower() != nombre_objetivo.lower()]

    if len(quedan) == len(usuarios):
        print(f"No se encontró el usuario '{nombre_objetivo}'.")
        return

    try:
        with open(ARCHIVO, "w", encoding="utf-8") as archivo:
            for nombre, edad, fecha in quedan:
                if fecha:
                    archivo.write(f"{nombre},{edad},{fecha}\n")
                else:
                    archivo.write(f"{nombre},{edad}\n")
        print(f"Usuario '{nombre_objetivo}' eliminado correctamente.")
    except PermissionError:
        print("No se tienen permisos para escribir en el archivo.")
    except Exception as error:
        print(f"Ocurrió un error inesperado: {error}")


def edad_promedio():
    """Calcula la edad promedio de los usuarios."""
    usuarios = leer_usuarios(mostrar_errores=False)
    if not usuarios:
        print("No hay usuarios registrados.")
        return
    suma = sum(u[1] for u in usuarios)
    promedio = suma / len(usuarios)
    print(f"La edad promedio es {promedio:.1f} años.")


def ordenar_usuarios():
    """Muestra los usuarios ordenados por nombre o por edad."""
    usuarios = leer_usuarios(mostrar_errores=False)
    if not usuarios:
        print("No hay usuarios registrados.")
        return

    criterio = input("Ordenar por (1) nombre o (2) edad: ").strip()
    if criterio == "1":
        usuarios.sort(key=lambda u: u[0].lower())
    elif criterio == "2":
        usuarios.sort(key=lambda u: u[1])
    else:
        print("Opción no válida.")
        return

    print("\nUsuarios ordenados:")
    for nombre, edad, _ in usuarios:
        print(f"  Nombre: {nombre}, Edad: {edad}")


# ---------------------------------------------------------------------------
# Menú principal
# ---------------------------------------------------------------------------

def menu():
    opcion = ""
    while opcion != "0":
        print("\n========= USUARIOS =========")
        print("1. Registrar usuario")
        print("2. Mostrar usuarios")
        print("3. Buscar usuario")
        print("4. Separar registros buenos/malos de un archivo")
        print("--- Opciones extra ---")
        print("5. Contar usuarios")
        print("6. Eliminar usuario")
        print("7. Edad promedio")
        print("8. Ordenar usuarios")
        print("0. Salir")
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            registrar_usuario()
        elif opcion == "2":
            mostrar_usuarios()
        elif opcion == "3":
            buscar_usuario()
        elif opcion == "4":
            separar_registros()
        elif opcion == "5":
            contar_usuarios()
        elif opcion == "6":
            eliminar_usuario()
        elif opcion == "7":
            edad_promedio()
        elif opcion == "8":
            ordenar_usuarios()
        elif opcion == "0":
            print("Programa finalizado.")
        else:
            print("Opción no válida. Intente nuevamente.")


if __name__ == "__main__":
    menu()
