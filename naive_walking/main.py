from universe import Figure
from simulation import Simulation, Display
from ga import GeneticAlgorithm

# TODO: solve gravity. Our figure can easily jump but does not move left/right (it can only spin around)
# TODO: I still don't know how to do that in Pymunk... 🥵
# Trying to change: 1) universe.py Universe class -> set space gravity
# Figure consists of 3 polygons, each has center of gravity 0, 0 by default (center of the body)

# Pymunk simulation
# runtime for a single simulation in seconds (e.g. 20 seconds)
# one move per second results in a list of 20 actions
sim_runtime = 20
moves_per_second = 4

# Creating the figure out of 3 polygons
fig = Figure()

# Parameters for genetic algorithm
population_size = 50  # change this 👈
num_generations = 20  # change this 👈
crossover_rate = 0.5
elitism_size = 0.1
crossover_size = 0.8

# Running Genetic algorithm with our figure
print('---Running GA for {} generations---'.format(num_generations))

ga = GeneticAlgorithm(figure=fig,
                      population_size=population_size,
                      num_generations=num_generations,
                      simulation_runtime=sim_runtime,
                      crossover_rate=crossover_rate,
                      elitism_size=elitism_size,
                      moves_per_second=moves_per_second,
                      )
ga.run()
best_actions = ga.best_individual.actions

# Displaying simulation with best individual calculated by GA
label = 'Generation ' + str(num_generations)
d = Display(best_actions, fig, label, sim_runtime)

print('----Displaying best individual----')
start_display = input("Enter 'S' to display: ")
if start_display.lower() == 's':
    d.display_simulation()
print('Score: {}'.format(int(d.get_score())))
