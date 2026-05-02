# DataDialogue AI — CLAUDE.md

## Descripción
Sistema RAG (Retrieval-Augmented Generation) que convierte preguntas en lenguaje natural a SQL y las ejecuta contra una base de datos bancaria en Supabase. Tiene interfaz Streamlit con soporte de texto y audio.

## Estructura del proyecto
```
rag-db/
├── app/
│   ├── config.py        # Carga .env con pydantic-settings
│   ├── database.py      # Conexión SQLAlchemy → Supabase (PostgreSQL)
│   ├── rag_chain.py     # Pipeline: NL → SQL → respuesta natural
│   └── audio.py         # Whisper (STT) + gTTS (TTS)
├── streamlit_app.py     # UI principal
├── setup_db.sql         # Script SQL con tablas e INSERT de ejemplo
├── requirements.txt
├── .env.example
└── .gitignore
```

## Variables de entorno (.env)
```
OPENAI_API_KEY=sk-proj-...
SUPABASE_DB_URL=postgresql://postgres:[PASSWORD]@[HOST]:5432/postgres
```
El `.env` nunca va al repositorio. Copiar `.env.example` y rellenar.

## Cómo correr el proyecto
```bash
pip install -r requirements.txt
# Ejecutar el SQL en Supabase SQL Editor (solo la primera vez)
# Crear .env con las credenciales
streamlit run streamlit_app.py
```

## Base de datos (Supabase)
4 tablas relacionadas: `ciudad`, `clientes`, `cuentas`, `movimientos`.
El script `setup_db.sql` crea las tablas y carga datos de ejemplo.
Se conecta vía SQLAlchemy usando `SUPABASE_DB_URL`.

## Pipeline NL→SQL (`app/rag_chain.py`)
1. `generar_sql(pregunta)` — LLM convierte pregunta a SQL
2. `ejecutar_sql_seguro(sql)` — valida que sea SELECT y ejecuta
3. `generar_respuesta_natural(pregunta, sql, df)` — LLM interpreta resultados
4. `consultar_bd(pregunta)` — orquesta todo, retorna dict

## Modelo usado
- LLM: `gpt-4.1-mini` con `temperature=0`
- Whisper: modelo `base` (balance velocidad/precisión)

## Notas de desarrollo
- El modelo Whisper se carga de forma lazy (primera llamada a `transcribir_audio`)
- El audio de respuesta se guarda en un archivo temporal (se borra al reiniciar)
- Solo se permiten consultas SELECT en `ejecutar_sql_seguro`
