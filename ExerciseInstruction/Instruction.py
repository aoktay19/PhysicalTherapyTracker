class Instruction():
    def __init__(self, instruction_steps, is_completed=False):
        self.instruction_steps = instruction_steps
        self.is_completed = is_completed

    def add_instruction_step(self, instruction_Step):
        self.instruction_steps.append(instruction_Step)

    def find_next_instruction(self):
        if not self.check_instruction_is_completed():
            for index in range(len(self.instruction_steps)):
                if not self.instruction_steps[0].completed:
                    return self.instruction_steps[0]
                if self.instruction_steps[index].completed and not self.instruction_steps[index+1].completed:
                    return self.instruction_steps[index+1]

    def check_instruction_is_completed(self):
        return all(step.completed for step in self.instruction_steps)

    def reset_instruction(self):
        for step in self.instruction_steps:
            step.completed = False
