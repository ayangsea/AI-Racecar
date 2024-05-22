import Const
from Car import Car
import random

def next_generation(generation, savedCars, screen, track):
    print("next generatio")
    fitness(savedCars)
    for i in range(Const.NUM_CARS_PER_GENERATION):
        generation.append(pick_one(savedCars, screen, track))
    print(len(generation))
    return generation

def pick_one(savedCars, screen, track):
    index = 0
    r = random.uniform(0, 1)

    while r > 0:
        r -= savedCars[index].fitness
        index += 1
    index -= 1
    
    car = savedCars[index]
    child = Car(Const.CAR_MAX_SPEED, Const.CAR_ROTATE_SPEED, Const.CAR_ACCEL, screen, track, False, car.brain)
    child.brain.mutate(0.1)
    return child

def fitness(savedCars):
    total = 0
    total = sum(car.score for car in savedCars)
    
    for car in savedCars:
        car.fitness = car.score / total
        


