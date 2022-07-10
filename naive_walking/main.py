from universe import Figure
from simulation import Simulation, Display
from ga import GeneticAlgorithm

# Pymunk simulation
# runtime for a single simulation in seconds (e.g. 15 seconds)
# one move per second results in a list of 20 actions
sim_runtime = 18
moves_per_second = 3

# Creating the figure out of 3 polygons
fig = Figure()

# Parameters for genetic algorithm
population_size = 100  # change this 👈
num_generations = 50  # change this 👈
elitism_size = 0.1  # percentage of best individuals that will be used in the next generation
crossover_size = 0.6  # percentage of individuals that will be created using mutation (crossover)
crossover_rate = 0.5  # probability of elite feature to be kept in genome

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
