import pandas as pd
from supabase import create_client, Client
from .config import settings

_client: Client | None = None

# Esquema fijo de la BD bancaria (evita consulta al servidor)
_ESQUEMA = """
Table: ciudad
Columns: id_ciudad (integer, PK), nombre_ciudad (varchar), departamento (varchar)

Table: clientes
Columns: id_cliente (integer, PK), nombre (varchar), apellido (varchar),
         documento (varchar, unique), fecha_nacimiento (date), id_ciudad (integer, FK->ciudad),
         telefono (varchar), correo (varchar)

Table: cuentas
Columns: id_cuenta (integer, PK), id_cliente (integer, FK->clientes), tipo_cuenta (varchar: Ahorros|Corriente),
         saldo (numeric), fecha_apertura (date), estado (varchar: Activa|Inactiva)

Table: movimientos
Columns: id_movimiento (integer, PK), id_cuenta (integer, FK->cuentas),
         fecha_movimiento (timestamp), tipo_movimiento (varchar: Depósito|Retiro|Transferencia),
         valor (numeric), descripcion (text)
"""


def get_client() -> Client:
    global _client
    if _client is None:
        _client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
    return _client


def get_schema() -> str:
    return _ESQUEMA.strip()


def ejecutar_query(sql: str) -> pd.DataFrame:
    """Ejecuta SQL arbitrario via Supabase RPC."""
    client = get_client()
    response = client.rpc("ejecutar_sql", {"query": sql}).execute()
    data = response.data
    if not data:
        return pd.DataFrame()
    return pd.DataFrame(data)