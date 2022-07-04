import pyglet
from pymunk.pyglet_util import DrawOptions
from universe import Universe, Figure
from typing import List


class Simulation:
    def __init__(
            self, actions: List[int],
            figure: Figure,
            runtime: float = 10,  # in seconds
            fps: float = 1.0 / 30  # 30 frames per second
    ):

        self.actions = actions
        self.num_actions_per_second = runtime / len(actions)
        self.universe = Universe(figure)
        self.runtime = runtime
        self.fps = fps
        self.score: float = None

    def run(self) -> None:
        """Runs the simulation for n seconds

        Simulates the universe (makes a 30 fps step)
        Figure makes n moves per second (n* current_action)
        The overlap is calculated after making a move (4 fps)
        The ball is placed back when it reaches the left wall
        """
        current_time = 0.0
        current_action = 1
        runtime_reached = False

        while not runtime_reached:
            self.universe.space.step(self.fps)
            current_time = current_time + self.fps

            if current_action < (self.num_actions_per_second *current_time):
                movement = self.actions[current_action - 1]
                if movement == 1:
                    self.universe.move_left('up')
                if movement == 2:
                    self.universe.move_left('down')
                if movement == 3:
                    self.universe.move_right('up')
                if movement == 4:
                    self.universe.move_right('down')
                current_action = current_action + 1

                # self.universe.set_space_gravity(0)

            if current_time > self.runtime:
                runtime_reached = True

        self.score = self.universe.calculate_distance()

    def evaluate(self) -> float:
        return self.score


class Display(pyglet.window.Window):
    def __init__(
            self,
            actions: List[int],
            figure: Figure,
            label: str = '',
            runtime: float = 8.2
    ):

        super().__init__(width=1000, height=400, caption='Walking evolution ', resizable=False)
        self.actions = actions
        self.num_actions_per_second = runtime / len(actions)
        self.universe = Universe(figure)
        self.current_action = 1
        self.current_time = 0.0
        self.fps = 1.0 / 30
        self.runtime = runtime
        self.label = pyglet.text.Label(
            label, font_name='Arial', font_size=22,
            x=170, y=320, anchor_x='center', anchor_y='center',
        )
        self.score: float = None

    def on_draw(self) -> None:
        super().clear()
        self.universe.space.debug_draw(DrawOptions())
        self.label.draw()

    def update(self, dt) -> None:
        self.universe.space.step(self.fps)
        self.current_time = self.current_time + self.fps
        if self.current_action < (self.num_actions_per_second * self.current_time):
            movement = self.actions[self.current_action - 1]
            if movement == 1:
                self.universe.move_left('up')
            if movement == 2:
                self.universe.move_left('down')
            if movement == 3:
                self.universe.move_right('up')
            if movement == 4:
                self.universe.move_right('down')
            self.current_action = self.current_action + 1

        self.score = self.universe.calculate_distance()

        if self.current_time > self.runtime:
            self.close()

    def close(self) -> None:
        super().close()
        pyglet.app.exit()

    def display_simulation(self) -> None:
        pyglet.clock.schedule_interval(self.update, self.fps)
        pyglet.app.run()

    def get_score(self) -> float:
        return self.score
