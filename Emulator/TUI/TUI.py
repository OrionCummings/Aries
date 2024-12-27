from textual.app import App, ComposeResult
from textual.containers import Container, VerticalScroll
from textual.reactive import Reactive
from textual.binding import Binding
from textual.widgets import Placeholder
from textual.widgets import Footer
from textual.widgets import DataTable
from textual.widgets import Header
from textual.color import Color

FILENAME = "ldi.aria"

DISASSEMBLY_HEADER = ["address", "instruction"]
ROWS_RAW = [
"ldi 1 A",
"ldi 2 B",
"ldi 4 C",
"ldi 8 D",
"ldi 16 E",
"ldi 32 F",
"ldi 64 G",
"ldi 128 H",
"ldi 256 I",
"ldi 512 J",
"ldi 1024 K",
"ldi 2048 L",
"ldi 1 A",
"ldi 2 B",
"ldi 4 C",
"ldi 8 D",
"ldi 16 E",
"ldi 32 F",
"ldi 64 G",
"ldi 128 H",
"ldi 256 I",
"ldi 512 J",
"ldi 1024 K",
"ldi 2048 L",
"hlt",
]

ROWS = list(enumerate(ROWS_RAW))

COLOR_HEADER = Color.parse('#415a77')
COLOR_FOOTER = Color.parse('#415a77')
COLOR_TEXT = Color.parse('#e0e1dd')
COLOR_BACKGROUND = Color.parse('#1b263b')

class CPUApp(App):
    CSS_PATH = "tui.tcss"

    BINDINGS = [
        Binding(key="q", action="quit", description="quit"),
        Binding(key="space", action="step", description="execute one clock cycle"),
        Binding(key="UP", action="disassembly_up", description="select previous instruction"),
        Binding(key="DOWN", action="disassembly_down", description="select next instruction"),
        Binding(key="c", action="run_breakpoint", description="run to next breakpoint"),
        Binding(key="b", action="set_breakpoint", description="set a breakpoint"),
    ]
    
    def create_header(self):
        (widget_header,) = Header(icon=None, time_format="%H:%M:%S", show_clock=True, id="header"),
        widget_header.styles.background = COLOR_HEADER
        widget_header.styles.color = COLOR_TEXT
        return widget_header

    def create_footer(self):
        widget_footer = Footer(show_command_palette=False)
        widget_footer.styles.background = COLOR_FOOTER
        return widget_footer
        
    def create_program_disassembly(self):
        widget_program_disassembly_table = DataTable(id="program_disassembly")
        widget_program_disassembly_table.border_title = f"Disassembly of {FILENAME}"
        widget_program_disassembly_table.styles.background = COLOR_BACKGROUND
        widget_program_disassembly_table.styles.color = COLOR_TEXT
        widget_program_disassembly_table.styles.border_title_align = 'center'
        return widget_program_disassembly_table

    def create_register_file(self):
        widget_register_file = Placeholder(" ", id="register_file")
        widget_register_file.border_title = "Register File"
        widget_register_file.styles.background = COLOR_BACKGROUND
        widget_register_file.styles.color = COLOR_TEXT
        widget_register_file.styles.border_title_align = 'center'
        return widget_register_file

    def create_data_memory(self):
        widget_data_memory = Placeholder(" ", id="data_memory")
        widget_data_memory.border_title = "Data Memory"
        widget_data_memory.styles.background = COLOR_BACKGROUND
        widget_data_memory.styles.color = COLOR_TEXT
        widget_data_memory.styles.border_title_align = 'center'
        return widget_data_memory

    def compose(self) -> ComposeResult:
        
        # Create each widget
        widget_header = self.create_header()
        widget_footer = self.create_footer()
        widget_program_disassembly_table = self.create_program_disassembly()
        widget_register_file = self.create_register_file()
        widget_data_memory = self.create_data_memory()
        
        # Create a container with all three main widgets
        
        container_main_view = Container(
                widget_program_disassembly_table,
                widget_register_file,
                widget_data_memory,
                id="main_view",
            )
        
        # Create a vertical scroll widget containing a header, footer, and content
        yield VerticalScroll(
            widget_header,
            container_main_view,
            widget_footer
        )
        
        
        # yield VerticalScroll(
        #     Container(
        #         Header(icon=None, time_format="%H:%M:%S", show_clock=True, id="header"),
        #         # Placeholder("Program Dissassembly", id="program_dissassembly"),
        #         DataTable(id="program_dissassembly"),
        #         Placeholder("Register File", id="register_file"),
        #         Placeholder("Data Memory", id="data_memory"),
        #         id="page",
        #     ),
        #     Footer(show_command_palette=False),
        # )

    def on_mount(self) -> None:
        
        # Header
        self.title = "Aires CPU Emulator"
        
        # Footer
        
        
        # Table
        program_dissassembly = self.query_one(DataTable)
        program_dissassembly.add_columns(*DISASSEMBLY_HEADER)
        program_dissassembly.add_rows(ROWS)
        program_dissassembly.expand = True
        program_dissassembly.cursor_type = "row"

if __name__ == "__main__":
    app = CPUApp()
    app.run()   