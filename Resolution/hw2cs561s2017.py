from copy import deepcopy

all_friends = []
all_enemies = []
all_clauses = []
GUEST_MULTIPLIER = 100


def generate_cnf_clauses():
    global guest_count, table_count

    for guest in range(1, guest_count + 1):
        clauses_first_rule = []
        for table in range(1, table_count + 1):
            clauses_first_rule.append((guest * GUEST_MULTIPLIER) + table)
        all_clauses.append(clauses_first_rule)

    for guest in range(1, guest_count + 1):
        for table_i in range(1, table_count + 1):
            for table_j in range(table_i + 1, table_count + 1):
                all_clauses.append([~((guest * GUEST_MULTIPLIER) + table_i), ~((guest * GUEST_MULTIPLIER) + table_j)])

    for friend in all_friends:
        for table in range(1, table_count + 1):
            all_clauses.append([~((friend[0] * GUEST_MULTIPLIER) + table), ((friend[1] * GUEST_MULTIPLIER) + table)])
            all_clauses.append([(friend[0] * GUEST_MULTIPLIER) + table, ~((friend[1] * GUEST_MULTIPLIER) + table)])

    for enemy in all_enemies:
        for table in range(1, table_count + 1):
            all_clauses.append([~((enemy[0] * GUEST_MULTIPLIER) + table), ~((enemy[1] * GUEST_MULTIPLIER) + table)])


def get_unique_symbols(clauses):
    unique_symbol_set = set()
    for i in clauses:
        for sym in i:
            unique_symbol_set.add(sym)
    return unique_symbol_set


def is_satisfiable(clause, model):
    false_count = 0
    for symbol in clause:
        if symbol in model:
            if model[symbol]:
                return True
            else:
                false_count += 1

    if false_count == len(clause):
        return False

    return None

def get_pure_symbols(clauses,symbols,model):
    new_symbols = set()
    for clause in clauses:
        sub_set = set()
        isTrue = False
        for symbol in clause:
            if symbol in model:
                if model[symbol]:
                    isTrue = True
                    break
            else :
                if symbol in symbols:
                    sub_set.add(symbol)
        if not isTrue:
          new_symbols = new_symbols.union(sub_set)

    positive_symobls = set()
    negative_symbols = set()
    for symbol in new_symbols:
        if ~symbol not in new_symbols:
            if symbol > 0:
                positive_symobls.add(symbol)
            else:
                negative_symbols.add(symbol)
    if len(positive_symobls) > 0:
        return positive_symobls
    if len(negative_symbols) > 0:
        return negative_symbols

    return False


def get_unit_clause(clauses,symbols,model):
    for clause in clauses:
        l = 0
        isTrue = False
        sym = None
        for symbol in clause:
            if symbol in model :
                if model[symbol]:
                    isTrue = True
                    break
            else :
                l += 1
                sym = symbol
        if l == 1 and isTrue == False:
            return sym

    return False


def dpll_algorithm(clauses, symbols, model):

    satisfiable = True
    for clause in clauses:
        satisfiable_check = is_satisfiable(clause,model)
        if satisfiable_check:
            continue
        elif satisfiable_check == False :
            return False,model
        else:
            satisfiable = False
            break
    if satisfiable:
        return True,model

    pure_symbols = get_pure_symbols(clauses,symbols,model)
    if pure_symbols:
        for p in pure_symbols:
            symbols.remove(p)
            model[p] = True
            model[~p] = False
            if ~p in symbols:
                symbols.remove(~p)
        return dpll_algorithm(clauses, symbols, model)

    unit_symbol = get_unit_clause(clauses,symbols,model)
    if unit_symbol:
        symbols.remove(unit_symbol)
        if ~unit_symbol in symbols:
            symbols.remove(~unit_symbol)
        model[unit_symbol] = True
        model[~unit_symbol] = False
        return dpll_algorithm(clauses, symbols, model)

    new_symbols = deepcopy(symbols)
    lst = list(new_symbols)
    p = lst.pop()
    rest = set(lst)
    rest1 = deepcopy(rest)
    if ~p in rest:
        rest.remove(~p)
    new_model_true = deepcopy(model)
    new_model_true[p] = True
    new_model_true[~p] = False
    p_true,new_model_true = dpll_algorithm(clauses, rest, new_model_true)
    if p_true:
        return True,new_model_true

    new_model_false = deepcopy(model)
    new_model_false[p] = False
    new_model_false[~p] = True
    if ~p in rest1:
        rest1.remove(~p)
    p_false,new_model_false = dpll_algorithm(clauses, rest1, new_model_false)
    if p_false:
        return True,new_model_false
    return False,None


lines = []
fh = open("input.txt", "r")
file_content = fh.readlines()
file_content_formatted = []
for line in file_content:
    file_content_formatted.append(line.strip())
guest_count, table_count = file_content_formatted[0].split(" ")
guest_count = int(guest_count)
table_count = int(table_count)
relationships = file_content_formatted[1:]
for relationship in relationships:
    relationship = relationship.split(" ")
    first = int(relationship[0])
    second = int(relationship[1])
    if relationship[2] == "F" or relationship[2] == "f":
        all_friends.append([first, second])
    elif relationship[2] == "E" or relationship[2] == "e":
        all_enemies.append([first, second])

generate_cnf_clauses()
symbols = get_unique_symbols(all_clauses)
model = {}
res,model = dpll_algorithm(all_clauses, symbols, model)
fh = open("output.txt", "w")
if res:
    keys = []
    for m in model:
        if m > 0 and model[m]:
            keys.append(m)
    fh.write("yes")
    keys = sorted(keys)
    for key in keys:
        guest = key / 100
        table = key % 100
        fh.write("\n" + str(guest) + " " + str(table))
else:
    fh.write("no")
fh.close()
