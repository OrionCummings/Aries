from textual.containers import Container, Grid, Horizontal, Vertical
from textual.app import App, ComposeResult, RenderResult
from textual.reactive import Reactive
from textual.widget import Widget, Color
from textual.widgets import Static, Placeholder, Label, Pretty
from textual.message import Message
from textual import events
from RegisterFile import RegisterFile
from Constants import TextRenderTarget

COLOR_TEXT = Color.parse('#e0e1dd')
COLOR_BACKGROUND = Color.parse('#1b263b')

"""
This class must be focusable for the current set up! If a class
is not focusable, then it cannot receive input (i.e. on_click(), etc...)
"""
# class WidgetRegisterFile(Static, can_focus = True):
class WidgetRegisterFile(Widget, can_focus = True):
    """Display the current state of a register file."""

    rf = RegisterFile()

    def update(self) -> None:
        
        # Test: increment PC
        self.rf.increment_program_counter()
        
        # Update the displayed text
        labels = self.query(Label)
        for label in labels:
            reg_name = label._content[:2].strip()
            if reg_name == 'PC':
                content = self.rf.get_reg('PC').unwrap()
                formatted_content = format(content, "04x")
                label._content = f"PC 0x{formatted_content}"
                
        pass

    def on_mount(self) -> None:
        self.update()

    def on_key(self, event: events.Key) -> None:
        self.update()
        
    def compose(self) -> ComposeResult:
        yield Grid(
            Label("PC "),
            Label("SP "),
            Label("BP "),
            Label("FL "),
            Label("A "),
            Label("B "),
            Label("C "),
            Label("D "),
            Label("E "),
            Label("F "),
            Label("G "),
            Label("H "),
            Label("I "),
            Label("J "),
            Label("K "),
            Label("L "),
            id = "register_grid"
            )

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
        yield Grid(
            main_view
        )
        

if __name__ == "__main__":
    app = CustomApp()
    app.run()