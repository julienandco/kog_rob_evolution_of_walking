# Walking evolution

1. Robot (figure): three-polygon shape with two motors and joints
2. Individual: a list of actions made by the figure during simulation (e.g. [1, 0, 4, 2, 4])
3. Actions: discrete value between 0 and 4 (left motor up/down, right motor up/down)
4. Genetic algorithm: find the best list of actions to reach the right wall
5. Mutation: uniform crossover between two lists of actions (elite individual and random individual)

Goal: figure starts on the left side of the universe (2D) and needs to walk to the right wall

### Requirements:
- Python >= 3.7
- Pyglet
- Pymunk 5.4.2 (pip install this exact version! newer versions won't work 👈)

### TODO:
- Solve gravity to make the figure move left/right. Now it is stuck in one place 🥵
