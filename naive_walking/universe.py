import pymunk
from pymunk import Vec2d
from typing import Tuple


class Polygon:
    """ Creating a single Polygon shape in Pymunk:
    Coordinates of each point and mass of the shape
    """
    def __init__(
            self,
            left: float,  # local coordinates to create polygon shape
            bottom: float,
            right: float,
            top: float,
            mass: float = 1.0  # adding mass to polygon shape
    ):
        self._points = (left, bottom, right, top)
        self._mass = mass
        self._shape = self._create_shape()
        self._body = self._create_body()

    def _create_shape(self) -> pymunk.Poly:
        shape = pymunk.Poly(None, self._points)
        shape.filter = pymunk.ShapeFilter(categories=1)
        return shape

    def _create_body(self) -> pymunk.Body:
        vertices = self._shape.get_vertices()
        moment = pymunk.moment_for_poly(self._mass, vertices, offset=(10, 10))
        body = pymunk.Body(self._mass, moment)
        #body.friction = 10000000.0
        self._shape.body = body
        return body

    def set_center_of_gravity(self, center: Tuple[float, float]) -> None:
        self._shape.body.center_of_gravity = center

    def set_position(self, position) -> None:
        self._body.position = position

    def get_position(self) -> float:
        return self._body.position

    @property
    def shape(self) -> pymunk.Poly:
        return self._shape

    @property
    def body(self) -> pymunk.Body:
        return self._body

    @property
    def points(self) -> Tuple[int, int, int, int]:
        return self._points

    @property
    def centroid(self) -> Tuple[int, int]:
        center = self._shape.bb.center().int_tuple
        return center


class Joint:
    def __init__(self, joint, motor):
        self._joint = joint
        self._motor = motor

    @property
    def motor(self) -> pymunk.SimpleMotor:
        return self._motor

    @property
    def joint(self) -> pymunk.PivotJoint:
        return self._joint


class Figure:
    """ A class that represents our 2D polygon robot:
    We create 3 polygon shapes (i.e. two legs and one center body).
    and attach 2 joints and 2 motors between each leg and center body.
    A figure moves by rotating changing motor rates to -1000 or 1000 (move right, move left)
    """
    def __init__(self):

        self._center_poly = None
        self._left_poly = None
        self._right_poly = None

        self._left_joint = None
        self._right_joint = None

        center_poly = Polygon((-35, 20), (35, 20), (30, 45), (-30, 45), mass=0.1)
        left_poly = Polygon((-20, 20), (-28, 7), (-20, -20), (-13, 7), mass=0.4)
        right_poly = Polygon((20, 20), (12, 7), (20, -20), (28, 7), mass=0.4)

        self.create_center_poly(center_poly)
        self.create_left_poly(left_poly)
        self.create_right_poly(right_poly)

    def create_center_poly(self, polygon: Polygon) -> None:
        polygon.set_position((100, 70))
        self._center_poly = polygon

    def create_right_poly(self, polygon: Polygon) -> None:
        """Creates the right polygon

        Sets its positon to the center of the window
        attaches right poly to the center poly using a pivot joint
        adds motor to the joint to control movements
        """
        polygon.set_position((100, 70))

        pivot_point = polygon.points[0]
        joint = pymunk.PivotJoint(
            self._center_poly.body, polygon.body, pivot_point, pivot_point
        )
        motor = pymunk.SimpleMotor(
            polygon.body, self._center_poly.body, 0
        )
        motor.collide_bodies = True
        motor.max_force = 3000
        self._right_joint = Joint(joint, motor)
        self._right_poly = polygon

    def create_left_poly(self, polygon: Polygon) -> None:
        """Creates the left polygon

        Sets its positon to the center of the window
        attaches left poly to the center poly using a pivot joint
        adds motor to the joint to control movements
        """
        polygon.set_position((100, 70))

        pivot_point = polygon.points[0]
        joint = pymunk.PivotJoint(
            self._center_poly.body, polygon.body, pivot_point, pivot_point
        )
        motor = pymunk.SimpleMotor(
            polygon.body, self._center_poly.body, 0
        )
        motor.collide_bodies = True
        motor.max_force = 3000
        self._left_joint = Joint(joint, motor)
        self._left_poly = polygon

    def move_left_poly(self, direction: str) -> None:
        """Moves the left polygon

        Movement is done by changing the spinning rate of the left motor
        """
        if direction == 'up':
            self._left_joint.motor.rate = 10000.0
        if direction == 'down':
            self._left_joint.motor.rate = -10000.0
        if direction == 'freeze':
            self._left_joint.motor.rate = 0.

    def move_right_poly(self, direction) -> None:
        """Moves the right polygon

        Movement is done by changing the spinning rate of the right motor
        """
        if direction == 'up':
            self._right_joint.motor.rate = -10000.0
        if direction == 'down':
            self._right_joint.motor.rate = 10000.0
        if direction == 'freeze':
            self._right_joint.motor.rate = 0.

    @property
    def center_poly(self) -> Polygon:
        return self._center_poly

    @property
    def left_poly(self) -> Polygon:
        return self._left_poly

    @property
    def right_poly(self) -> Polygon:
        return self._right_poly

    @property
    def left_joint(self) -> Joint:
        return self._left_joint

    @property
    def right_joint(self) -> Joint:
        return self._right_joint


