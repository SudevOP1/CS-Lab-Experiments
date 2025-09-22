
# for optimization
START = True
END = False

def input_bldgs(n: int) -> list[list[int]]:
    return [[
        int(input(f"bldg_{i+1} l: ")),
        int(input(f"bldg_{i+1} h: ")),
        int(input(f"bldg_{i+1} r: ")),
    ] for i in range(n)]

def get_skyline(bldgs: list[list[int]]) -> list[int]:
    if not bldgs:
        return []
    
    # get all critical points (start and end of bldgs)
    points = []
    for l, h, r in bldgs:
        points.append((l, h, START))
        points.append((r, h, END))
    
    # sort points by x coords
    # for same x, process end before start (for edge cases)
    points.sort(key=lambda x: (x[0], x[2] == START))
    
    # track active building heights
    active_heights = []
    result = []
    prev_max_height = 0
    
    i = 0
    while i < len(points):
        curr_x = points[i][0]
        
        # process all points at the same x coords
        while i < len(points) and points[i][0] == curr_x:
            x, h, event = points[i]
            
            if event == START:
                active_heights.append(h)
            else:
                active_heights.remove(h)
            
            i += 1
        
        # find current max height
        curr_max_height = max(active_heights) if active_heights else 0
        
        # if height changed, add to result
        if curr_max_height != prev_max_height:
            result.extend([curr_x, curr_max_height])
            prev_max_height = curr_max_height
    
    # add final point
    if result and result[-1] != 0:
        result.append(0)
    
    return result

if __name__ == "__main__":
    # print(get_skyline(input_bldgs(int(input("enter num bldgs: ")))))

    # test cases 👇
    print(get_skyline([
        [1, 10, 6],
        [2, 30, 4],
        [3, 30, 5],
    ])) # [1, 10, 2, 30, 5, 10, 6, 0]
    print(get_skyline([
        [ 3, 13,  9],
        [ 1, 11,  5],
        [12,  7, 16],
        [14,  3, 25],
        [19, 18, 22],
        [ 2,  6,  7],
        [23, 13, 29],
        [23,  4, 28],
    ])) # [1, 11, 3, 13, 9, 0, 12, 7, 16, 3, 19, 18, 22, 3, 23, 13, 29, 0]

