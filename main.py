import db
from logic.consultas import (
    obtener_especialidades,
    obtener_turnos_disponibles,
    buscar_paciente_por_dni,
    reservar_turno,
    registrar_paciente,
    registrar_aviso,
    guardar_cambios
)

sesion = {
    "estado": "inicio",
    "especialidad_elegida": None,
    "turno_elegido": None,
    "paciente": None
}

print("Bienvenido al sistema de turnos del Consultorio San Martín.")

while True:

    if sesion["estado"] == "inicio":
        especialidades = obtener_especialidades()
        print("\n¿Qué especialidad necesita?")
        for i, esp in enumerate(especialidades, 1):
            print(f"  {i}. {esp}")
        sesion["estado"] = "esperando_especialidad"

    elif sesion["estado"] == "esperando_especialidad":
        entrada = input("\nIngrese el número de especialidad: ")
        especialidades = obtener_especialidades()
        if entrada.isdigit() and 1 <= int(entrada) <= len(especialidades):
            sesion["especialidad_elegida"] = especialidades[int(entrada) - 1]
            sesion["estado"] = "esperando_dni"
        else:
            print("Opción inválida, intente de nuevo.")

    elif sesion["estado"] == "esperando_dni":
        dni = input("\nIngrese su DNI (solo números, sin puntos): ").strip()
        if not dni.isdigit():
            print("El DNI debe contener solo números. Intente de nuevo.")
        elif len(dni) < 7 or len(dni) > 8:
            print("El DNI debe tener entre 7 y 8 dígitos. Intente de nuevo.")
        else:
            paciente = buscar_paciente_por_dni(dni)
            if paciente is not None:
                sesion["paciente"] = paciente
                sesion["estado"] = "esperando_turno"
            else:
                print("Su DNI no está registrado en el sistema.")
                respuesta = input("¿Desea registrarse como paciente nuevo? (s/n): ")
                if respuesta.lower() == "s":
                    sesion["estado"] = "registro_paciente"
                elif respuesta.lower() == "n":
                    print("De acuerdo. Puede acercarse al consultorio para registrarse.")
                    sesion["estado"] = "fin"
                else:
                    print("Respuesta inválida. Ingrese s o n.")

    elif sesion["estado"] == "registro_paciente":
        print("\nComplete sus datos para registrarse:")
        nombre      = input("  Nombre: ")
        apellido    = input("  Apellido: ")
        dni         = input("  DNI: ")
        obra_social = input("  Obra social (o 'Particular'): ")
        nro_socio   = input("  Número de socio (o '-' si no tiene): ")
        while True:
            telefono = input("  Teléfono (ej: 11-4523-1234): ").strip()
            if all(c.isdigit() or c == "-" for c in telefono):
                break
            print("  Teléfono inválido. Use solo números y guiones.")
        while True:
            email = input("  Email: ").strip()
            if "@" in email and "." in email:
                break
            print("  Email inválido. Debe contener '@' y '.'")
        nuevo_id = registrar_paciente(nombre, apellido, dni, obra_social, nro_socio, telefono, email)
        sesion["paciente"] = buscar_paciente_por_dni(dni)
        guardar_cambios()
        print(f"\nRegistro exitoso. Su ID de paciente es: {nuevo_id}")
        sesion["estado"] = "esperando_turno"

    elif sesion["estado"] == "esperando_turno":
        turnos = obtener_turnos_disponibles(sesion["especialidad_elegida"])
        if turnos.empty:
            print(f"\nNo hay turnos disponibles para {sesion['especialidad_elegida']}.")
            respuesta = input("¿Desea que le avisemos cuando haya un turno disponible? (s/n): ")
            if respuesta.lower() == "s":
                sesion["estado"] = "registro_aviso"
            elif respuesta.lower() == "n":
                sesion["estado"] = "fin"
            else:
                print("Respuesta inválida. Ingrese s o n.")
        else:
            print(f"\nTurnos disponibles para {sesion['especialidad_elegida']}:")
            turnos_lista = turnos.reset_index(drop=True)
            for i, row in turnos_lista.iterrows():
                print(f"  {i+1}. Fecha: {row['fecha']}  Hora: {row['hora']}")
            entrada = input("\nIngrese el número de turno: ")
            if entrada.isdigit() and 1 <= int(entrada) <= len(turnos_lista):
                sesion["turno_elegido"] = turnos_lista.iloc[int(entrada) - 1]
                sesion["estado"] = "confirmacion"
            else:
                print("Opción inválida, intente de nuevo.")

    elif sesion["estado"] == "registro_aviso":
        id_aviso = registrar_aviso(
            sesion["paciente"]["id_paciente"],
            sesion["especialidad_elegida"]
        )
        guardar_cambios()
        print(f"\nListo. Le avisaremos a {sesion['paciente']['email']} cuando haya un turno disponible.")
        print(f"Número de aviso: {id_aviso}")
        sesion["estado"] = "fin"

    elif sesion["estado"] == "confirmacion":
        turno    = sesion["turno_elegido"]
        paciente = sesion["paciente"]
        print(f"\nResumen de su turno:")
        print(f"  Paciente:     {paciente['nombre']} {paciente['apellido']}")
        print(f"  Especialidad: {sesion['especialidad_elegida']}")
        print(f"  Fecha:        {turno['fecha']}")
        print(f"  Hora:         {turno['hora']}")
        confirmacion = input("\n¿Confirma la reserva? (s/n): ")
        if confirmacion.lower() == "s":
            reservar_turno(turno["id_turno"], paciente["id_paciente"])
            guardar_cambios()
            print("Turno reservado con éxito.")
            sesion["estado"] = "fin"
        elif confirmacion.lower() == "n":
            print("Reserva cancelada.")
            sesion["estado"] = "fin"
        else:
            print("Respuesta inválida. Ingrese s o n.")

    elif sesion["estado"] == "fin":
        print("\nGracias por usar el sistema. ¡Hasta pronto!")
        break