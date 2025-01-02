from textual.containers import Container
from textual.app import App, ComposeResult, RenderResult
from textual.reactive import Reactive
from textual.widget import Widget, Color
from textual.widgets import Static
from textual import events
from RegisterFile import RegisterFile, RegisterFileRenderTarget

COLOR_TEXT = Color.parse('#e0e1dd')
COLOR_BACKGROUND = Color.parse('#1b263b')

"""
This class must be focusable for the current set up! If a class
is not focusable, then it cannot receive input (i.e. on_click(), etc...)
"""
# class WidgetRegisterFile(Static, can_focus = True):
class WidgetRegisterFile(Static, can_focus = False):
    """Display the current state of a register file."""

    rf = RegisterFile()

    def on_mount(self) -> None:
        self.update_register_file()

    def on_click(self) -> None:
        self.update_register_file()

    def on_key(self, event: events.Key) -> None:
        self.update_register_file()
        
    def update_register_file(self) -> None:
        self.rf.increment_program_counter()
        self.update(self.rf.to_string(RegisterFileRenderTarget.Widget))

class CustomApp(App):
    
    CSS_PATH = "tui.tcss"
    
    BINDINGS = [
        ('q', 'quit', 'quit'),
    ]
    
    def create_register_file_widget(self):
        widget_register_file = WidgetRegisterFile()
        widget_register_file.border_title = "Register File"
        widget_register_file.styles.background = COLOR_BACKGROUND
        widget_register_file.styles.color = COLOR_TEXT
        widget_register_file.styles.border_title_align = 'center'
        return widget_register_file
    
    def compose(self) -> ComposeResult:
        
        main_view = self.create_register_file_widget()
        yield Container(
            main_view
        )
        

if __name__ == "__main__":
    app = CustomApp()
    app.run()