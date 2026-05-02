import time
import pandas as pd
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table
from rich.text import Text
from rich import box

console = Console()


def log_consulta(pregunta: str, sql: str | None, resultado: pd.DataFrame | None,
                 respuesta: str, error: str | None, elapsed: float):
    console.print()

    # ── Pregunta ──────────────────────────────────────────────────────────────
    console.print(Panel(
        Text(pregunta, style="bold white"),
        title="[bold cyan]🗣  Pregunta[/bold cyan]",
        border_style="cyan",
        padding=(0, 1),
    ))

    if error:
        # ── Error ─────────────────────────────────────────────────────────────
        console.print(Panel(
            Text(error, style="bold red"),
            title="[bold red]✗  Error[/bold red]",
            border_style="red",
            padding=(0, 1),
        ))
    else:
        # ── SQL generado ──────────────────────────────────────────────────────
        if sql:
            syntax = Syntax(sql, "sql", theme="monokai", word_wrap=True)
            console.print(Panel(
                syntax,
                title="[bold yellow]⚙  SQL Generado[/bold yellow]",
                border_style="yellow",
                padding=(0, 1),
            ))

        # ── Resultados ────────────────────────────────────────────────────────
        if resultado is not None and not resultado.empty:
            table = Table(box=box.ROUNDED, border_style="green", header_style="bold green",
                          show_lines=True)
            for col in resultado.columns:
                table.add_column(str(col), style="white")
            for _, row in resultado.iterrows():
                table.add_row(*[str(v) for v in row])
            console.print(Panel(
                table,
                title=f"[bold green]📊  Resultados — {len(resultado)} fila(s)[/bold green]",
                border_style="green",
                padding=(0, 1),
            ))
        else:
            console.print(Panel(
                Text("Sin resultados", style="dim"),
                title="[bold green]📊  Resultados[/bold green]",
                border_style="green",
                padding=(0, 1),
            ))

        # ── Respuesta ─────────────────────────────────────────────────────────
        console.print(Panel(
            Text(respuesta, style="white"),
            title="[bold magenta]🤖  Respuesta[/bold magenta]",
            border_style="magenta",
            padding=(0, 1),
        ))

    # ── Tiempo ────────────────────────────────────────────────────────────────
    console.print(f"  [dim]⏱  {elapsed:.2f}s[/dim]\n")