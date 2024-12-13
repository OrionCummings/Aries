from __future__ import annotations

class DeltaType:

    def __init__(self):
        self.current_value  = None
        self.previous_value = None

    def __str__(self) -> str:
        return "{} ({})".format(str(self.current_value), str(self.previous_value))

    def __eq__(self, other: DeltaType) -> bool:
        return (self.current_value == other.current_value and self.previous_value == other.previous_value)

    def update(self, value) -> None:
        self.previous_value = self.current_value
        self.current_value = value

    def changed(self) -> bool:
        return self.current_value != self.previous_value