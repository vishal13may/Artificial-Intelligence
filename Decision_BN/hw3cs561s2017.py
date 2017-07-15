from copy import deepcopy
import itertools
from decimal import Decimal



CPT = {}


all_queries = []
all_parents = {}
all_variables = []
decision_nodes = []
utility_parents = []
utility_values = {}
domain_values = [True, False]
cache = {}
all_result = []





def get_cache_key(variable, rest, explored):

    parent_sub_key = ()
    for parent in all_parents[variable]:
        parent_sub_key += ((parent, explored[parent],),)
    sub_key = ()
    parents = set()
    for variable in rest:
        for parent in all_parents[variable]:
            parents.add(parent)

    parents = sorted(list(parents))

    for parent in parents:
        if parent in explored:
            sub_key += ((parent, explored[parent],),)
    key = (variable, parent_sub_key, sub_key)
    return key

def process_queries():
    global all_queries, all_result

    all_result = []
    for query in all_queries:
        if query["type"] == "P":
            p_result = calculate_probability(query)
            p_result_quantized = str(Decimal(str(p_result)).quantize(Decimal("0.01")))
            all_result.append(p_result_quantized)
        elif query['type'] == "EU":
            eu_result = calculate_expected_utility(query)
            all_result.append(str(int(round(eu_result))))
        elif query['type'] == "MEU":
            meu_result, meu_key = calculate_max_expected_utility(query)
            result_formatted = ""
            for value in meu_key:
                if value:
                    result_formatted += "+ "
                else:
                    result_formatted += "- "
            result_formatted += str(int(round(meu_result)))
            all_result.append(result_formatted)

def get_cpt_probability(variable, value, explored):
    global decision_nodes, CPT

    if variable in decision_nodes:
        return 1.0
    cpt_key = ()
    for parent in all_parents[variable]:
        cpt_key += (explored[parent],)

    if value:
        return CPT[variable][cpt_key]
    else:
        return 1 - CPT[variable][cpt_key]


def get_ancestors(query_variables):

    variables = []
    parents = set()
    while len(query_variables) > 0:
        variable = query_variables[0]
        del query_variables[0]
        parents.add(variable)
        for val in all_parents[variable]:
            if len(all_parents[val]) > 0:
                query_variables.append(val)
            parents.add(val)

    for variable in all_variables:
        if variable in parents:
            variables.append(variable)

    return variables

def enumeration_ask(query, query_value, explored):
    global cache
    cache = {}

    query_variables = [query]
    query_variables.extend(explored.iterkeys())
    variables = get_ancestors(query_variables)
    return enumerate_all(variables, extend_dict(explored, query, query_value))


def enumerate_all(variables, explored):
    if not variables:
        return 1.0

    first = variables[0]
    rest = variables[1:]

    key = get_cache_key(first, rest, explored)
    if key in cache:
        return cache[key]

    if first in explored:
        probability = get_cpt_probability(first, explored[first], explored)
        if probability == 0.0:
            return 0.0
        return probability * enumerate_all(rest, explored)
    else:
        result = 0
        for value in domain_values:
            probability = get_cpt_probability(first,value, explored)
            sub_result = enumerate_all(rest, extend_dict(explored, first, value))
            result += probability * sub_result

        cache[get_cache_key(first, rest, explored)] = result
        return result

def calculate_probability(query):
    if 'evidence' not in query:
        find = query['to_find']
        first = find[0][0]
        first_value = find[0][1]
        evidence = {}
        for variable in xrange(1, len(find)):
            evidence[find[variable][0]] = find[variable][1]
        return enumeration_ask(first,first_value, evidence)
    else:
        find = query['to_find']
        evidence = {}
        for variable in xrange(1, len(find)):
            evidence[find[variable][0]] = find[variable][1]
        for variable in xrange(len(query['evidence'])):
            evidence[query['evidence'][variable][0]] = query['evidence'][variable][1]
        numerator = enumeration_ask(find[0][0],find[0][1], evidence)

        e = query['evidence']
        evidence = {}
        for variable in xrange(1, len(e)):
            evidence[e[variable][0]] = e[variable][1]
        denominator = enumeration_ask(e[0][0],e[0][1], evidence)

        return numerator / denominator

def calculate_expected_utility(query):
    global domain_values, utility_parents, utility_values

    utility = 0.0
    utility_query = {'to_find': [], 'evidence': query['to_find']}
    parent_value_mapping = {}
    if 'evidence' in query:
        for evidence in query['evidence']:
            utility_query['evidence'].append(evidence)

    for parent in utility_parents:
        parent_found_flag = False
        for variable in utility_query['evidence']:
            if variable[0] == parent:
                parent_found_flag = True
                parent_value_mapping[parent] = variable[1]
                break
        if not parent_found_flag:
            utility_query['to_find'].append([parent, None])

    if len(utility_query['to_find']) > 0:
        for value in itertools.product(domain_values, repeat=len(utility_query['to_find'])):
            for literal_index in range(len(utility_query['to_find'])):
                utility_query['to_find'][literal_index][1] = value[literal_index]
            utility_cpt_key = ()
            permutation_index = 0
            for parent in utility_parents:
                if parent not in parent_value_mapping:
                    utility_cpt_key += (value[permutation_index],)
                    permutation_index += 1
                else:
                    utility_cpt_key += (parent_value_mapping[parent],)

            utility = utility + utility_values[utility_cpt_key] * calculate_probability(utility_query)

        return utility
    else:
        utility_cpt_key = ()
        for parent in utility_parents:
            for evidence_variable in utility_query['evidence']:
                if evidence_variable[0] == parent:
                    utility_query['to_find'].append([evidence_variable[0], evidence_variable[1]])
                    utility_cpt_key += (evidence_variable[1],)

        utility = utility_values[utility_cpt_key]
        return utility

