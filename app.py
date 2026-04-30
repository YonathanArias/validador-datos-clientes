import streamlit as st
import random
import pandas as pd
from datetime import datetime

# ================= CONFIGURACIÓN =================

st.set_page_config(
    page_title="Validador de Clientes Niubiz",
    layout="centered"
)


col_logo, col_title = st.columns([1, 4])

with col_logo:
    st.image("niubiz_logo.png", width=120)

with col_title:
    st.markdown("## Validador de Clientes Niubiz")

st.divider()

# ================= DATA =================

CONTACT_REASONS = [
    "Consulta de transacciones y/o ventas realizadas y Abonos recibidos",
    "Tasas y/o comisiones, condiciones, DAE's y/o contratos",
    "Datos de RL, contacto, establecimiento y/o código de comercio registrados",
    "Datos de POS asignados, cantidad y series registradas"
]

QUESTIONS_DB = {
    "Consulta de transacciones y/o ventas realizadas y Abonos recibidos": [
        "¿Cuántos POS tienes activos actualmente con tu RUC?",
	"¿Qué modelo es tu POS? (Describe el producto)",
	"¿Tu número de RUC cuenta con más código de comercio?",
	"¿Tu código de comercio es permanente o temporal?",
	"¿Te encuentras registrado en NEL?",
	"¿Cuál es el giro de tu negocio? (MCC)",
	"Indícame tu dirección comercial",
	"Indícame tu dirección administrativa",
	"¿Cuál es tu razón social?",
	"¿Reportaste alguna avería en los últimos 2 meses?",
	"Indícame el banco donde se abona el dinero de tus ventas",
	"¿Cuántos terminales tienes en tu establecimiento?",
	"¿Cuál es el nombre de tu comercio registrado?",
	"¿Cuál es el nombre del representante legal?",
	"¿Cuál es el DNI del representante legal?",
	"¿Dime el tipo de tu cuenta bancaria registrada?",
	"¿En el último mes solicitaste contómetros?",
	"¿En el último mes realizaste alguna modificación de tus datos?",
	"¿Tu código de comercio se encuentra en soles o dolares?"
    ],
    "Tasas y/o comisiones, condiciones, DAE's y/o contratos": [
        "¿Cuántos POS tienes activos actualmente con tu RUC?",
	"¿Qué modelo es tu POS? (Describe el producto)",
	"¿Tu número de RUC cuenta con más código de comercio?",
	"¿Tu código de comercio es permanente o temporal?",
	"¿Te encuentras registrado en NEL?",
	"¿Cuál es el giro de tu negocio? (MCC)",
	"Indícame tu dirección comercial",
	"Indícame tu dirección administrativa",
	"¿Cuál es tu razón social?",
	"¿Reportaste alguna avería en los últimos 2 meses?",
	"Indícame el banco donde se abona el dinero de tus ventas",
	"¿Cuál fue el monto de tu último abono?",
	"¿Cuándo recibiste tu último abono?",
	"¿Cuántos terminales tienes en tu establecimiento?",
	"¿Cuál es el importe de tu última venta?",
	"¿Cuál es el nombre de tu comercio registrado?",
	"¿Cuál es el nombre del representante legal?",
	"¿Cuál es el DNI del representante legal?",
	"¿Dime el tipo de tu cuenta bancaria registrada?",
	"¿En el último mes solicitaste contómetros?",
	"¿En el último mes realizaste alguna modificación de tus datos?",
	"¿Tu código de comercio se encuentra en soles o dolares?"
    ],
    "Datos de RL, contacto, establecimiento y/o código de comercio registrados": [
        "¿Cuántos POS tienes activos actualmente con tu RUC?",
	"¿Qué modelo es tu POS? (Describe el producto)",
	"¿Tu número de RUC cuenta con más código de comercio?",
	"¿Te encuentras registrado en NEL?",
	"¿Cuál es el giro de tu negocio? (MCC)",
	"¿Reportaste alguna avería en los últimos 2 meses?",
	" Indícame el banco donde se abona el dinero de tus ventas",
	"¿Cuál fue el monto de tu último abono?",
	"¿Cuándo recibiste tu último abono?",
	"¿Cuántos terminales tienes en tu establecimiento?",
	"¿Cuál es el importe de tu última venta?",
	"¿Dime el tipo de tu cuenta bancaria registrada?",
	"¿En el último mes solicitaste contómetros?",
	"¿En el último mes realizaste alguna modificación de tus datos?",
	"¿Tu código de comercio se encuentra en soles o dolares?"

    ],
    "Datos de POS asignados, cantidad y series registradas": [
        "¿Tu número de RUC cuenta con más código de comercio?",
	"¿Tu código de comercio es permanente o temporal?",
	"¿Te encuentras registrado en NEL?",
	"¿Cuál es el giro de tu negocio? (MCC)",
	"Indícame tu dirección comercial",
	"Indícame tu dirección administrativa",
	"¿Cuál es tu razón social?",
	"¿Reportaste alguna avería en los últimos 2 meses?",
	" Indícame el banco donde se abona el dinero de tus ventas",
	"¿Cuál fue el monto de tu último abono?",
	"¿Cuándo recibiste tu último abono?",
	"¿Cuál es el importe de tu última venta?",
	"¿Cuál es el nombre de tu comercio registrado?",
	"¿Cuál es el nombre del representante legal?",
	"¿Cuál es el DNI del representante legal?",
	"¿Dime el tipo de tu cuenta bancaria registrada?",
	"¿En el último mes solicitaste contómetros?",
	"¿En el último mes realizaste alguna modificación de tus datos?",
	"¿Tu código de comercio se encuentra en soles o dolares?"
    ]
}

