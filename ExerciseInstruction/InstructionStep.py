class InstructionStep():
    def __init__(self, index, instructions, completed=False):
        self.index = index
        self.instructions = instructions
        self.completed = completed

    def complete_step(self):
        self.completed = True


