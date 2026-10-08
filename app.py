import streamlit as st
import pandas as pd
import os

# 1. Configuración de la Base de Datos Local
DATA_FILE = 'horarios_avante.csv'

if not os.path.exists(DATA_FILE):
    df_init = pd.DataFrame(columns=["Hora", "Paciente", "Terapeuta", "Piso_Sala", "Estado"])
    df_init.to_csv(DATA_FILE, index=False)

def load_data():
    return pd.read_csv(DATA_FILE)

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

# 2. Configuración de la Aplicación
st.set_page_config(page_title="Terapias Avante", layout="wide")
st.title("Centro de Terapias - Instituto Avante")

# Menú de navegación
menu = st.sidebar.radio(
    "Selecciona la vista:", 
    ["📱 Vista Padres (Buscar Hijo)", "📺 Vista TV (1er Piso)", "⚙️ Administración (Recepción)"]
)

# 3. Pantalla para los Padres
if menu == "📱 Vista Padres (Buscar Hijo)":
    st.subheader("Encuentra la terapia de tu hijo/a")
    df = load_data()
    
    search = st.text_input("Escribe el primer nombre de tu hijo/a:", placeholder="Ejemplo: Sebastian")
    
    if search:
        # Filtra la base de datos por el nombre ingresado
        resultados = df[df["Paciente"].str.contains(search, case=False, na=False)]
        
        if not resultados.empty:
            st.success("Terapia encontrada:")
            st.table(resultados)
        else:
            st.warning("No se encontraron terapias asignadas para este nombre el día de hoy.")

# 4. Pantalla para el Televisor del Primer Piso
elif menu == "📺 Vista TV (1er Piso)":
    st.subheader("Horarios Generales de Terapias")
    
    # Código oculto para que la pantalla del TV se actualice sola cada 60 segundos
    st.components.v1.html("<meta http-equiv='refresh' content='60'>", height=0)
    
    df = load_data()
    # Muestra la tabla en tamaño grande para el TV
    st.dataframe(df, use_container_width=True, hide_index=True)

# 5. Pantalla para la Recepción / Coordinación
elif menu == "⚙️ Administración (Recepción)":
    st.subheader("Asignar o Reubicar Terapias")
    df = load_data()

    # Formulario de ingreso de datos
    with st.form("nuevo_horario"):
        col1, col2 = st.columns(2)
        hora = col1.time_input("Hora de la terapia")
        paciente = col2.text_input("Nombre del Paciente")
        terapeuta = col1.text_input("Terapeuta Asignado")
        sala = col2.selectbox("Piso y Sala", ["Piso 1 - Sala A", "Piso 2 - Sala B", "Piso 2 - Sala C", "Piso 3 - Sala D"])
        estado = st.selectbox("Estado", ["Confirmado", "Reubicado (Cambio de Sala/Terapeuta)", "Cancelado"])
        
        submit = st.form_submit_button("Guardar en el sistema")

        if submit and paciente:
            nueva_fila = pd.DataFrame({
                "Hora": [hora.strftime("%H:%M")], 
                "Paciente": [paciente], 
                "Terapeuta": [terapeuta], 
                "Piso_Sala": [sala], 
                "Estado": [estado]
            })
            df = pd.concat([df, nueva_fila], ignore_index=True)
            save_data(df)
            st.success("Horario guardado y proyectado en el TV correctamente.")
            st.rerun()

    st.divider()
    st.write("📋 **Terapias registradas hoy:**")
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Botón para limpiar al final del día
    if st.button("Borrar todos los registros (Cerrar el día)"):
        df_clean = pd.DataFrame(columns=df.columns)
        save_data(df_clean)
        st.success("Sistema limpio para el día de mañana.")
        st.rerun()
