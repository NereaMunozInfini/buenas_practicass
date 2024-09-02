import openai
import streamlit as st
from streamlit import runtime
runtime.exists()

avatar = {
    'user': 'lorelei',
    'assistant': 'pixel-art'
}

st.image("https://www.infini.es/wp-content/uploads/2022/10/1.-INFINI_logotipo_negro.png", width=130)
#st.title("Chat Buenas Prácticas 💬")
st.markdown("<h1 style='font-size: 32px;'>Chat Mejores Prácticas 💬</h1>", unsafe_allow_html=True)

with st.sidebar:
    
    st.title('Configuraciones')
        # if ('APIKEY' in st.secrets) and ('IDMODEL' in st.secrets):
    #     st.success('Credenciales secretas cargadas!', icon='✅')
    #     api_key = st.secrets['APIKEY']
    #     id_model = st.secrets['IDMODEL']
    
    # else:
    placeholder = st.empty()

    # Quitamos la parte de la izquierda
    #api_key = st.text_input('API Key:', placeholder='Aquí tu API Key de OpenAI', type='password')
    #id_model = st.text_input('Id Modelo:', placeholder='Id de tu modelo de fine-tuning', type='password')

    api_key = st.secrets["api_key"]
    id_model = "ft:gpt-4o-2024-08-06:personal:bestpractices8:A1DsNAL7"

    # with placeholder.container():
    #     if not (api_key and id_model):
    #         st.warning('Por favor, ingresa tus credenciales!', icon='⚠️')
    #     else:
    #         st.success('Ingresar credenciales:', icon='👉')
            
    # system_message = st.text_area(label='Mensaje de sistema:',
    #                             height=180,
    #                             placeholder='Instrucciones que complementan el comportamiento de tu modelo de fine-tuning. Ej: Responde siempre alegre.')
    
    system_message = "Instrucciones: Entrada: Un fragmento de código en Python. Salida: Para cada criterio: Indicar la categoría del criterio. Indicar si se cumple o no. Si no se cumple, proporcionar un fragmento de código revisado y una breve explicación del problema y la solución. Al final, proporcionar una calificación basada en el número de criterios que el código original cumplió . Criterios: PEP8 Uso Adecuado de Espacios y Líneas en Blanco, PEP8 Nomenclatura Correcta, PEP8 Convenciones de Programación, Uso de Nombres de Variables Descriptivos, Manejo Adecuado de Casos Extremos y Entradas No Permitidas, Evitar Repetición de Código, Evitar Números Mágicos, Funciones Desglosadas (No Monolíticas), Docstrings Adecuados, Comentarios Adecuados, Lógica Simplificada, Código Limpio, Uso Adecuado de Objetos en Lugar de Funciones, Evitar Reinventar la Rueda"
    memory = st.slider(label='Memoria conversación (num. mensajes):',value=4, min_value=1)
    #temp = st.slider(label='Creatividad (temperatura):',value=0.5, min_value=0.0, max_value=2.0, step=0.1)
    temp = 0.18

    openai.api_key = api_key
    

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": system_message},
        ]

for message in st.session_state.messages:
    if message['role']=='system': continue
    with st.chat_message(message["role"]):
        st.write(message["content"])

def clear_chat_history():
    st.session_state.messages = st.session_state.messages = [
        {"role": "system", "content": system_message},
        ]
st.sidebar.button('Limpiar chat', on_click=clear_chat_history)

def generate_response(model):
    history = [st.session_state.messages[0]] + st.session_state.messages[-memory:] if len(st.session_state.messages) > 5 else st.session_state.messages
    response = openai.ChatCompletion.create(  # Cambiado aquí
                        model=model,
                        messages=history,
                        temperature=temp,
                        max_tokens=2000
                    )
    msg = response.choices[0].message['content']  # Asegúrate de extraer el mensaje de la respuesta correctamente
    return msg


# if prompt := st.chat_input(disabled=not (api_key and id_model), placeholder='Tú mensaje...'):
#     st.session_state.messages.append({"role": "user", "content": prompt})
#     with st.chat_message("user"):
#         st.write(prompt)

if prompt := st.chat_input(placeholder='Tú mensaje...'):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

if st.session_state.messages[-1]["role"] == "user":
    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            response = generate_response(id_model) 
            st.write(response) 
    message = {"role": "assistant", "content": response}
    st.session_state.messages.append(message)