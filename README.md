# DataDialogue AI 🏦

Sistema de consulta bancaria en lenguaje natural. Escribe o habla una pregunta y el sistema la convierte automáticamente en SQL, la ejecuta contra la base de datos y te responde en español.

## Tecnologías

- **LangChain + OpenAI GPT-4.1-mini** — conversión NL → SQL y respuesta natural
- **Supabase (PostgreSQL)** — base de datos bancaria en la nube
- **Streamlit** — interfaz web de chat
- **OpenAI Whisper** — transcripción de audio a texto
- **gTTS** — respuesta en audio

## Estructura de la base de datos

```
ciudad ←── clientes ←── cuentas ←── movimientos
```

| Tabla        | Descripción                         |
|--------------|-------------------------------------|
| ciudad       | Ciudades y departamentos            |
| clientes     | Datos personales de clientes        |
| cuentas      | Cuentas de ahorros y corriente      |
| movimientos  | Depósitos, retiros y transferencias |

## Setup

**1. Clonar el repositorio**
```bash
git clone https://github.com/Santy-417/Rag-DB-DataDialogueAI.git
cd Rag-DB-DataDialogueAI
```

**2. Instalar dependencias**
```bash
pip install -r requirements.txt
```
> Requiere `ffmpeg` instalado en el sistema para las funciones de audio.

**3. Configurar variables de entorno**
```bash
cp .env.example .env
# Editar .env con tu API key de OpenAI y la URL de Supabase
```

**4. Crear las tablas en Supabase**

Ir al SQL Editor de tu proyecto en Supabase y ejecutar el contenido de `setup_db.sql`.

**5. Correr la aplicación**
```bash
streamlit run streamlit_app.py
```

## Uso

- **Tab Texto**: escribe tu pregunta directamente en el chat
- **Tab Audio**: sube un archivo de audio (mp3/wav/m4a) con tu pregunta

Ejemplos de preguntas:
- *¿Qué clientes tienen cuentas corrientes?*
- *¿Cuál es el saldo total de todas las cuentas activas?*
- *¿Cuántos movimientos ha tenido la cuenta de Carlos Ramírez?*
- *¿Qué ciudad tiene más clientes registrados?*

## Flujo del sistema

```
Pregunta (texto o audio)
        ↓
  [Whisper STT]  ← solo si es audio
        ↓
  generar_sql()  → GPT-4.1-mini convierte a SQL
        ↓
ejecutar_sql_seguro()  → valida y ejecuta en Supabase
        ↓
generar_respuesta_natural()  → GPT interpreta los resultados
        ↓
  Respuesta en texto + [gTTS] audio opcional
```
