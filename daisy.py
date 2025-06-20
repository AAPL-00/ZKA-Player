import asyncio
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.text import Text
from src.json_manager import load_repository, update_repository
from src.audio import init_mixer, play_playlist
from src.sorts import random_sort

console = Console()

async def main():
    init_mixer()

    # Super cute welcome message with bunny and daisy ASCII art
    console.print(Panel(
        Text(
            "🌼✨ ZA-Pwayew ✨🌼\n"
            "  (ᵘʷᵘ)  \n"
            "  /) /)  \n"
            " ( ˶• ₒ •˶ ) \n"
            "  >🌼<  \n"
            "  ~*~  \n"
            "Hiii! W-welcome to the cutest music pwayew eva! >w<",
            justify="center",
            style="bold magenta"
        ),
        title="🌼 ZA-Pwayew 🌼",
        border_style="bright_magenta",
        padding=(1, 2)
    ))

    repo = await load_repository()

    # Prompt for adding songs with a playful tone
    console.print("\n[bold bright_cyan]✨ Wanna add some cute songies? (y/n) >w<: [/bold bright_cyan]", end=" ")
    if input().lower() == 'y':
        console.print("[bold bright_cyan]🎀 Pwease give a path for your music fiwes: [/bold bright_cyan]", end=" ")
        ruta = input().strip()
        await update_repository(ruta)
        repo = await load_repository()  # Reload after modification
        console.print("\n[magenta]🌼 Yay! Songies added to your wibrary! >w<[/magenta]")

    # Display song list in a sparkly table
    table = Table(title="🎵 Your Cute Songies Wist! 🌟", title_style="bold bright_cyan", border_style="bright_magenta")
    table.add_column("✨ Titwe", style="magenta", no_wrap=True)
    table.add_column("🎤 Awtist", style="bright_cyan")
    table.add_column("💿 Awbum", style="bright_yellow")
    table.add_column("⏳ Timey (sec)", justify="right", style="green")

    for path, metadata in repo.items():
        title, album, artist, duration = metadata
        table.add_row(title, artist, album, f"{duration}")

    console.print(table)

    # Prompt for playback with extra sparkles
    console.print("\n[bold bright_cyan]🎶 Wanna pway your songies? (y/n) *giggles*: [/bold bright_cyan]", end=" ")
    if input().lower() == 'y':
        console.print("\n[bold magenta]🌼✨ Stawting super cute shuffwe pwayback! >w< 🎶[/bold magenta]")

        # Custom progress bar with a sparkly heart spinner
        async def play_with_progress(playlist):
            with Progress(
                SpinnerColumn(spinner_name="hearts", style="bright_magenta"),  # Heart spinner for extra cuteness
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress:
                task = progress.add_task("[magenta]Pwaying songies... 🌼✨", total=len(playlist) if playlist else 1)
                for path, title in playlist:
                    progress.update(task, description=f"[magenta]Pwaying {title}... 🌼✨")
                    await play_playlist([(path, title)])  # Pass single track as a list
                    progress.advance(task)
                progress.update(task, description="[magenta]Done pwaying aww songies! >w<")

        await play_with_progress(random_sort(repo))

if __name__ == "__main__":
    asyncio.run(main())
