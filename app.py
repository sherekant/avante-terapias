import streamlit as st
import pandas as pd
import os

# 1. Configuración de página y Título
st.set_page_config(page_title="Fundación Avante", layout="wide")

# Intentar cargar el logo (debes subirlo a GitHub como logo.png)
if os.path.exists("logo.png"):
    st.image("logo.png", width=300)

st.title("Fundación Avante")
st.subheader("Intervención Especializada en Autismo")

DATA_FILE = 'horarios_avante.csv'
COLUMNAS = ["Hora", "ID_Paciente", "Nombre_Paciente", "Terapeuta", "Consultorio", "Observacion", "Estado"]

if not os.path.exists(DATA_FILE):
    df_init = pd.DataFrame(columns=COLUMNAS)
    df_init.to_csv(DATA_FILE, index=False)

def load_data():
    return pd.read_csv(DATA_FILE)

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

# 2. Menú principal
menu = st.sidebar.radio(
    "Selecciona la vista:", 
    ["📱 Vista Padres (Buscar)", "📺 Vista TV (1er Piso)", "⚙️ Administración"]
)

# 3. Vista de Padres (Búsqueda por ID o Nombre)
if menu == "📱 Vista Padres (Buscar)":
    st.write("### Encuentra la terapia de tu hijo/a")
    df = load_data()
    
    search = st.text_input("Escribe el Número de ID o el Nombre del paciente:", placeholder="Ejemplo: 10234 o Sebastian")
    
    if search:
        # Busca tanto por número de ID como por nombre
        resultados = df[(df["ID_Paciente"].astype(str).str.contains(search, case=False, na=False)) | 
                        (df["Nombre_Paciente"].astype(str).str.contains(search, case=False, na=False))]
        
        if not resultados.empty:
            st.success("Terapia encontrada:")
            st.dataframe(resultados, use_container_width=True, hide_index=True)
        else:
            st.warning("No se encontraron terapias asignadas para este dato.")

# 4. Vista TV (Actualización automática)
elif menu == "📺 Vista TV (1er Piso)":
    st.write("### Horarios Generales de Terapias")
    st.components.v1.html("<meta http-equiv='refresh' content='60'>", height=0)
    df = load_data()
    st.dataframe(df, use_container_width=True, hide_index=True)

# 5. Administración (Protegida con contraseña y con subida de Excel)
elif menu == "⚙️ Administración":
    
    password = st.sidebar.text_input("Contraseña de acceso:", type="password")
    
    # La contraseña por defecto es avante123
    if password == "avante123":
        st.success("Candado abierto: Modo Administrador")
        
        st.write("### 1. Subir Excel del Día")
        st.info("Tu archivo Excel debe tener estas columnas en la primera fila: Hora, ID_Paciente, Nombre_Paciente, Terapeuta, Consultorio, Observacion, Estado")
        archivo_subido = st.file_uploader("Sube el archivo Excel o CSV", type=["xlsx", "csv"])
        
        if archivo_subido is not None:
            try:
                if archivo_subido.name.endswith('.csv'):
                    df_nuevo = pd.read_csv(archivo_subido)
                else:
                    df_nuevo = pd.read_excel(archivo_subido)
                save_data(df_nuevo)
                st.success("Base de datos cargada con éxito. Se está proyectando en el TV.")
            except Exception as e:
                st.error(f"Error al leer el archivo: {e}")

        st.divider()
        st.write("### 2. Administrar Terapias (Editar, Agregar o Quitar casillas)")
        st.write("Haz clic en cualquier celda para editarla. Usa el botón '+' al final para agregar terapias, o selecciona una fila y bórrala con el ícono de papelera.")
        
        df = load_data()
        
        # Tabla inteligente que permite agregar y quitar casillas libremente
        df_modificado = st.data_editor(df, num_rows="dynamic", use_container_width=True)
        
        if st.button("Guardar Cambios Manuales"):
            save_data(df_modificado)
            st.success("¡Cambios guardados y actualizados en el sistema!")
            
        st.divider()
        if st.button("Borrar todos los registros (Cerrar el día)"):
            df_clean = pd.DataFrame(columns=COLUMNAS)
            save_data(df_clean)
            st.success("Sistema limpio para mañana.")
            st.rerun()
            
    elif password != "":
        st.error("Contraseña incorrecta.")
    else:
        st.warning("Por favor, introduce la contraseña en el menú lateral izquierdo para gestionar los horarios.")
