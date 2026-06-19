import pandas as pd
from datetime import date
import db

def obtener_especialidades():
    especialidades = db.df_medicos["especialidad"].unique()
    return list(especialidades)

def obtener_turnos_disponibles(especialidad):
    medicos_especialidad = db.df_medicos[db.df_medicos["especialidad"] == especialidad]
    ids_medicos = medicos_especialidad["id_medico"].tolist()

    turnos = db.df_turnos[
        (db.df_turnos["id_medico"].isin(ids_medicos)) &
        (db.df_turnos["estado"] == "disponible")
    ]
    return turnos

def buscar_paciente_por_dni(dni):
    resultado = db.df_pacientes[db.df_pacientes["dni"] == dni]
    if resultado.empty:
        return None
    return resultado.iloc[0]

def reservar_turno(id_turno, id_paciente):
    indice = db.df_turnos[db.df_turnos["id_turno"] == id_turno].index[0]
    db.df_turnos.at[indice, "id_paciente"] = id_paciente
    db.df_turnos.at[indice, "estado"] = "ocupado"

def registrar_paciente(nombre, apellido, dni, obra_social, nro_socio, telefono, email):
    nuevo_id = f"P{len(db.df_pacientes) + 1:03d}"
    nueva_fila = pd.DataFrame([{
        "id_paciente": nuevo_id,
        "nombre":      nombre,
        "apellido":    apellido,
        "dni":         dni,
        "obra_social": obra_social,
        "nro_socio":   nro_socio,
        "telefono":    telefono,
        "email":       email
    }])
    db.df_pacientes = pd.concat([db.df_pacientes, nueva_fila], ignore_index=True)
    return nuevo_id

def registrar_aviso(id_paciente, especialidad):
    nuevo_id = f"AV{len(db.df_avisos) + 1:03d}"
    nueva_fila = pd.DataFrame([{
        "id_aviso":        nuevo_id,
        "id_paciente":     id_paciente,
        "especialidad":    especialidad,
        "fecha_solicitud": date.today().strftime("%d/%m/%Y"),
        "estado_aviso":    "pendiente"
    }])
    db.df_avisos = pd.concat([db.df_avisos, nueva_fila], ignore_index=True)
    return nuevo_id

def guardar_cambios():
    with pd.ExcelWriter("data/BD_Consultorio_SanMartin.xlsx", engine="openpyxl") as writer:
        db.df_pacientes.to_excel(writer, sheet_name="Pacientes",              index=False)
        db.df_medicos.to_excel(writer,   sheet_name="Médicos",                index=False)
        db.df_turnos.to_excel(writer,    sheet_name="Turnos",                 index=False)
        db.df_avisos.to_excel(writer,    sheet_name="Avisos_Disponibilidad",  index=False)