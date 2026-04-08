import math

class DecisionTree:
    
    def __init__(self, data: list[dict], target_parameter: str):
        self.data = data
        self.target_parameter = target_parameter
    
    def predict(self, params: dict):

        data = self.data
        target = self.target_parameter

        def entropy(rows):
            counts = {}
            for r in rows:
                label = r[target]
                if label not in counts:
                    counts[label] = 0
                counts[label] += 1

            total = len(rows)
            ent = 0.0

            for label in counts:
                p = counts[label] / total
                if p > 0:
                    ent -= p * math.log2(p)

            return ent

        def information_gain(rows, attribute):
            total_entropy = entropy(rows)
            total = len(rows)

            groups = {}
            for r in rows:
                v = r[attribute]
                if v not in groups:
                    groups[v] = []
                groups[v].append(r)

            weighted_entropy = 0.0
            for v in groups:
                subset = groups[v]
                weighted_entropy += (len(subset) / total) * entropy(subset)

            return total_entropy - weighted_entropy

        def majority(rows):
            counts = {}
            for r in rows:
                label = r[target]
                if label not in counts:
                    counts[label] = 0
                counts[label] += 1

            best_label = None
            best_count = -1

            for label in counts:
                if counts[label] > best_count:
                    best_count = counts[label]
                    best_label = label

            return best_label

        def build(rows, attributes):
            first_label = rows[0][target]
            all_same = True

            for r in rows:
                if r[target] != first_label:
                    all_same = False
                    break

            if all_same:
                return first_label

            if len(attributes) == 0:
                return majority(rows)

            best_attr = None
            best_gain = -1

            for attr in attributes:
                gain = information_gain(rows, attr)
                if gain > best_gain:
                    best_gain = gain
                    best_attr = attr

            tree = {best_attr: {}}

            values = []
            for r in rows:
                v = r[best_attr]
                if v not in values:
                    values.append(v)

            for v in values:
                subset = []
                for r in rows:
                    if r[best_attr] == v:
                        subset.append(r)

                remaining = []
                for a in attributes:
                    if a != best_attr:
                        remaining.append(a)

                if len(subset) == 0:
                    tree[best_attr][v] = majority(rows)
                else:
                    tree[best_attr][v] = build(subset, remaining)

            return tree

        attributes = []
        for k in data[0]:
            if k != target:
                attributes.append(k)

        tree = build(data, attributes)

        node = tree
        while isinstance(node, dict):
            attr = list(node.keys())[0]
            value = params.get(attr)

            if value not in node[attr]:
                return majority(data)

            node = node[attr][value]

        return node
    
    def pretty_print(self) -> None:
        
        if self.data is None or len(self.data) == 0:
            print("no data to print")
            return
        
        param_values_max_len = {}
        params = []
        for entry in self.data:
            for key, value in entry.items():
                if key not in param_values_max_len.keys():
                    params.append(key)
                    param_values_max_len[key] = len(key)
                param_values_max_len[key] = max(param_values_max_len[key], len(value))
        
        # td
        print("|", end="")
        for param in params:
            num_spaces = " " * (param_values_max_len[param] - len(param))
            print(f" {param}{num_spaces} |", end="")
        print("")
        
        # separator
        print("|", end="")
        for param in params:
            num_spaces = "-" * (param_values_max_len[param])
            print(f" {num_spaces} |", end="")
        print("")
        
        # tr
        for entry in self.data:
            print("|", end="")
            for key, value in entry.items():
                num_spaces = " " * (param_values_max_len[key] - len(value))
                print(f" {value}{num_spaces} |", end="")
            print("")

data = [
    {
        "Age": "Youth",
        "Income": "High",
        "Student": "No",
        "Credit Rating": "Fair",     
        "Buys Computer": "No",
    }, {
        "Age": "Youth",
        "Income": "High",
        "Student": "No",
        "Credit Rating": "Excellent",
        "Buys Computer": "No",
    }, {
        "Age": "Middle-Aged",
        "Income": "High",
        "Student": "No",
        "Credit Rating": "Fair",
        "Buys Computer": "Yes",
    }, {
        "Age": "Senior",
        "Income": "Medium",
        "Student": "No",
        "Credit Rating": "Fair",
        "Buys Computer": "Yes",
    }, {
        "Age": "Senior",
        "Income": "Low",
        "Student": "Yes",
        "Credit Rating": "Fair",
        "Buys Computer": "Yes",
    }, {
        "Age": "Senior",
        "Income": "Low",
        "Student": "Yes",
        "Credit Rating": "Excellent",
        "Buys Computer": "No",
    }, {
        "Age": "Middle-Aged",
        "Income": "Low",
        "Student": "Yes",
        "Credit Rating": "Excellent",
        "Buys Computer": "Yes",
    }, {
        "Age": "Youth",
        "Income": "Medium",
        "Student": "No",
        "Credit Rating": "Fair",
        "Buys Computer": "No",
    }, {
        "Age": "Youth",
        "Income": "Low",
        "Student": "Yes",
        "Credit Rating": "Fair",
        "Buys Computer": "Yes",
    }, {
        "Age": "Senior",
        "Income": "High",
        "Student": "Yes",
        "Credit Rating": "Fair",
        "Buys Computer": "Yes",
    }, {
        "Age": "Youth",
        "Income": "Medium",
        "Student": "Yes",
        "Credit Rating": "Excellent",
        "Buys Computer": "Yes",
    }, {
        "Age": "Middle-Aged",
        "Income": "Medium",
        "Student": "No",
        "Credit Rating": "Excellent",
        "Buys Computer": "Yes",
    }, {
        "Age": "Middle-Aged",
        "Income": "High",
        "Student": "Yes",
        "Credit Rating": "Fair",
        "Buys Computer": "Yes",
    }, {
        "Age": "Senior",
        "Income": "Medium",
        "Student": "No",
        "Credit Rating": "Excellent",
        "Buys Computer": "No",
    }
]

to_predict = {
    "Age": "Youth",
    "Income": "Low",
    "Student": "No",
    "Credit Rating": "Fair",     
    "Buys Computer": "No",
} # No

def print_prediction(decision_tree: DecisionTree, to_predict: dict) -> None:
    print(f"to predict: (", end="")
    tuple_format = ""
    for key, value in to_predict.items():
        tuple_format += f"{key}={value}, "
    print(f"{tuple_format[:-2]})")
    print(f"prediction: {decision_tree.predict(to_predict)}")

def test_decision_tree(decision_tree: DecisionTree):

    param_values = {}
    for entry in decision_tree.data:
        for key, value in entry.items():
            if key == decision_tree.target_parameter:
                continue
            if key not in param_values:
                param_values[key] = []
            if value not in param_values[key]:
                param_values[key].append(value)

    keys = list(param_values.keys())

    def generate(index, current):
        if index == len(keys):
            print_prediction(decision_tree, current)
            return

        key = keys[index]
        for value in param_values[key]:
            next_params = current.copy()
            next_params[key] = value
            generate(index + 1, next_params)

    generate(0, {})

if __name__ == "__main__":
    decision_tree = DecisionTree(data, target_parameter="Buys Computer")
    
    print("")
    decision_tree.pretty_print()
    print("")
    # test_decision_tree(decision_tree)
    print_prediction(decision_tree, to_predict)
    print("")
