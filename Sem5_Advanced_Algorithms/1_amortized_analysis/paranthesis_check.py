import time

push_times = []
pop_times = []

def check_paranthesis(expression: str):
    brackets = []
    paranthesis_mapper = {
        ")": "(",
        "}": "{",
        "]": "[",
    }
    for char in expression:
        if char in paranthesis_mapper.values():
            t1 = time.time()
            brackets.append(char)
            t2 = time.time()
            push_times.append(t2-t1)
        elif char in paranthesis_mapper.keys():
            if not brackets[-1] == paranthesis_mapper[char]:
                return False
            else:
                t1 = time.time()
                brackets.pop()
                t2 = time.time()
                pop_times.append(t2-t1)
    if len(brackets) == 0: return True
    return False

if __name__ == "__main__":
    for i in range(100000):
        for exp in [
            "()[]{}",
            "([{}])",
            "([)]",
            "{[()]",
            "",
        ]:
            somthing = check_paranthesis(exp)

    print(f"len of push time = {len(push_times)}")
    print(f"len of pop time  = {len(pop_times)}")
    print("="*40)
    print(f"sum of push time = {sum(push_times)}")
    print(f"sum of pop time  = {sum(pop_times)}")
    print("="*40)
    print(f"avg of push time = {sum(push_times)/len(push_times)}")
    print(f"avg of pop time  = {sum(pop_times)/len(pop_times)}")


