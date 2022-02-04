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

class Resource:
    def __init__(self, **kwargs):
        self.possible_types = ('Hardware', 'Software')
        self.type = kwargs.get('type', self.possible_types[0])
        self.possible_states = ('Free', 'Busy')
        self.state = kwargs.get('state', self.possible_states[0])

    def _is_free(self) -> bool:
        return self.state == 'Free'

    def _reserve(self):
        self.state = 'Busy'

    def _free(self):
        self.state = 'Free'

class Process:
    process = []
    process_index = 0
    waiting_line = []
    def __init__(self, **kwargs):
        self.name = kwargs.get('name', f'T{self.__class__.process_index + 1}')
        self.priority = kwargs.get('priority', 0)
        self.possible_states = ('New', 'Active', 'Blocked', 'Finished')
        self.state = kwargs.get('state', self.possible_states[0])
        self.arrival_time = kwargs.get('arrival_time', 0)
        self.__class__.process.append(self)
        self.__class__.process_index += 1
        self.__class__._update_waiting_line(self)

    def __repr__(self) -> str:
        return '{name: %s, priority: %d, state: %s, arrival time: %d}' % (self.name, self.priority, self.state, self.arrival_time)

    def _is_waiting(self) -> bool:
        return self.state in ('New', 'Blocked')

    def _check_waiting(self):
        if not self._is_waiting(): 
            print(f'The {self.state} resource can not reserve a resource')
            raise

    def _execute(self):
        self.state = 'Active'

    @classmethod
    def _get_active_process(cls):
        for process in cls.process:
            if process._is_active():
                return process

    @classmethod
    def _inhertit_priority(cls, active_process, blocked_process):
        active_process.inherited_priority = blocked_process.inherited_priority

    @classmethod
    def _update_waiting_line(cls, process):
        waiting_line = cls.waiting_line
        if not process in waiting_line:
            waiting_line.append(process)
        cls.waiting_line = sorted(waiting_line, key=lambda p: (p.priority, p.arrival_time))


    @classmethod
    def _get_highets_waiting_priority_process(cls):
        return cls.waiting_line[0]
    
    @classmethod 
    def inherit_priority(cls):
        active_process = cls._get_active_process()
        blocked_process = cls._get_highets_waiting_priority_process()
        cls._inhertit_priority(active_process, blocked_process)

    def _reserve_resource(self, resource: Resource):
        self._check_waiting()
        if resource._is_free():
            resource._reserve()
            self._execute()
        else: 
            self.__class__._get_active_process()

    def _is_active(self) -> bool:
        return self.state == 'Active'

    def _check_active(self):
        if not self._is_active():
            print(f'The {self.state} resource can not free a resource')
            raise
        

    def _free_resource(self, resource: Resource):
        self._check_active()
        if resource._is_free(): 
            print('The resource is already free')
            raise
        resource._free()
        self.__class__._get_highets_waiting_priority_process()._reserve_resource(resource)

        


p1 = Process(priority=5)
p2 = Process(priority=3, arrival_time=3)
p3 = Process(priority=3, arrival_time=4)

# print(len(list(Process._get_process())))
print(Process._get_highets_waiting_priority_process())