import random
from collections import Counter

POPULATION_SIZE = 4
CHROMOSOME_LENGTH = 5
NUM_GENERATIONS = 10


def binary_to_int(binary_str):
    return int(binary_str, 2)


def fitness_function(x):
    return x**2


def roulette_wheel_selection(population, fitness_values):
    total_fitness = sum(fitness_values)
    if total_fitness == 0:
        return random.choices(population, k=POPULATION_SIZE)

    cumulative_probs = [
        sum(fitness_values[: i + 1]) / total_fitness for i in range(len(fitness_values))
    ]

    mating_pool = []
    for _ in range(POPULATION_SIZE):
        r = random.random()
        for i, prob in enumerate(cumulative_probs):
            if r <= prob:
                mating_pool.append(population[i])
                break
    return mating_pool


def crossover(parent1, parent2):
    point = random.randint(1, CHROMOSOME_LENGTH - 1)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return child1, child2, point


def mutate(chromosome):
    PM = 1 / CHROMOSOME_LENGTH
    mutated = ""
    for bit in chromosome:
        if random.random() < PM:
            mutated += "1" if bit == "0" else "0"
        else:
            mutated += bit
    return mutated


def run_ga_and_display_final_iteration():

    current_population = ["01101", "11000", "01000", "10011"]

    print("1. Initial Population and Roulette Wheel Selection Table")

    x_values = [binary_to_int(ind) for ind in current_population]
    fitness_values = [fitness_function(x) for x in x_values]
    total_fitness = sum(fitness_values) if sum(fitness_values) > 0 else 1
    avg_fitness = total_fitness / POPULATION_SIZE

    probabilities = [f / total_fitness for f in fitness_values]
    expected_counts = [f / avg_fitness for f in fitness_values]

    mating_pool = roulette_wheel_selection(current_population, fitness_values)
    actual_counts = Counter(mating_pool)

    header = (
        f"{'String no.':<12} | {'Initial Pop':<15} | {'x Value':<10} | "
        f"{'Fitness (x^2)':<15} | {'Probability':<12} | {'Expected Count':<16} | {'Actual Count':<12}"
    )
    print(header)
    print("-" * len(header))

    for i in range(POPULATION_SIZE):
        print(
            f"{i+1:<12} | {current_population[i]:<15} | {x_values[i]:<10} | "
            f"{fitness_values[i]:<15} | {probabilities[i]:<12.4f} | "
            f"{expected_counts[i]:<16.4f} | {actual_counts[current_population[i]]:<12}"
        )

    for gen in range(NUM_GENERATIONS):

        fitness_values = [
            fitness_function(binary_to_int(ind)) for ind in current_population
        ]
        mating_pool = roulette_wheel_selection(current_population, fitness_values)
        random.shuffle(mating_pool)

        offspring_after_crossover = []
        crossover_details = []

        for i in range(0, POPULATION_SIZE, 2):
            parent1, parent2 = mating_pool[i], mating_pool[i + 1]
            child1, child2, point = crossover(parent1, parent2)

            offspring_after_crossover.extend([child1, child2])
            crossover_details.append(
                {
                    "parent1": parent1,
                    "parent2": parent2,
                    "child1": child1,
                    "child2": child2,
                    "point": point,
                }
            )

        offspring_after_mutation = [
            mutate(child) for child in offspring_after_crossover
        ]

        if gen == NUM_GENERATIONS - 1:

            print(f"\n2. Crossover Table (Final Iteration: {gen + 1})")
            crossover_header = (
                f"{'String no.':<12} | {'Mating Pool':<15} | {'Crossover Pt.':<15} | "
                f"{'Offspring after X':<20} | {'x Value':<10} | {'Fitness (x^2)':<15}"
            )
            print(crossover_header)
            print("-" * len(crossover_header))

            idx = 1
            for d in crossover_details:
                x1 = binary_to_int(d["child1"])
                f1 = fitness_function(x1)
                print(
                    f"{idx:<12} | {d['parent1']:<15} | {d['point']:<15} | "
                    f"{d['child1']:<20} | {x1:<10} | {f1:<15}"
                )
                idx += 1

                x2 = binary_to_int(d["child2"])
                f2 = fitness_function(x2)
                print(
                    f"{idx:<12} | {d['parent2']:<15} | {d['point']:<15} | "
                    f"{d['child2']:<20} | {x2:<10} | {f2:<15}"
                )
                idx += 1

            print(f"\n3. Mutation Table (Final Iteration: {gen + 1})")
            mutation_header = (
                f"{'String no.':<12} | {'After Crossover':<18} | {'After Mutation':<18} | "
                f"{'x Value':<10} | {'Fitness (x^2)':<15}"
            )
            print(mutation_header)
            print("-" * len(mutation_header))

            for i in range(POPULATION_SIZE):
                x_val = binary_to_int(offspring_after_mutation[i])
                fit = fitness_function(x_val)
                print(
                    f"{i+1:<12} | {offspring_after_crossover[i]:<18} | "
                    f"{offspring_after_mutation[i]:<18} | {x_val:<10} | {fit:<15}"
                )

        current_population = offspring_after_mutation


if __name__ == "__main__":
    run_ga_and_display_final_iteration()
