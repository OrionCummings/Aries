from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, VerticalScroll
from textual.widgets import Placeholder
from textual.binding import Binding
from textual.widgets import Footer

class PlaceholderApp(App):
    CSS_PATH = "placeholder.tcss"

    BINDINGS = [
        Binding(key="q", action="quit", description="Quit the app"),
        Binding(key="space", action="step", description="Execute one clock cycle"),
    ]

    def compose(self) -> ComposeResult:
        yield VerticalScroll(
            Container(
                Placeholder("Program Dissassembly", id="program_dissassembly"),
                Placeholder("Register File", id="register_file"),
                Placeholder("Data Memory", id="data_memory"),
                id="page",
            ),
            Footer(),
        )

if __name__ == "__main__":
    app = PlaceholderApp()
    app.run()   