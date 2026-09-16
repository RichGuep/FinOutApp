# FindOut

Aplicación de validación de procesos de **Greenmovil S.A.S.** (nómina y
bonificaciones del personal), construida en Python + Streamlit.

Primer módulo disponible: **Bonificación** — cruza los "Puntos PM
Conciliados" del DWH `GRMDW` (miproceso) contra el archivo plano de
bonificación que se carga manualmente en Excel.

---

## 1. Requisitos

- Python 3.10 o superior
- Acceso de red al DWH `10.0.22.78:5432` (base de datos `GRMDW`)

## 2. Instalación

```bash
cd FindOut
python -m venv .venv
source .venv/bin/activate      # En Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## 3. Configurar la conexión al DWH (obligatorio antes de usar Bonificación)

Por seguridad, la contraseña del DWH **nunca** se escribe en el código.
Se configura en un archivo local que no se sube a ningún repositorio:

```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

Edita `.streamlit/secrets.toml` y coloca la contraseña real:

```toml
[dwh]
host = "10.0.22.78"
port = 5432
database = "GRMDW"
user = "richard.guevara"
password = "TU_CONTRASEÑA_REAL"
```

> Alternativa rápida para pruebas: dentro del módulo Bonificación hay un
> expander **"Conexión manual al DWH"** en la barra lateral donde puedes
> escribir la contraseña solo para esa sesión, sin guardarla en ningún
> archivo.

## 4. Ejecutar la aplicación

```bash
streamlit run app.py
```

Se abrirá en `http://localhost:8501`.

## 5. Primer uso

1. La primera vez que abras la app, como no hay usuarios registrados, te
   pedirá crear la cuenta de **administrador**.
2. Con esa cuenta puedes ingresar y, desde **Gestión de usuarios**, crear
   cuentas adicionales (rol `usuario` o `admin`).
3. Los usuarios se guardan en `data/findout_users.db` (SQLite local, con
   contraseñas cifradas con bcrypt). Esta base es independiente del DWH.

## 6. Usar el módulo Bonificación

1. Selecciona el rango de fechas de las novedades a consultar en el DWH.
2. Decide si solo quieres considerar novedades con `Procede = Sí` (activado
   por defecto).
3. Carga el archivo plano de bonificación (Excel) con las columnas:
   `Identificación, Código, Empleado, Empresa, Cargo, Grupo, Días Novedad,
   Puntos PM Conciliados, Valor Bono, Vr Día, Vr Punto, Dcto Puntos,
   Dcto Días, A pagar`.
4. Elige con qué columna del archivo se relaciona el campo `Operador` del
   DWH (por defecto `Empleado`).
5. Pulsa **Ejecutar validación**. La app:
   - Suma `PuntosPmConciliados` del DWH agrupado por `Operador`.
   - Lo compara contra `Puntos PM Conciliados` del archivo.
   - Marca cada registro como `OK`, `ALERTA` (diferencia de puntos),
     `NO ENCONTRADO EN DWH` o `NO ENCONTRADO EN ARCHIVO`.
   - Muestra un resumen con métricas y una tabla coloreada por estado.
   - Permite descargar el reporte completo en Excel, ya resaltado.

## 7. Estructura del proyecto

```
FindOut/
├── app.py                     # App principal: login, navegación
├── auth.py                    # Autenticación y gestión de usuarios
├── db.py                      # Conexión y consultas al DWH GRMDW
├── requirements.txt
├── .streamlit/
│   ├── config.toml            # Tema de colores Greenmovil
│   └── secrets.toml.example   # Plantilla de credenciales (copiar y completar)
├── modules/
│   └── bonificacion.py        # Módulo 1: validador de bonificación
├── utils/
│   └── styling.py             # Estilos con la paleta #145A4F
└── data/
    └── findout_users.db       # Usuarios de la app (se crea automáticamente)
```

## 8. Notas y siguientes pasos

- El cruce se hace por nombre de operador (normalizado a mayúsculas y sin
  espacios extra) porque el DWH solo expone el campo `Operador` como texto.
  Si más adelante el DWH incorpora una identificación o código de operador,
  se puede cambiar el cruce a una llave numérica, más confiable.
- Próximos módulos de validación (nómina, etc.) se pueden agregar como
  nuevos archivos dentro de `modules/` y añadirlos al menú de `app.py`.
- Colores institucionales usados: `#145A4F` (primario), `#0D3B34`
  (sidebar), `#1F8A73` (secundario/éxito). Si tienes la guía de marca
  completa de Greenmovil, se pueden ajustar en `utils/styling.py`.
