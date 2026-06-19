# 🏥 Consultorio San Martín — Bot de Gestión de Turnos

Trabajo Práctico Integrador — Organización Empresarial  
Tecnicatura Universitaria en Programación — UTN

## Descripción

Simulador de chatbot por consola que automatiza el proceso de solicitud de turnos médicos del Consultorio San Martín. El sistema permite reservar turnos, registrar pacientes nuevos y solicitar avisos de disponibilidad, interactuando mediante respuestas de texto simples.

## Estructura del proyecto

    consultorio_bot/
    ├── data/
    │   └── BD_Consultorio_SanMartin.xlsx
    ├── logic/
    │   ├── __init__.py
    │   └── consultas.py
    ├── db.py
    ├── main.py
    └── README.md

## Requisitos

- Python 3.8 o superior
- pandas
- openpyxl

## Instalación

```bash
pip install pandas openpyxl
```

## Ejecución

```bash
python main.py
```

> ⚠️ El archivo `BD_Consultorio_SanMartin.xlsx` debe estar cerrado antes de ejecutar el programa.

## Funcionalidades

- Reserva de turnos por especialidad médica
- Alta automática de pacientes nuevos
- Registro de avisos cuando no hay turnos disponibles
- Validación de entradas del usuario
- Persistencia de datos en archivo Excel

## Base de datos

El sistema utiliza una planilla Excel con 4 hojas normalizadas en 3FN:

| Hoja | Descripción |
|------|-------------|
| Pacientes | Datos personales y de contacto |
| Médicos | Especialidades y horarios |
| Turnos | Disponibilidad y reservas |
| Avisos_Disponibilidad | Lista de espera |

## Herramientas utilizadas

- **Python 3** — Lenguaje principal
- **pandas / openpyxl** — Manejo del Excel
- **FigJam** — Modelado BPMN 2.0
- **Claude (Anthropic)** — Asistente de IA para diseño y documentación