# ================= FUNCIONES =================

def export_history_to_csv():
    if not st.session_state.history:
        return None

    rows = []
    for h in st.session_state.history:
        rows.append({
            "Fecha": h["fecha"],
            "Hora": h["hora"],
            "Cliente": h["cliente"],
            "ID Cliente": h["id_cliente"],
            "Canal": h["canal"],
            "Motivo": h["motivo"],
            "Pregunta 1": h["preguntas"][0],
            "Resultado 1": h["respuestas"][0],
            "Pregunta 2": h["preguntas"][1],
            "Resultado 2": h["respuestas"][1],
            "Pregunta 3": h["preguntas"][2],
            "Resultado 3": h["respuestas"][2],
            "Estatus Final": h["resultado"]
        })

    return pd.DataFrame(rows)

# ================= SESSION STATE =================

if "step" not in st.session_state:
    st.session_state.step = "IDENTIFICATION"
    st.session_state.questions = []
    st.session_state.current_question = 0
    st.session_state.answers = []
    st.session_state.timestamp = None
    st.session_state.history = []

# ================= ETAPA 1: IDENTIFICACIÓN =================

if st.session_state.step == "IDENTIFICATION":

    st.subheader("Identificación del cliente")

    client_name = st.text_input("Cliente")
    client_id = st.text_input("Identificador (RUC / ID)")

    channel = st.radio(
        "Canal de contacto",
        ["phone", "whatsapp", "email"],
        horizontal=True
    )

    reason = st.radio(
        "Motivo de contacto",
        CONTACT_REASONS
    )

    # 👉 Exportación disponible EN CUALQUIER MOMENTO DE LA SESIÓN
    df_export = export_history_to_csv()
    if df_export is not None:
        st.download_button(
            label="📥 Exportar Reporte Maestro (CSV)",
            data=df_export.to_csv(index=False),
            file_name="reporte_validaciones_sesion.csv",
            mime="text/csv"
        )

    if st.button("Iniciar Validación"):
        if not client_name or not client_id:
            st.error("Debe completar los datos del cliente")
        else:
            st.session_state.client_name = client_name
            st.session_state.client_id = client_id
            st.session_state.channel = channel
            st.session_state.reason = reason

            st.session_state.questions = random.sample(
                QUESTIONS_DB.get(reason, []), 3
            )
            st.session_state.current_question = 0
            st.session_state.answers = []
            st.session_state.timestamp = datetime.now()
            st.session_state.step = "VALIDATION"
            st.rerun()

# ================= ETAPA 2: VALIDACIÓN =================

elif st.session_state.step == "VALIDATION":

    if st.session_state.current_question >= len(st.session_state.questions):
        st.session_state.step = "RESULT"
        st.rerun()

    q_index = st.session_state.current_question
    question = st.session_state.questions[q_index]

    st.subheader(f"Pregunta {q_index + 1} de 3")
    st.markdown(f"### {question}")

    col1, col2 = st.columns(2)

    if col1.button("❌ Incorrecto"):
        st.session_state.answers.append(False)
        st.session_state.current_question += 1
        st.rerun()

    if col2.button("✅ Correcto"):
        st.session_state.answers.append(True)
        st.session_state.current_question += 1
        st.rerun()

# ================= ETAPA 3: RESULTADO =================

elif st.session_state.step == "RESULT":

    failures = st.session_state.answers.count(False)
    successes = st.session_state.answers.count(True)

    resultado_final = "APROBADO" if failures <= 1 else "RECHAZADO"

    if resultado_final == "APROBADO":
        st.success("✅ VALIDACIÓN APROBADA")
    else:
        st.error("❌ NO PASÓ EL PROCESO DE VALIDACIÓN")

    st.write(f"**Aciertos:** {successes}")
    st.write(f"**Fallos:** {failures}")
    st.write(
        f"**Fecha y hora:** {st.session_state.timestamp.strftime('%d/%m/%Y %H:%M:%S')}"
    )

    # ✅ Guardar en historial de sesión
    record = {
        "fecha": st.session_state.timestamp.strftime("%d/%m/%Y"),
        "hora": st.session_state.timestamp.strftime("%H:%M:%S"),
        "cliente": st.session_state.client_name,
        "id_cliente": st.session_state.client_id,
        "canal": st.session_state.channel,
        "motivo": st.session_state.reason,
        "preguntas": st.session_state.questions,
        "respuestas": [
            "CORRECTO" if r else "INCORRECTO"
            for r in st.session_state.answers
        ],
        "resultado": resultado_final
    }

    if record not in st.session_state.history:
        st.session_state.history.append(record)

    df_export = export_history_to_csv()
    if df_export is not None:
        st.download_button(
            label="📥 Exportar Reporte Maestro (CSV)",
            data=df_export.to_csv(index=False),
            file_name="reporte_validaciones_sesion.csv",
            mime="text/csv"
        )

    if st.button("Nueva Gestión"):
        st.session_state.step = "IDENTIFICATION"
        st.rerun()