from copy import deepcopy

m = 0
n = 0
final = []
colors = []


class Block:
    def __init__(self, no, color):
        self.color = color
        self.no = no
        self.color_dom = []
        self.num_dom = []

    def __repr__(self):
        return "% s% s" % (self.no, self.color)


def to_block(raw):
    length = len(raw)
    color = raw[length - 1]
    raw = raw[:length - 1]
    if raw == "*":
        number = 0
    else:
        number = int(raw)
    new = Block(number, color)
    return new


def print_grid(arr):
    for i in range(m):
        print(arr[i])


def count_number_degree(grid, row, col):
    degree = -2
    for i in range(m):
        if grid[i][col].no == 0:
            degree += 1
    for i in range(m):
        if grid[row][i].no == 0:
            degree += 1
    return degree


def count_color_degree(grid, i, j):
    degree = 0
    xxx = [(i, j + 1), (i, j - 1), (i + 1, j), (i - 1, j)]
    for block in xxx:
        if -1 < block[0] < m and -1 < block[1] < m:
            if grid[block[0]][block[1]].color == "#":
                degree += 1

    return degree


def mrv(grid):
    return_list = [[], [], [], [], [], []]
    color_list = [[], [], []]
    color_list_count = []
    number_list = [[], [], []]
    number_list_count = []
    min_num = 999
    min_color = 999
    for row in range(m):
        for col in range(m):
            if grid[row][col].no == 0:
                number_list[0].append(grid[row][col])
                number_list[1].append(row)
                number_list[2].append(col)
                number_list_count.append(len(grid[row][col].num_dom))
            if grid[row][col].color == "#":
                color_list[0].append(grid[row][col])
                color_list[1].append(row)
                color_list[2].append(col)
                color_list_count.append(len(grid[row][col].color_dom))
    if number_list_count:
        min_num = min(number_list_count)
    if color_list_count:
        min_color = min(color_list_count)
    if not number_list_count and not color_list_count:
        return False
    if min_num == min_color:
        for i in range(len(number_list[0])):
            if number_list_count[i] == min_num:
                return_list[0].append(number_list[0][i])
                return_list[1].append(number_list[1][i])
                return_list[2].append(number_list[2][i])
                # return_list[1].append(number_list_count[i])
        for i in range(len(color_list[0])):
            if color_list_count[i] == min_color:
                return_list[3].append(color_list[0][i])
                return_list[4].append(color_list[1][i])
                return_list[5].append(color_list[2][i])
                # return_list[3].append(color_list_count[i])
    elif min_color > min_num:
        for i in range(len(number_list[0])):
            if number_list_count[i] == min_num:
                return_list[0].append(number_list[0][i])
                return_list[1].append(number_list[1][i])
                return_list[2].append(number_list[2][i])
                # return_list[1].append(number_list_count[i])
    else:
        for i in range(len(color_list[0])):
            if color_list_count[i] == min_color:
                return_list[0].append(color_list[0][i])
                return_list[1].append(color_list[1][i])
                return_list[2].append(color_list[2][i])
    return return_list


def degree(grid, mrv_list):
    if not mrv_list:
        return False
    degree_list = [[], [], []]
    for i in range(len(mrv_list[0])):
        degree_list[0].append(mrv_list[1][i])
        degree_list[1].append(mrv_list[2][i])
        if grid[mrv_list[1][i]][mrv_list[2][i]].no == 0:
            degree_list[2].append(count_number_degree(grid, mrv_list[1][i], mrv_list[2][i]))
        else:
            degree_list[2].append(count_color_degree(grid, mrv_list[1][i], mrv_list[2][i]))
    if degree_list[0]:
        maximum = max(degree_list[2])
    else:
        return False
    for j in range(len(degree_list[2])):
        if degree_list[2][j] == maximum:
            ff = [degree_list[0][j], degree_list[1][j]]
            return ff


def heuristic(grid, l):
    mrv_list = mrv(grid)
    tmp = degree(grid, mrv_list)
    if mrv_list:
        l[0] = tmp[0]
        l[1] = tmp[1]
        return True
    return False


# def update_location(arr, l):
#     for row in range(m):
#         for col in range(m):
#             if arr[row][col].no == 0 or arr[row][col].color == "#":
#                 l[0] = row
#                 l[1] = col
#                 return True
#     return False


def row_check(arr, row, num):
    for i in range(m):
        if arr[row][i].no == num:
            return True
    return False


def column_check(arr, col, num):
    for i in range(m):
        if arr[i][col].no == num:
            return True
    return False


def check_color(arr, i, j, sus_color):
    xxx = [(i, j + 1), (i, j - 1), (i + 1, j), (i - 1, j)]
    for block in xxx:
        if -1 < block[0] < m and -1 < block[1] < m:
            if arr[block[0]][block[1]].color != "#" and arr[block[0]][block[1]].no != 0 and arr[i][j].no != 0:
                if arr[block[0]][block[1]].no > arr[i][j].no:
                    if colors.index(arr[block[0]][block[1]].color) <= colors.index(sus_color):
                        return True
                elif arr[block[0]][block[1]].no < arr[i][j].no:
                    if colors.index(arr[block[0]][block[1]].color) >= colors.index(sus_color):
                        return True
            else:
                if arr[block[0]][block[1]].color == sus_color:
                    return True
    return False


