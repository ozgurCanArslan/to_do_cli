import typer
from rich.console import Console
from rich.table import Table
from core.model import Todo
from core.database import (
    get_all_todos,
    get_todos_category,
    delete_todo,
    insert_todo,
    complete_todo,
    update_todo,
)
from core.functions import (
    load_json,
    check_colors,
    update_categories,
)


CATEGORIES = load_json()


def complete_name():
    return [
        "add",
        "add-category",
        "complete",
        "del-category",
        "delete",
        "show",
        "show-category" "update",
        "update-category",
    ]


console = Console()

app = typer.Typer()


@app.command(short_help="adds an item")
def add(task: str, category: str):
    all_categories = load_json()
    if category in all_categories:
        typer.echo(f"adding {task}, {category}")
        todo = Todo(
            task,
            category,
        )
        insert_todo(todo)
    else:
        typer.echo(f"category is not found {task}, {category}")
    show()


@app.command(short_help="adds an item to categories")
def add_category(category: str, color: str):
    typer.echo(f"adding {category}")
    update_categories(method="add", field=category, color=color)
    show()


@app.command(short_help="delete an item")
def delete(position: int):
    typer.echo(f"deleting {position}")
    # indices in UI begin at 1, but in database at 0
    delete_todo(position - 1)
    show()


@app.command(short_help="delete a category")
def del_category(category: int):
    typer.echo(f"deleting {category}")
    update_categories(method="del", field=category)


@app.command(short_help="update task and category")
def update(position: int, task: str = None, category: str = None):
    typer.echo(f"updating {position}")
    update_todo(position - 1, task, category)
    show()


@app.command()
def update_category(category: str, new_category: str = None, color: str = None):
    typer.echo(f"updating {category}")
    update_categories(
        method="updated", field=category, new_field=new_category, color=color
    )
    show()


@app.command()
def complete(position: int):
    typer.echo(f"complete {position}")
    complete_todo(position - 1)
    show()


@app.command()
def show():
    typer.echo(f"Categories: {CATEGORIES}")
    tasks = get_all_todos()
    console.print("[bold magenta]Todos[/bold magenta]!", "💻")
    table = Table(show_header=True, header_style="bold blue")
    table.add_column("#", style="dim", width=6)
    table.add_column("Todo", min_width=20)
    table.add_column("Date", min_width=12, justify="right")
    table.add_column("Category", min_width=12, justify="right")
    table.add_column("Done", min_width=12, justify="right")

    def get_category_color(category):
        check_colors()
        colors = load_json()
        try:
            if category in colors:
                return colors[category]
        except Exception:
            return "white"

    for idx, task in enumerate(tasks, start=1):
        c = get_category_color(task.category)
        is_done_str = "✅" if task.status == 2 else "❌"
        table.add_row(
            str(idx),
            task.task,
            f"[{c}]{task.date}[/{c}]",
            f"[{c}]{task.category}[/{c}]",
            is_done_str,
        )
    console.print(table)


@app.command()
def show_category(category: str):
    typer.echo(f"Categories: {CATEGORIES}")
    if category == "all":
        tasks = get_all_todos()
    else:
        tasks = get_todos_category(category=category)
    console.print("[bold magenta]Todos[/bold magenta]!", "💻")

    table = Table(show_header=True, header_style="bold blue")
    table.add_column("#", style="dim", width=6)
    table.add_column("Todo", min_width=20)
    table.add_column("Date", min_width=12, justify="right")
    table.add_column("Category", min_width=12, justify="right")
    table.add_column("Done", min_width=12, justify="right")

    def get_category_color(category):
        check_colors()
        colors = load_json()
        try:
            if category in colors:
                return colors[category]
        except Exception:
            return "white"

    for idx, task in enumerate(tasks, start=1):
        c = get_category_color(task.category)
        is_done_str = "✅" if task.status == 2 else "❌"
        table.add_row(
            str(idx),
            task.task,
            f"[{c}]{task.date}[/{c}]",
            f"[{c}]{task.category}[/{c}]",
            is_done_str,
        )
    console.print(table)


if __name__ == "__main__":
    app()
