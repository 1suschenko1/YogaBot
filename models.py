class WorkoutPlan:
    def __init__(self, goal, level):
        self.goal = goal
        self.level = level

    def generate_plan(self):
        return f"План для цели: {self.goal}, уровень: {self.level}"