def check_location_is_safe(arr, row, col, num):
    return not row_check(arr, row, num) and not column_check(arr, col, num)


def backtrack_algo(arr):
    global final
    final = arr
    l = [0, 0]

    if not heuristic(arr, l):
        return True

    row = l[0]
    col = l[1]

    if arr[row][col].num_dom:
        for num in arr[row][col].num_dom:
            if check_location_is_safe(arr, row, col, num):
                tmp = deepcopy(arr)
                arr[row][col].no = num
                arr[row][col].num_dom = []
                fc_number(arr, arr[row][col], row, col)
                fc_color(arr, row, col)
                if backtrack_algo(arr):
                    return True
                arr = tmp
                arr[row][col].num_dom.remove(num)
    else:
        for color in arr[row][col].color_dom:
            if not check_color(arr, row, col, color):
                tmp = deepcopy(arr)
                arr[row][col].color = color
                arr[row][col].color_dom = []
                fc_number(arr, arr[row][col], row, col)
                fc_color(arr, row, col)
                if backtrack_algo(arr):
                    return True
                arr = tmp
                arr[row][col].color_dom.remove(color)
    return False


def fc_init(grid):
    for i in range(m):
        for j in range(m):
            if grid[i][j].no == 0:
                for k in range(1, m + 1):
                    if not column_check(grid, j, k) and not row_check(grid, i, k):
                        grid[i][j].num_dom.append(k)

    for i in range(m):
        for j in range(m):
            if grid[i][j].color == "#":
                for k in colors:
                    if not check_color(grid, i, j, k):
                        grid[i][j].color_dom.append(k)


def fc_col(grid, col, num):
    for i in range(m):
        if num in grid[i][col].num_dom:
            grid[i][col].num_dom.remove(num)


def fc_row(grid, row, num):
    for i in range(m):
        if num in grid[row][i].num_dom:
            grid[row][i].num_dom.remove(num)


def fc_number(grid, block, row, col):
    fc_col(grid, col, block.no)
    fc_row(grid, row, block.no)


def fc_color(grid, i, j):
    xxx = [(i, j + 1), (i, j - 1), (i + 1, j), (i - 1, j)]
    for block in xxx:
        if -1 < block[0] < m and -1 < block[1] < m:
            if grid[block[0]][block[1]].no != 0 and grid[i][j].color != "#":
                if grid[block[0]][block[1]].no > grid[i][j].no:
                    for color_in_color_dom in grid[block[0]][block[1]].color_dom:
                        if colors.index(color_in_color_dom) <= colors.index(grid[i][j].color):
                            grid[block[0]][block[1]].color_dom.remove(color_in_color_dom)
                else:
                    for color_in_color_dom in grid[block[0]][block[1]].color_dom:
                        if colors.index(color_in_color_dom) >= colors.index(grid[i][j].color):
                            grid[block[0]][block[1]].color_dom.remove(color_in_color_dom)
            else:
                if grid[i][j].color in grid[block[0]][block[1]].color_dom:
                    grid[block[0]][block[1]].color_dom.remove(grid[i][j].color)
    # self color_dom checking
    if grid[i][j].no != 0 and grid[i][j].color == "#":
        for block in xxx:
            if -1 < block[0] < m and -1 < block[1] < m:
                if grid[block[0]][block[1]].color != "#" and grid[block[0]][block[1]].no != 0:
                    if grid[block[0]][block[1]].no > grid[i][j].no:
                        for color_in_color_dom in grid[i][j].color_dom:
                            if colors.index(color_in_color_dom) >= colors.index(grid[block[0]][block[1]].color):
                                grid[i][j].color_dom.remove(color_in_color_dom)

                    else:
                        for color_in_color_dom in grid[i][j].color_dom:
                            if colors.index(color_in_color_dom) <= colors.index(grid[block[0]][block[1]].color):
                                grid[i][j].color_dom.remove(color_in_color_dom)


def print_dom(grid):
    for listy in grid:
        for objecty in listy:
            print(objecty.color_dom)
        print()


inputs = input().split(" ")
m = int(inputs[1])
n = int(inputs[0])

colors = input().split(" ")
colors.reverse()
grid = [[0 for x in range(m)] for y in range(m)]

for i in range(m):
    grid[i] = input().split(" ")

main_grid = grid

for i in range(m):
    for j in range(m):
        main_grid[i][j] = to_block(grid[i][j])

print_grid(main_grid)
print()
# # making color_dom and num_dom
fc_init(main_grid)

if backtrack_algo(main_grid):
    print_grid(final)
else:
    print("No solution exists")
