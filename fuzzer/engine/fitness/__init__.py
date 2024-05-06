#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math

def fitness_function(indv, env):
    return compute_code_distance(indv, env)
    """
    block_coverage_fitness = compute_branch_coverage_fitness(env.individual_branches[indv.hash], env.code_coverage)
    if env.args.data_dependency:
        data_dependency_fitness = compute_data_dependency_fitness(indv, env.data_dependencies)
        return block_coverage_fitness + data_dependency_fitness
    return block_coverage_fitness
    """

def compute_branch_coverage_fitness(branches, pcs):
    non_visited_branches = 0.0

    for jumpi in branches:
        for destination in branches[jumpi]:
            if not branches[jumpi][destination] and destination not in pcs:
                non_visited_branches += 1

    return non_visited_branches

def compute_data_dependency_fitness(indv, data_dependencies):
    data_dependency_fitness = 0.0
    all_reads = set()

    for d in data_dependencies:
        all_reads.update(data_dependencies[d]["read"])

    for i in indv.chromosome:
        _function_hash = i["arguments"][0]
        if _function_hash in data_dependencies:
            for i in data_dependencies[_function_hash]["write"]:
                if i in all_reads:
                    data_dependency_fitness += 1

    return data_dependency_fitness

def compute_code_coverage_fitness(indv, env):
    return float(len(env.individual_code_coverage[indv.hash]))

def compute_vulnerability_fitness(indv, env):
    return env.individual_vulnerabilities_detected[indv.hash]

def compute_branch_distance(indv, env):
    branch_distance = 0.0
    for jumpi_pc in env.visited_branches:
        if len(env.visited_branches[jumpi_pc]) == 2:
            continue
        elif 0 not in env.visited_branches[jumpi_pc] and jumpi_pc in env.individual_branch_distances[indv.hash] and 0 in env.individual_branch_distances[indv.hash][jumpi_pc]:
            branch_distance += env.individual_branch_distances[indv.hash][jumpi_pc][0]
        elif 1 not in env.visited_branches[jumpi_pc] and jumpi_pc in env.individual_branch_distances[indv.hash] and 1 in env.individual_branch_distances[indv.hash][jumpi_pc]:
            branch_distance += env.individual_branch_distances[indv.hash][jumpi_pc][1]
    return branch_distance

def compute_code_distance(indv, env):
    if len(env.code_coverage) == len(env.overall_pcs):
        return 0.0
    queue = list()
    visited = set()
    for vertice in env.cfg.vertices.values():
        for pc in env.cfg.visited_pcs:
            if vertice.start_address <= pc <= vertice.end_address:
                break
        else:
            queue.append([vertice, 0.0])
            visited.add(vertice.start_address)
    if len(queue) == 0:
        return 0.0
    while len(queue) > 0:
        node, dist = queue.pop()
        for pc in env.individual_code_coverage[indv.hash]:
            if node.start_address <= pc <= node.end_address:
                return dist
        neighbors = set()
        for vertice in env.cfg.edges:
            if node.start_address in env.cfg.edges[vertice]:
                neighbors.add(vertice)
        for neighbor in neighbors:
            for vertice in env.cfg.vertices.values():
                if vertice.end_address == neighbor:
                    if not vertice.start_address in visited:
                        queue.append([vertice, dist + 1])
                        visited.add(vertice.start_address)
                    break
    return math.inf