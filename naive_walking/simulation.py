import pyglet
from pymunk.pyglet_util import DrawOptions
from universe import Universe, Figure
from typing import List


class Simulation:
    """Runs the simulation for n seconds

    Simulates the universe (30 fps)
    Figure makes n moves per second
    The overlap is calculated after making a move (e.g. 4 fps)
    The distance between figure and a right wall (i.e. finish position) is calculated in the end of the simulation time
    """
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
        current_time = 0.0
        current_action = 1
        runtime_reached = False

        while not runtime_reached:
            self.universe.space.step(self.fps)
            current_time += self.fps

            if current_action < (current_time / self.num_actions_per_second):
                movement = self.actions[current_action - 1]
                if movement == 0:
                    self.universe.move_left_poly('up')
                if movement == 1:
                    self.universe.move_left_poly('down')
                if movement == 2:
                    self.universe.move_right_poly('up')
                if movement == 3:
                    self.universe.move_right_poly('down')
                current_action = current_action + 1

                # calculate overlap between figure and obstacle every step
                self.universe.calculate_overlap()

            if current_time > self.runtime:
                runtime_reached = True

        # calculate the distance reached at the end of the simulation
        self.universe.calculate_distance()
        self.score = self.universe.score

    def evaluate(self) -> float:
        return self.score


class Display(pyglet.window.Window):
    """ Given a list of actions displays the simulation using Pyglet
    Similar code as in Simulation class.
    """
    def __init__(
            self,
            actions: List[int],
            figure: Figure,
            label: str = '',
            runtime: float = 10
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

        if self.current_action < (self.current_time / self.num_actions_per_second):
            movement = self.actions[self.current_action - 1]
            if movement == 0:
                self.universe.move_left_poly('up')
            if movement == 1:
                self.universe.move_left_poly('down')
            if movement == 2:
                self.universe.move_right_poly('up')
            if movement == 3:
                self.universe.move_right_poly('down')
            self.current_action = self.current_action + 1

            # calculate overlap between figure and obstacle every step
            self.universe.calculate_overlap()

        # calculate distance between figure and right wall in the end of the simulation
        if self.current_time > self.runtime:
            self.universe.calculate_distance()
            self.score = self.universe.score
            self.close()

    def close(self) -> None:
        super().close()
        pyglet.app.exit()

    def display_simulation(self) -> None:
        pyglet.clock.schedule_interval(self.update, self.fps)
        pyglet.app.run()

    def get_score(self) -> float:
        return self.score
