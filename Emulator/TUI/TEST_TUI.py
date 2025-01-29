from itertools import cycle

from textual.app import App, ComposeResult
from textual.widgets import Static
from textual.widgets import Header, Footer
from textual.widgets import Footer, Header, Static
from textual import events

hellos = cycle(
    [
        "Hola",
        "Bonjour",
        "Guten tag",
        "Salve",
        "Nǐn hǎo",
        "Olá",
        "Asalaam alaikum",
        "Konnichiwa",
        "Anyoung haseyo",
        "Zdravstvuyte",
        "Hello",
    ]
)


class Hello(Static, can_focus=True):
    """Display a greeting."""

    def on_mount(self) -> None:
        self.next_word()

    def on_click(self) -> None:
        self.next_word()

    def next_word(self) -> None:
        """Get a new hello and update the content area."""
        hello = next(hellos)
        self.update(f"{hello}, [b]World[/b]!")

    def on_key(self, event: events.Key) -> None:
        print("key sent")
        self.next_word()


class CustomApp(App):
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]
    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield Hello()




if __name__ == "__main__":
    app = CustomApp()
    app.run() 