def get_possible_four_number_combinations():
    combinations = set()
    for i in range(10):
        for j in range(10):
            for k in range(10):
                for l in range(10):
                    combinations.add(tuple(sorted((i, j, k, l))))
    return combinations

def get_possible_number_combinations(maximum=10, count=4):
    if count == 0:
        return {tuple()}
    combinations = set()
    for combination in get_possible_number_combinations(maximum=maximum, count=count - 1):
        for i in range(maximum):
            combinations.add(tuple(sorted(combination + (i,))))
    return combinations

OPS = set('*/+-')

def _insert_operations(eqn, ops=OPS):
    if len(eqn) == 1:
        return [eqn]
    results = []
    for op in ops:
        for combo in _insert_operations(eqn[1:], ops):
            results.append([eqn[0], op] + combo)
    return results

def _insert_parentheses(eqn, parens=True):
    if not parens:
        return [eqn]
    eqn = list(map(str, eqn))
    equations = []

    options = []
    for start in range(0, len(eqn), 2):
        for middle in range(3, len(eqn) + 1, 2):
            if middle - start > 2:
                options.append(eqn[:start] + ['('] + eqn[start:middle] + [')'] + eqn[middle:])

    for option in options:
        try:
            if eval(''.join(option)) != eval(''.join(eqn)):
                equations.append(option)
        except:
            pass
    return equations

def get_possible_equations(numbers, parens=True):
    equations = []
    for expr in _insert_operations(list(numbers)):
        for eqn in _insert_parentheses(list(expr), parens=parens):
            equations.append(''.join(map(str, eqn)))
    return equations

def is_equation_equal_to_ten(equation):
    try:
        return eval(equation) == 10
    except:
        pass
    return False

def get_valid_equations(maximum=10, count=4, parens=True):
    equations = []
    combinations = get_possible_number_combinations(maximum=maximum, count=count)
    for combination in combinations:
        for equation in get_possible_equations(combination, parens=parens):
            if is_equation_equal_to_ten(equation):
                equations.append(equation)
    print(f"Possible {count}-number combinations: {len(combinations)}")
    print(f"Possible equations: {len(equations)}")
    return equations

import string

def get_numbers_from_equations(equation):
    return tuple(item for item in equation if item in string.digits)

def get_valid_levels(maximum=10, count=4):
    remaining = set()
    for equation in get_valid_equations(maximum=maximum, count=count):
        remaining.add(get_numbers_from_equations(equation))
    print(f"Possible {count}-number sets: {len(remaining)}")
    return remaining

def get_operations_from_equations(equation):
    return tuple(sorted(item for item in equation if item in OPS))


def get_valid_levels(maximum=10, count=4, parens=True):
    remaining = set()
    for equation in get_valid_equations(maximum=maximum, count=count, parens=parens):
        remaining.add(get_numbers_from_equations(equation) + get_operations_from_equations(equation))
    print(f"Possible sets of numbers and operations: {len(remaining)}")
    return remaining

import time
for count in range(4, 7):
    start = time.time()
    get_valid_levels(maximum=10, count=count, parens=False)
    print(f"Time to complete {count}-number: {time.time() - start}")


# # those with only one occurrence
# from collections import defaultdict
# mapping = defaultdict(list)
# for eqn in filtered:
#     mapping[(eqn[0], eqn[2], eqn[4], eqn[6])].append(eqn)

# counts = defaultdict(int)
# for key, values in mapping.items():
#     counts[len(values)] += 1
# print(counts)

# final = []
# for key, values in mapping.items():
#     if len(values) == 1:
#         final.append(values[0])
# print(len(final))