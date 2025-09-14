allowed_file_extensions = ["py"]

def get_time_complexity(file_name: str) -> tuple[bool, str]:
    """
    returns success_bool, (time_complexity_str or error_str)
    """
    
    # helper functions 👇

    def count_indent(line: str) -> int:
        """
        returns the indentation count of a given line
        """
        count = 0
        for char in line:
            if char == " ":     count += 1
            elif char == "\t":  count += 4
            else: break
        return count

    def get_formatted_tc(power: int, includes_log: bool) -> str:
        if power == 0 and not includes_log: return "O(1)"
        notation = "O("
        if power > 0:
            if power == 1: notation += "n"
            else: notation += f"n^{power}"
        if includes_log: 
            notation += "log(n)"
        notation += ")"
        return notation

    def is_loop(line: str, loop_type: str) -> bool:
        """
        returns True if line is a "loop_type" loop statement
        """
        stripped = line.strip()
        return stripped.startswith(f"{loop_type} ") and stripped.endswith(":")

    def get_while_loop_iterator(line: str) -> str:
        """
        returns iterator from while loop line
        """
        iterator = line[:]
        for i in [
            "while",
            ":",
            "=",
            ">",
            "<",
            "!",
            "range",
            "(",
            ")",
            " ",
        ]: iterator = iterator.replace(i, "")
        return iterator

    # main function 👇

    def analyze_code_block(
        lines: list[str],
        start_line: int = 0,
        base_indent: int = 0,
    ) -> tuple[int, bool, int]:
        """
        recursively analyzes a block of code
        returns power, includes_log, line_index
        (power = number of nested loops)
        """
        
        max_power = 0
        includes_log = False
        line_ind = start_line
        num_lines = len(lines)

        while line_ind < num_lines:
            line = lines[line_ind]
            indent = count_indent(line)
            stripped_line = line.strip()

            # end of code block, return to previous level
            if indent < base_indent:
                return max_power, includes_log, line_ind
            
            # skip empty lines and comments
            if not stripped_line or stripped_line.startswith('#'):
                line_ind += 1
                continue
            
            # for loop
            if is_loop(stripped_line, "for"):

                # find the expected indentation of loop body
                next_line_ind = line_ind + 1
                body_indent = base_indent + 4
                if next_line_ind < num_lines:
                    next_line = lines[next_line_ind]
                    if next_line.strip():
                        body_indent = count_indent(next_line)
                
                # recursively analyze for loop body
                new_power, new_includes_log, new_line_index = analyze_code_block(
                    lines, 
                    start_line=line_ind + 1, 
                    base_indent=body_indent
                )
                
                # update results
                max_power = max(max_power, 1 + new_power)
                includes_log = includes_log or new_includes_log
                line_ind = new_line_index
                continue
            
            # while loop
            if is_loop(stripped_line, "while"):

                # find the expected indentation of loop body
                next_line_ind = line_ind + 1
                body_indent = base_indent + 4
                if next_line_ind < num_lines:
                    next_line = lines[next_line_ind]
                    if next_line.strip():
                        body_indent = count_indent(next_line)
                
                # keywords to check whether n is divided inside while loop
                iterator = get_while_loop_iterator(stripped_line)
                log_keywords = [
                    "n=n/", 
                    "n/=",
                    "n=n//", 
                    "n//=",
                    f"{iterator}*=",
                    f"{iterator}={iterator}*",
                ]

                # check whether n is divided inside while loop
                temp_line_ind = line_ind + 1
                while temp_line_ind < num_lines and count_indent(lines[temp_line_ind]) >= body_indent:
                    for keyword in log_keywords:
                        if keyword in lines[temp_line_ind].replace(" ", ""):
                            includes_log = True
                            break
                    if includes_log:
                        break
                    temp_line_ind += 1
                
                # recursively analyze while loop body
                new_power, new_includes_log, new_line_index = analyze_code_block(
                    lines, 
                    start_line=line_ind + 1, 
                    base_indent=body_indent
                )

                # update results
                max_power = max(max_power, 1 + new_power)
                includes_log = includes_log or new_includes_log
                line_ind = new_line_index
                continue
        
            line_ind += 1
        
        return max_power, includes_log, line_ind

    try:
        # validate file extension
        dot_index = file_name.find(".")
        if dot_index < 0:
            return False, "invalid file name"
        file_extension = file_name[dot_index + 1:]
        if file_extension not in allowed_file_extensions:
            return False, f"file extension not allowed\nallowed file extensions = {', '.join(allowed_file_extensions)}"

        # read the file
        with open(file_name, "r") as file:
            file_contents = file.readlines()

        # analyse the code block
        power, includes_log, _ = analyze_code_block(file_contents)

        # return formatted tc
        return True, get_formatted_tc(power, includes_log)

    except Exception as e:
        return False, str(e)

def print_time_complexity_of_files(files: list[str]) -> None:
    longest_file_name_len = max([len(file) for file in files])
    for file_name in files:
        tc_ok, tc = get_time_complexity(file_name)
        spaces = longest_file_name_len - len(file_name)
        print(f"{spaces*' '}{file_name}: ", end="")
        
        if not tc_ok:
            print(f"something went wrong: {tc}")
        else:
            print(f"{tc}")

if __name__ == "__main__":
    print_time_complexity_of_files([
        "n1.py",
        "n2.py", 
        "n3.py",
        "logn.py",
        "nlogn.py",
        "n2logn.py",
    ])