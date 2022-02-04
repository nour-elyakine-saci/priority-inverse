import resource


def type_input(type_to_input, *input_message):
    value = input(*input_message)
    while type(value) != type_to_input:
        try:
            value = type_to_input(value)
        except:
            print(value, 'could not be converted to', type_to_input, 'please enter a valid value')
            value = input(*input_message)
    else:
        return value

class ResourceCopy:
    def __init__(self, **kwargs) -> None:
        self.possible_types = ('Hardware', 'Software')
        self.type = kwargs.get('type', self.possible_types[0])
        self.possible_states = ('Free', 'Busy')
        self.state = kwargs.get('state', self.possible_states[0])

    def _switch_state(self) -> None:
        self.state = self.possible_states[self.state == self.possible_states[0]]

class Resource:
    def __init__(self, **kwargs) -> None:
        self.possible_types = ('Hardware', 'Software')
        self.type = kwargs.get('type', self.possible_types[0])
        self.copy_number = kwargs.get('copy_namber', 1)
        self.possible_states = ('Free', 'Busy')
        self.free_copies = kwargs.get('free_copies', self.copy_number)
        if self.free_copies > self.copy_number:
            raise ValueError('The number of free copies should be lower than or equal the total number of copies')
        self.busy_copies = kwargs.get('busy_copies', self._compute_busy_copies())
        if self.busy_copies + self.free_copies != self.copy_number:
            raise ValueError('The sum of the busy copies and the free copies should be equal to the total number of copies')
        self.state = kwargs.get('state', 'Free')

    def _compute_busy_copies(self) -> int:
        return self.copy_number - self.free_copies
    
    def compute_busy_copies(self) -> None:
        self.busy_copies = self._compute_busy_copies()      