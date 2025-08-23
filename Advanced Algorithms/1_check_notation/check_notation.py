import os

allowed_files = ["py"]

# count the indentation of a given line
def count_indent(line: str):
    count = 0
    for char in line:
        if char == " ":
            count += 1
        elif char == "\t":
            count += 4
        else:
            return count

# count the nested for loops  starting at a given line_num
def count_num_fors(file_contents: list[str], line_num: int):
    num_fors = 1
    line = file_contents[line_num]
    main_for_indent = count_indent(line)

    i = line_num + 1
    while i < len(file_contents):
        indent = count_indent(file_contents[i])
        if indent <= main_for_indent:  # block ends here
            break
        if "for" in file_contents[i].strip().split() and indent > main_for_indent:
            # found a nested for, count its nested fors
            nested_count = count_num_fors(file_contents, i)
            num_fors = max(num_fors, 1 + nested_count)
        i += 1

    return num_fors

# return big O notation of a file
def check_notation_of_file(file_name: str):
    try:
        # check file extension
        dot_index = file_name.find(".")
        file_extension = file_name[dot_index+1:]
        if(file_extension not in allowed_files):
            return False, f"File not in {allowed_files}"
        
        # read file
        file_contents = []
        with open(file_name, "r") as file:
            file_contents = file.readlines()

        # find fors with 0 indentation
        fors_with_0_indent = []
        for line_num, line in enumerate(file_contents):
            if "for" in line and count_indent(line) == 0:
                fors_with_0_indent.append(line_num)

        # return for with max power
        max_power = -1
        for for_line in fors_with_0_indent:
            power = count_num_fors(file_contents, for_line)
            max_power = max(max_power, power)
        if max_power == -1:
            return True, "O(1)"
        return True, f"O(n^{max_power})"
        
    except Exception as e:
        return False, f"something went wrong: {str(e)}"

# print big O notation of a file
def print_notation(file_name: str):
    resp_ok, resp = check_notation_of_file(file_name)
    if resp_ok:
        print(f"{file_name}: {resp}")
    else:
        print(f"Error: {resp}")


if __name__ == "__main__":
    for file in ["n1.py", "n2.py", "n3.py"]:
        print_notation(file)