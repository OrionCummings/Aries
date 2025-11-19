from textual.containers import Container
from textual.app import App, ComposeResult
from textual.widget import Color
from textual.widgets import Static
from textual import events
from Memory import Memory, MemoryRenderTarget

COLOR_TEXT = Color.parse('#e0e1dd')
COLOR_BACKGROUND = Color.parse('#1b263b')


class WidgetMemory(Static, can_focus = True):
    """Display the current state of memory."""

    memory = Memory(capacity=512)
    value = 1

    def on_mount(self) -> None:
        self.update_memory()
        

    def on_click(self) -> None:
        self.update_memory()
 
    def on_key(self, event: events.Key) -> None:
        self.update_memory()
        
    def update_memory(self) -> None:
        self.value *= 2
        self.memory.update(self.value, self.memory.size)
        self.memory.size += 1
        self.update(self.memory.to_string(MemoryRenderTarget.Widget))

class CustomApp(App):
    
    CSS_PATH = "tui.tcss"
    
    BINDINGS = [
        ('q', 'quit', 'quit'),
    ]
    
    def create_memory(self):
        widget_memory = WidgetMemory(id='data_memory')
        widget_memory.border_title = "Data Memory"
        widget_memory.styles.background = COLOR_BACKGROUND
        widget_memory.styles.color = COLOR_TEXT
        widget_memory.styles.border_title_align = 'center'
        return widget_memory
    
    def compose(self) -> ComposeResult:
        
        main_view = self.create_memory()
        yield Container(
            main_view
        )
        

if __name__ == "__main__":
    app = CustomApp()
    app.run()