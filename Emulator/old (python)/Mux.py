

class Mux:

    def __init__(self, num_inputs: int = 2):

        # Set up inputs
        self.num_inputs = num_inputs
        self.inputs: list[bool] = [False] * num_inputs

        self.selector = 0

    def __str__(self) -> str:
        return str(int(self.inputs[self.selector] == True))

    def get_value(self) -> bool:
        return self.inputs[self.selector]
    
    def set_input(self, index, value) -> None:

        assert index < self.num_inputs
        
        self.inputs[index] = value
    
    def set_inputs(self, inputs) -> None:

        assert len(inputs) == self.num_inputs

        for index in range(0, len(inputs)):
            self.inputs[index] = inputs[index]

    def set_selector(self, index) -> None:

        assert index < self.num_inputs
        
        self.selector = index







