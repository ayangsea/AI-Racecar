import Const
from Car import Car
import random

def next_generation(generation, savedCars, screen, track):
    fitness(savedCars)
    for i in range(Const.NUM_CARS_PER_GENERATION):
        generation.append(pick_one(savedCars, screen, track))
    return generation

def pick_one(savedCars, screen, track):
    index = 0
    r = random.uniform(0, 1)

    while r > 0:
        r -= savedCars[index].fitness
        index += 1
    index -= 1
    
    car = savedCars[index]
    child = Car(screen, track, False, car.brain)
    child.brain.mutate(0.2)
    return child

def fitness(savedCars):
    total = 0
    total = sum(car.score for car in savedCars)
    
    if total == 0:
        return 0

    for car in savedCars:
        car.fitness = car.score / total
        


