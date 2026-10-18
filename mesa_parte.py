import csv
import os

ARCHIVO = "expedientes.csv"
CAMPOS = ["codigo", "dni", "nombre", "fecha", "asunto", "area"]


def cargar_expedientes():
    if not os.path.exists(ARCHIVO):
        return []

    with open(ARCHIVO, "r", newline="", encoding="utf-8") as archivo:
        return list(csv.DictReader(archivo))


def guardar_expedientes(expedientes):
    with open(ARCHIVO, "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=CAMPOS)
        escritor.writeheader()
        escritor.writerows(expedientes)


def registrar_expediente(expedientes):
    print("\n--- REGISTRO DE EXPEDIENTE ---")

    dni = input("DNI: ").strip()
    nombre = input("Nombre del ciudadano: ").strip()
    fecha = input("Fecha (DD/MM/AAAA): ").strip()
    asunto = input("Asunto: ").strip()
    area = input("Area de destino: ").strip()

    if not all([dni, nombre, fecha, asunto, area]):
        print("Error: todos los campos son obligatorios.")
        return

    if not dni.isdigit() or len(dni) != 8:
        print("Error: el DNI debe contener 8 digitos.")
        return

    numero = max(
        [int(e["codigo"].split("-")[1]) for e in expedientes],
        default=0
    ) + 1

    expediente = {
        "codigo": f"EXP-{numero:04d}",
        "dni": dni,
        "nombre": nombre,
        "fecha": fecha,
        "asunto": asunto,
        "area": area
    }

    expedientes.append(expediente)
    guardar_expedientes(expedientes)
    print("Expediente registrado:", expediente["codigo"])


def buscar_expediente(expedientes):
    codigo = input("Codigo del expediente: ").strip().upper()

    for expediente in expedientes:
        if expediente["codigo"] == codigo:
            print(expediente)
            return expediente

    print("No se encontro el expediente.")
    return None


def ordenar_expedientes(expedientes):
    expedientes.sort(key=lambda e: e["codigo"])
    guardar_expedientes(expedientes)
    print("Expedientes ordenados por codigo.")


def listar_expedientes(expedientes):
    if not expedientes:
        print("No hay expedientes registrados.")
        return

    for expediente in expedientes:
        print(expediente)


def generar_constancia(expedientes):
    expediente = buscar_expediente(expedientes)

    if expediente is None:
        return

    nombre_archivo = expediente["codigo"] + ".txt"

    with open(nombre_archivo, "w", encoding="utf-8") as archivo:
        archivo.write("CONSTANCIA DE RECEPCION\n")
        archivo.write("======================\n")
        for campo, valor in expediente.items():
            archivo.write(f"{campo.capitalize()}: {valor}\n")

    print("Constancia generada:", nombre_archivo)


def main():
    expedientes = cargar_expedientes()

    while True:
        print("\n=== MESA DE PARTES ===")
        print("1. Registrar expediente")
        print("2. Buscar expediente")
        print("3. Ordenar expedientes")
        print("4. Listar expedientes")
        print("5. Generar constancia")
        print("6. Salir")

        opcion = input("Seleccione una opcion: ").strip()

        if opcion == "1":
            registrar_expediente(expedientes)
        elif opcion == "2":
            buscar_expediente(expedientes)
        elif opcion == "3":
            ordenar_expedientes(expedientes)
        elif opcion == "4":
            listar_expedientes(expedientes)
        elif opcion == "5":
            generar_constancia(expedientes)
        elif opcion == "6":
            print("Sistema finalizado.")
            break
        else:
            print("Opcion no valida.")


if __name__ == "__main__":
    main()