# -*- coding: utf-8 -*-

import random
import itertools
from copter import *
from deap import creator, base, tools, algorithms


def generate_codons(aa_seq,
                    creator):
    codons = [amino_to_codon(amino) for amino in aa_seq]
    return creator.Individual(codons)


def mutate_codon(individual,
                 indpb=0.05):
    for i in range(0, len(individual)):
        codon = individual[i]
        if random.random() < indpb:
            individual[i] = codon_to_codon(codon)
    return individual, # mutation func should return tuple


def crossover_synonyms_codon(individual,
                             indpb=0.05):
    crossover_position_table = {}
    for i in range(0, len(individual)):
        codon = individual[i]
        amino = codon_to_amino(codon)
        if amino not in crossover_position_table:
            crossover_position_table[amino] = []
        crossover_position_table[amino].append(i)

    crossed_positions = []
    for amino in crossover_position_table:
        swap_possible_positions = crossover_position_table[amino]
        unique_swap_possible_positions = set(swap_possible_positions)
        # if only 1 codon synonyms is available, then skip this amino series
        if len(swap_possible_positions) < 2:
            continue
        if random.random() < indpb:
            swap_posA, swap_posB = random.sample(unique_swap_possible_positions, 2)
            # 一度crossoverされた箇所はスキップ
            if swap_posA in crossed_positions or swap_posB in crossed_positions:
                continue
            codonA = individual[swap_posA]
            codonB = individual[swap_posB]
            individual[swap_posA] = codonB
            individual[swap_posB] = codonA
            crossed_positions.extend([swap_posA, swap_posB])
    return individual,


def initWithSpecificIndividual(initial_na_seq, n):
    initial_codons = [''.join(codon_tpl) for codon_tpl in itertools.zip_longest(*[iter(initial_na_seq)]*3)]
    return [creator.Individual(initial_codons) for i in range(0, n)]


def validate(individual,
             ng_sequences=[],
             validation_func=None):
    ng_sequences = [ng_seq.strip() for ng_seq in ng_sequences if ng_seq.strip() != '']
    is_valid = True
    if ng_sequences is not None and len(ng_sequences) != 0:
        is_valid = not has_ng_sequences(individual, ng_sequences)
    if validation_func is not None:
        is_valid = validation_func(individual)
    return is_valid


def generate_population(toolbox,
                        population_size,
                        initial_na_seq=None,
                        ng_sequences=[],
                        validation_func=None):
    # とりあえず100回くらいPopulationの生成を試み、駄目なら諦める
    for i in range(0, 100):
        if initial_na_seq is None:
            population = toolbox.population(n=population_size)
        else:
            population = toolbox.initial_population(n=population_size)
        population = [ind for ind in population if validate(ind,
                                                            ng_sequences=ng_sequences,
                                                            validation_func=validation_func)]
        if len(population) > 0:
            return population
    return []

def optimize(aa_seq,
             eval_func,
             weights,
             initial_na_seq=None,
             validation_func=None,
             generation_size=100,
             population_size=100,
             indpb=0.05,
             surviver_amount=1,
             mutation_func=mutate_codon,
             ng_sequences=[]):
    toolbox = setup_toolbox(aa_seq,
                            weights,
                            initial_na_seq=initial_na_seq,
                            surviver_amount=surviver_amount,
                            population_size=population_size,
                            indpb=indpb,
                            mutation_func=mutation_func)
    population = generate_population(toolbox,
                                     population_size,
                                     initial_na_seq=initial_na_seq,
                                     ng_sequences=ng_sequences,
                                     validation_func=validation_func)
    if len(population) == 0:
        return []
    survivers = tools.selBest(population, k=surviver_amount)

    for gen in range(generation_size):
        new_population, survivers = evolve(population,
                                           survivers,
                                           eval_func,
                                           toolbox,
                                           population_size=population_size,
                                           surviver_amount=surviver_amount,
                                           ng_sequences=ng_sequences)
        if len(new_population) > 0:
            population = new_population
    surviver_genes = [''.join(codons) for codons in survivers]
    if validation_func is not None:
        surviver_genes = [gene for gene in surviver_genes if validation_func(gene)]
    return surviver_genes


def setup_toolbox(aa_seq,
                  weights,
                  initial_na_seq=None,
                  surviver_amount=1,
                  population_size=100,
                  indpb=0.05,
                  mutation_func=mutate_codon):
    if surviver_amount > population_size:
        raise Exception('surviver_amount should be lower than population_size')

    creator.create("FitnessMax", base.Fitness, weights=weights)
    creator.create("Individual", list, fitness=creator.FitnessMax)

    toolbox = base.Toolbox()
    toolbox.register("individual", generate_codons, aa_seq, creator)
    toolbox.register("mutate", mutation_func, indpb=indpb)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("initial_population", initWithSpecificIndividual, initial_na_seq)
    return toolbox


def evolve(population,
           survivers,
           eval_func,
           toolbox,
           surviver_amount=1,
           population_size=1,
           ng_sequences=[]):
    dead_count = population_size - len(population)
    amplified_population = population + [creator.Individual(random.sample(population, 1)[0]) for i in range(0, dead_count)]

    # no cross over, 100% mutation(except for survivers)
    offspring = algorithms.varAnd(amplified_population, toolbox, cxpb=0.0, mutpb=1.0)
    offspring = offspring + survivers

    # remove genes that have ng_sequences
    if ng_sequences is not None and len(ng_sequences) != 0:
        offspring = [ind for ind in offspring if validate(ind, ng_sequences)]

    fits = toolbox.map(eval_func, offspring)
    for fit, ind in zip(fits, offspring):
        ind.fitness.values = fit
    survivers = tools.selBest(offspring, k=surviver_amount)
    new_population = tools.selBest(offspring, k=population_size)

    return new_population, survivers
