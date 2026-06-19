import pandas as pd

df_pacientes = pd.read_excel("data/BD_Consultorio_SanMartin.xlsx", sheet_name="Pacientes", dtype=str)
df_medicos   = pd.read_excel("data/BD_Consultorio_SanMartin.xlsx", sheet_name="Médicos",   dtype=str)
df_turnos    = pd.read_excel("data/BD_Consultorio_SanMartin.xlsx", sheet_name="Turnos",    dtype=str)
df_avisos    = pd.read_excel("data/BD_Consultorio_SanMartin.xlsx", sheet_name="Avisos_Disponibilidad", dtype=str)

# Limpiar espacios en todas las columnas de texto
df_pacientes = df_pacientes.apply(lambda col: col.str.strip())
df_medicos   = df_medicos.apply(lambda col: col.str.strip())
df_turnos    = df_turnos.apply(lambda col: col.str.strip())
df_avisos    = df_avisos.apply(lambda col: col.str.strip())