def calculate_max_expected_utility(query):
    key_value_count = 0
    original_find = deepcopy(query['to_find'])
    result = {}

    delete_index = []
    for variable_index in range(len(query['to_find'])):
        if query['to_find'][variable_index][1] is None:
            key_value_count += 1
        else:
            result[query['to_find'][variable_index][0]] = variable_index
            delete_index.append(variable_index)

    if len(delete_index) > 0:
        if 'evidence' not in query:
            query['evidence'] = []
        delete_index = list(reversed(delete_index))

        for index in delete_index:
            query['evidence'].append(query['to_find'][index])
            del query['to_find'][index]

    max_utility = 0
    max_utility_key = ()

    for value in itertools.product(domain_values, repeat=key_value_count):
        for literal_index in range(len(query['to_find'])):
            query['to_find'][literal_index][1] = value[literal_index]
        expected_utility = calculate_expected_utility(deepcopy(query))
        if expected_utility > max_utility:
            max_utility = expected_utility
            max_utility_key = ()
            literal_index = 0

            for variable_value in original_find:
                if variable_value[1] is None:
                    max_utility_key += (value[literal_index],)
                    literal_index += 1
                else:
                    max_utility_key += (variable_value[1],)
    return max_utility, max_utility_key


def extend_dict(dictionary, key, value):
    new_dictionary = dictionary.copy()
    new_dictionary[key] = value
    return new_dictionary


def get_formatted_query(query_line):

    query_split = query_line.split("|")
    to_find = query_split[0].split(",")
    formatted_query = {'to_find': []}
    for single_find in to_find:
        to_find_variable_value = single_find.split("=")
        if len(to_find_variable_value) == 2:
            if to_find_variable_value[1] == "+":
                to_find_variable_value[1] = True
            else:
                to_find_variable_value[1] = False
        else:
            to_find_variable_value.append(None)

        formatted_query['to_find'].append(to_find_variable_value)

    if len(query_split) == 2:
        evidences = query_split[1].split(",")
        formatted_query['evidence'] = []
        for single_evidence in evidences:
            evidence = single_evidence.split("=")
            if evidence[1] == "+":
                evidence[1] = True
            else:
                evidence[1] = False
            formatted_query['evidence'].append(evidence)

    return formatted_query

def create_baysian_network(input_lines):
    #Process the input and generate the Baysin Network

    global all_variables, all_queries, CPT, decision_nodes, utility_parents, utility_values

    counter = 0
    star_counter = 0
    while counter < len(input_lines):
        if input_lines[counter] != "******" and star_counter == 0:
            line_split = input_lines[counter].split()
            line = "".join(line_split)
            if line.startswith("P"):
                query = get_formatted_query(line[2:-1])
                query['type'] = "P"
            elif line.startswith("EU"):
                query = get_formatted_query(line[3:-1])
                query['type'] = "EU"
            elif line.startswith("MEU"):
                query = get_formatted_query(line[4:-1])
                query['type'] = "MEU"

            all_queries.append(query)
            counter += 1

        elif input_lines[counter] != "******" and star_counter == 1:
            child_parent = input_lines[counter].split("|")
            child = child_parent[0].strip()
            all_variables.append(child)
            parents = []
            if len(child_parent) == 2:
                parents = child_parent[1].strip()
                parents = parents.split(" ")
            all_parents[child] = parents

            counter += 1
            cpt = {}

            while "***" not in input_lines[counter]:
                if input_lines[counter] == "decision":
                    decision_nodes.append(child)
                    counter += 1
                    continue
                table_line = input_lines[counter].split(" ")
                cpt_key = ()
                for sign in range(1, len(table_line)):
                    if table_line[sign] == "+":
                        cpt_key += (True,)
                    else:
                        cpt_key += (False,)
                cpt[cpt_key] = float(table_line[0])

                counter += 1
                if counter == len(input_lines):
                    CPT[child] = cpt
                    return
            CPT[child] = cpt

            if input_lines[counter] == "***":
                counter += 1

        elif input_lines[counter] == "******" :
            star_counter += 1
            counter += 1

        elif input_lines[counter] != "******" and star_counter == 2:
            utility_parents = input_lines[counter].split("|")[1].strip().split(" ")
            counter += 1

            while counter < len(input_lines):
                utility_line = input_lines[counter].split(" ")
                utility_key = ()
                for sign in range(1, len(utility_line)):
                    if utility_line[sign] == "+":
                        utility_key += (True,)
                    else:
                        utility_key += (False,)
                utility_values[utility_key] = float(utility_line[0])
                counter += 1


# Read Input
input_lines = []
with open("input.txt", "r") as read_handler:
    input_lines = read_handler.readlines()
input_lines = [line.strip() for line in input_lines]
create_baysian_network(input_lines)
process_queries()
with open("output.txt", "w") as write_handler:
    for i in range(len(all_result) - 1):
        write_handler.write(all_result[i] + "\n")
    write_handler.write(all_result[len(all_result) - 1])
