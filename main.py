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
    process_count = 0
    waiting_line = []
    resource = Resource()
    def __init__(self, arrival_time=0, execution_duration=0, priority=0, **kwargs):
        self.name = kwargs.get('name', f'T{self.__class__.process_count + 1}')
        self.arrival_time = arrival_time
        self.execution_duration = execution_duration
        self.remaining_execution_duration = self.execution_duration
        self.priority = priority
        self.inherited_priority = self.priority
        self.state = 'New'
        self.__class__._update_process_list(self)

    def __repr__(self) -> str:
        return '{name: %s, priority: %d, state: %s, arrival time: %d, remaining execution duration: %d}' % (self.name, self.priority, self.state, self.arrival_time, self.remaining_execution_duration)

    @classmethod
    def _update_process_list(cls, process):
        cls.process.append(process)
        cls.process = sorted(cls.process, key=lambda p: (p.arrival_time, p.inherited_priority))
        cls.process_count += 1

    def _is_waiting(self) -> bool:
        return self.state in ('New', 'Blocked')

    def _check_waiting(self):
        if not self._is_waiting(): 
            print(f'The {self.state} resource can not reserve a resource')
            raise

    def _execute(self):
        self.state = 'Active'
        self.remaining_execution_duration -= 1
        if self.remaining_execution_duration == 0:
            self._free_resource()

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
        if process not in waiting_line:
            waiting_line.append(process)
        cls.waiting_line = sorted(waiting_line, key=lambda p: (p.inherited_priority, p.arrival_time), reverse=True)


    @classmethod
    def _get_highets_waiting_priority_process(cls):
        if cls.waiting_line:
            process = cls.waiting_line.pop(0)
            return process
    
    @classmethod 
    def inherit_priority(cls):
        active_process = cls._get_active_process()
        blocked_process = cls._get_highets_waiting_priority_process()
        cls._inhertit_priority(active_process, blocked_process)

    def _reserve_resource(self):
        self._check_waiting()
        resource = self.__class__.resource
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
        

    def _free_resource(self):
        self._check_active()
        resource = self.__class__.resource
        if resource._is_free(): 
            print('The resource is already free')
            raise
        resource._free()
        self.state = 'Finished'


process_count = type_input(int, 'Process count: ')

for counter in range(process_count):
    print()
    print('***')
    print(f'Process {counter + 1}: ')
    arrival_time = type_input(int, 'Arrival time: ')
    execution_duration = type_input(int, 'Execution duration: ')
    priority = type_input(int, 'Priority: ')
    Process(arrival_time=arrival_time, execution_duration=execution_duration, priority=priority)
    print('***')

total_execution_duration = type_input(int, 'Total execution duration: ')
process = None
active_process = None

for t in range(total_execution_duration):
    print()
    print('***')
    print(f'Time: t{t}')
    while Process.process and t == Process.process[0].arrival_time:
        process = Process.process.pop(0)
        process.state = 'Blocked'
        Process._update_waiting_line(process)
    else:
        if Process.waiting_line:
            process = Process.waiting_line[0]
    if process is not None:
        if Process.resource._is_free():
            process = Process.waiting_line.pop(0)
            process.state = 'Active'
            active_process = process
            Process.resource._reserve()
        else:
            if active_process is not None and active_process.inherited_priority < process.priority:
                process.state = 'Blocked'
                active_process.inherited_priority = process.priority
        process = None
    print('Waiting line:', Process.waiting_line)
    if active_process is not None:
        print('Active process:', active_process)
        active_process.remaining_execution_duration -= 1
        if active_process.remaining_execution_duration == 0:
            active_process.state == 'Finished'
            active_process.inherited_priority = active_process.priority
            active_process = None
            Process.resource._free()
    print('***')
