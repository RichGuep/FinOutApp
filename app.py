"""
FindOut - App principal.
Validador de procesos de Greenmovil S.A.S. (nómina y bonificaciones).
"""

import streamlit as st

import auth
import bonificacion
from styling import inject_css

st.set_page_config(
    page_title="FindOut | Greenmovil",
    page_icon="🟩",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_css()
auth.init_db()

if "usuario" not in st.session_state:
    st.session_state.usuario = None


def _header():
    st.markdown(
        '<div class="findout-header"><h1>FindOut</h1>'
        '<p>Validador de procesos — Greenmovil S.A.S.</p></div>',
        unsafe_allow_html=True,
    )


def pantalla_crear_admin():
    _header()
    st.info("No hay usuarios registrados todavía. Crea la cuenta de administrador para comenzar.")
    with st.form("crear_admin"):
        col1, col2 = st.columns(2)
        with col1:
            username = st.text_input("Usuario")
            nombre = st.text_input("Nombre completo")
        with col2:
            password = st.text_input("Contraseña", type="password")
            password2 = st.text_input("Confirmar contraseña", type="password")
        enviado = st.form_submit_button("Crear administrador", use_container_width=True)

    if enviado:
        if password != password2:
            st.error("Las contraseñas no coinciden.")
        else:
            ok, msg = auth.crear_usuario(username, password, nombre, rol="admin")
            if ok:
                st.success(msg + " Ahora puedes iniciar sesión.")
                st.rerun()
            else:
                st.error(msg)


def pantalla_login():
    _header()
    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        with st.form("login_form"):
            st.markdown("#### Iniciar sesión")
            username = st.text_input("Usuario")
            password = st.text_input("Contraseña", type="password")
            entrar = st.form_submit_button("Ingresar", use_container_width=True)
        if entrar:
            user = auth.verificar_usuario(username, password)
            if user:
                st.session_state.usuario = user
                st.rerun()
            else:
                st.error("Usuario o contraseña incorrectos, o usuario inactivo.")


def pantalla_gestion_usuarios():
    st.subheader("👥 Gestión de usuarios")

    with st.expander("➕ Crear nuevo usuario"):
        with st.form("crear_usuario_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                username = st.text_input("Usuario")
                nombre = st.text_input("Nombre completo")
            with col2:
                password = st.text_input("Contraseña", type="password")
                rol = st.selectbox("Rol", ["usuario", "admin"])
            crear = st.form_submit_button("Crear usuario")
        if crear:
            ok, msg = auth.crear_usuario(username, password, nombre, rol)
            (st.success if ok else st.error)(msg)

    st.markdown("#### Usuarios registrados")
    usuarios = auth.listar_usuarios()
    for u in usuarios:
        col1, col2, col3, col4, col5 = st.columns([2, 2, 1, 1, 1])
        col1.write(f"**{u['username']}**")
        col2.write(u["nombre_completo"] or "—")
        col3.write(u["rol"])
        col4.write("Activo" if u["activo"] else "Inactivo")
        etiqueta = "Desactivar" if u["activo"] else "Activar"
        if col5.button(etiqueta, key=f"toggle_{u['id']}"):
            auth.cambiar_estado_usuario(u["id"], not u["activo"])
            st.rerun()


def barra_lateral():
    with st.sidebar:
        st.markdown('<div class="sidebar-brand">FindOut</div>', unsafe_allow_html=True)
        nombre = st.session_state.usuario["nombre_completo"] or st.session_state.usuario["username"]
        st.caption(f"Sesión: {nombre}")
        st.caption(f"Rol: {st.session_state.usuario['rol']}")
        st.divider()

        opciones = ["Inicio", "Bonificación"]
        if st.session_state.usuario["rol"] == "admin":
            opciones.append("Gestión de usuarios")

        seleccion = st.radio("Módulos", opciones, label_visibility="collapsed")
        st.divider()

        if st.button("Cerrar sesión", use_container_width=True):
            st.session_state.usuario = None
            st.rerun()

    return seleccion


def pantalla_inicio():
    _header()
    st.markdown("Bienvenido/a. Selecciona un módulo en la barra lateral para comenzar.")
    st.markdown("### Módulos disponibles")
    st.markdown(
        "- **Bonificación**: cruce de Puntos PM Conciliados entre el DWH (miproceso) "
        "y el archivo plano de nómina/bonificación cargado."
    )
    st.caption("Próximamente se irán agregando más módulos de validación.")


def main():
    if not auth.hay_usuarios():
        pantalla_crear_admin()
        return

    if not st.session_state.usuario:
        pantalla_login()
        return

    seleccion = barra_lateral()

    if seleccion == "Inicio":
        pantalla_inicio()
    elif seleccion == "Bonificación":
        bonificacion.render()
    elif seleccion == "Gestión de usuarios":
        pantalla_gestion_usuarios()


if __name__ == "__main__":
    main()
