import pandas as pd
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from sqlalchemy import text

from .config import settings
from .database import get_db, get_schema

llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0, api_key=settings.OPENAI_API_KEY)

_prompt_sql = PromptTemplate(
    input_variables=["esquema_bd", "pregunta_usuario"],
    template="""Eres un experto en SQL para PostgreSQL. Dado el siguiente esquema de base de datos bancaria:

{esquema_bd}

Genera UNA SOLA consulta SQL válida para responder la siguiente pregunta del usuario.
Reglas estrictas:
- Solo usa tablas y columnas del esquema anterior. No inventes nombres.
- Solo genera consultas SELECT. Nunca DROP, DELETE, UPDATE, INSERT ni ALTER.
- Máximo 100 filas en el resultado (usa LIMIT 100).
- Respeta mayúsculas, tildes y género de los valores en los filtros.
- Responde ÚNICAMENTE con la consulta SQL, sin explicaciones ni texto adicional.

Pregunta: {pregunta_usuario}
SQL:"""
)

_prompt_respuesta = PromptTemplate(
    input_variables=["pregunta_usuario", "sql_generado", "resultado_tabular"],
    template="""Eres un asistente bancario amable que responde en español claro.

El usuario preguntó: {pregunta_usuario}

Se ejecutó la consulta SQL: {sql_generado}

El resultado fue:
{resultado_tabular}

Reglas para tu respuesta:
- No inventes información que no esté en el resultado.
- Si el resultado está vacío, dilo claramente.
- Enumera los hallazgos cuando sean varios.
- Sé conciso y directo.

Respuesta:"""
)

_cadena_sql = _prompt_sql | llm | StrOutputParser()
_cadena_respuesta = _prompt_respuesta | llm | StrOutputParser()


def generar_sql(pregunta: str) -> str:
    esquema = get_schema()
    return _cadena_sql.invoke({"esquema_bd": esquema, "pregunta_usuario": pregunta}).strip()


def ejecutar_sql_seguro(sql: str) -> pd.DataFrame:
    sql_lower = sql.strip().lower()
    if not sql_lower.startswith("select"):
        raise ValueError("Solo se permiten consultas SELECT.")
    bloqueadas = ["drop ", "delete ", "update ", "insert ", "alter "]
    if any(p in sql_lower for p in bloqueadas):
        raise ValueError("La consulta contiene instrucciones no permitidas.")
    db = get_db()
    with db._engine.connect() as conn:
        return pd.read_sql_query(text(sql), conn)


def generar_respuesta_natural(pregunta: str, sql: str, resultado: pd.DataFrame) -> str:
    resultado_tabular = resultado.to_string(index=False) if not resultado.empty else "(sin resultados)"
    return _cadena_respuesta.invoke({
        "pregunta_usuario": pregunta,
        "sql_generado": sql,
        "resultado_tabular": resultado_tabular
    }).strip()


def consultar_bd(pregunta: str) -> dict:
    try:
        sql = generar_sql(pregunta)
        resultado = ejecutar_sql_seguro(sql)
        respuesta = generar_respuesta_natural(pregunta, sql, resultado)
        return {"pregunta": pregunta, "sql": sql, "resultado": resultado, "respuesta": respuesta, "error": None}
    except Exception as e:
        return {"pregunta": pregunta, "sql": None, "resultado": None, "respuesta": f"Error: {e}", "error": str(e)}