class Universe:
    def __init__(self, figure: Figure):
        self._space = pymunk.Space()
        self._add_walls()
        self._add_obstacle()
        self._score = 0.0
        self._figure = None
        self.add_figure(figure)
        self._finish_position = 940
        self._space.gravity = (0, -100)

    def _add_walls(self) -> None:
        static_lines = [
            pymunk.Segment(self._space.static_body, Vec2d(60, 50), Vec2d(940, 50), 2),
            pymunk.Segment(self._space.static_body, Vec2d(60, 50), Vec2d(60, 300), 2),
            pymunk.Segment(self._space.static_body, Vec2d(940, 50), Vec2d(940, 300), 2),
            pymunk.Segment(self._space.static_body, Vec2d(60, 300), Vec2d(940, 300), 2)
        ]
        static_lines[0].friction = 100000.0
        self.space.add(static_lines)

    def _add_obstacle(self, radius: int = 20) -> None:
        circle_moment = pymunk.moment_for_circle(1.0, 0, radius)
        circle_body = pymunk.Body(1.0, circle_moment)
        circle_body.body_type = pymunk.Body.KINEMATIC
        circle_shape = pymunk.Circle(circle_body, radius)
        circle_shape.filter = pymunk.ShapeFilter(mask=pymunk.ShapeFilter.ALL_MASKS ^ 1)
        circle_body.position = 930, 70
        circle_body.angular_velocity = 0.5
        circle_body.velocity = (-100, 0)

        self._space.add(circle_body, circle_shape)
        self._obstacle = circle_body
        self._obstacle_shape = circle_shape

    def add_figure(self, figure: Figure) -> None:
        center_poly = figure.center_poly
        right_poly = figure.right_poly
        left_poly = figure.left_poly
        left_joint = figure.left_joint
        right_joint = figure.right_joint

        self._figure = figure
        self._space.add(
            center_poly.body, center_poly.shape,
            left_poly.body, left_poly.shape,
            right_poly.body, right_poly.shape,
            left_joint.joint, left_joint.motor,
            right_joint.joint, right_joint.motor
        )

    def move_left_poly(self, direction) -> None:
        """Moves left polygon up/down"""
        self._figure.move_left_poly(direction)

    def move_right_poly(self, direction: str) -> None:
        """Moves right polygon up/down"""
        self._figure.move_right_poly(direction)

    def calculate_distance(self) -> float:
        """Calculates the distance between the ball and
        the figure (center polygon) at the current time step"""
        figure_position_x = self._figure.center_poly.centroid[0]
        distance = self._finish_position - figure_position_x
        self._score += distance

    def calculate_overlap(self) -> None:
        """ Calculates overlap at the current time step """
        overlap = 0.0
        obstacle_bb = self._obstacle_shape.bb
        center_poly_bb = self._figure.center_poly.shape.bb
        right_poly_bb = self._figure.left_poly.shape.bb
        left_poly_bb = self._figure.right_poly.shape.bb
        if obstacle_bb.intersects(center_poly_bb):
            dx = max(center_poly_bb.left, obstacle_bb.left) - min(center_poly_bb.top, obstacle_bb.top)
            overlap += dx
        if obstacle_bb.intersects(left_poly_bb):
            dx = max(left_poly_bb.left, obstacle_bb.left) - min(left_poly_bb.top, obstacle_bb.top)
            overlap += dx
        if obstacle_bb.intersects(right_poly_bb):
            dx = max(right_poly_bb.left, obstacle_bb.left) - min(right_poly_bb.top, obstacle_bb.top)
            overlap += dx

        self._score += overlap

    @property
    def space(self) -> float:
        return self._space

    @property
    def figure(self) -> Figure:
        return self._figure

    @property
    def score(self) -> Figure:
        return self._score
