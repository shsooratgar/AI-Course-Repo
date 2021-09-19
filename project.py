import copy

k = 5
m = 4
n = 5
explored_length = 0
frontier_length = 0


class card:
    def __init__(self, no, color):
        self.color = color
        self.no = no

    def __repr__(self):
        return "% s% s" % (self.no, self.color)


class board:
    def __init__(self, current_cards, parent):
        self.card_slots = current_cards
        self.depth = 0
        self.parent = parent
        self.p_moves = [-1, -1]

    def __eq__(self, other):
        if self.card_slots == other.card_slots:
            return True
        else:
            return False

    def move(self, originRow, destinationRow):
        self.card_slots[destinationRow].append(self.card_slots[originRow][
                                                   len(self.card_slots[originRow]) - 1])

        del self.card_slots[originRow][len(self.card_slots[originRow]) - 1]

    def num_goal(self, row):
        first = float('inf')
        for card_to_numcheck in self.card_slots[row]:
            second = card_to_numcheck.no
            # print('{} > {}'.format(first, second))
            if second >= first:
                return False
            first = second
        return True

    def color_goal(self, row):
        if len(self.card_slots[row]) == 0:
            return True
        row_color = self.card_slots[row][0].color
        for item in self.card_slots[row]:
            # print('{} != {}'.format(item.color, row_color))
            if item.color != row_color:
                return False
        return True

    def goal_test(self):
        for i in range(k):
            if len(self.card_slots[i]) >0:
                if not self.num_goal(i):
                    return False
                if not self.color_goal(i):
                    return False
        return True


# if __name__ == '__main__':
#   pool = Pool()
#  pool.map(self.num_goal, range(k))


def toCard(raw):
    if raw == '#':
        return None
    length = len(raw)
    color =raw[length -1]
    raw = raw[:length -1]
    number = int(raw)
    new = card(number, color)
    return new


def toArr(input, card_output):
    for i in range(k):
        card_output.append([])
        for item in input[i]:
            if toCard(item):
                card_output[i].append(toCard(item))
    del card_output[k]
    return card_output


def board_moves(board):
    legal_moves = []
    cards = board.card_slots
    for i in range(len(cards)):
        if cards[i]:
            moving_card = cards[i][len(cards[i]) - 1]
            moving_card_no = moving_card.no
            for j in range(len(cards)):
                if cards[j]:

                    if moving_card_no < cards[j][len(cards[j]) - 1].no:
                        legal_move = [i, j]
                        legal_moves.append(legal_move)
                else:
                    legal_move = [i, j]
                    legal_moves.append(legal_move)
    return legal_moves


def BFS(initial_board):
    global explored_length
    global frontier_length
    print(initial_board.card_slots)
    print("Start Search")
    print()
    print()
    frontier = [initial_board]
    if initial_board.goal_test == True:
        return initial_board
    explored = []
    while True:
        if not frontier:
            return False
        node = frontier.pop(0)
        explored.append(node)
        for move in board_moves(node):
            new_node = copy.deepcopy(node)
            new_node.move(move[0], move[1])
            new = True
            for item in frontier:
                if item == new_node:
                    new = False
                    break
            for sth in explored:
                if sth == new_node:
                    new = False
                    break
            if new == True:
                new_node.depth = node.depth + 1
                new_node.parent = node
                new_node.p_moves = move
                # print(new_node.card_slots)
                # print(new_node.depth)
                # print()
                if new_node.goal_test() == True:
                    explored_length = len(explored)
                    frontier_length = len(frontier)
                    return new_node
                else:
                    frontier.append(new_node)


initial_input = []
initial_board = [[]]
arr = list(map(int, input().split()))
k = arr[0]
m = arr[1]
n = arr[2]
for i in range(k):
    arr = list(map(str, input().split()))
    initial_input.append(arr)

initial_board = toArr(initial_input, initial_board)
b = board(initial_board, None)
Solution = BFS(b)
parent = Solution.parent
actions = []
while parent:
    actions.append(parent)
    parent = parent.parent
actions.reverse()
if Solution:
    print('The Solution Found At Depth {}'.format(Solution.depth))
    print(Solution.card_slots)
print('Explored Nodes {}'.format(explored_length))
print('{} Nodes Constructed'.format(frontier_length + explored_length))

for action in actions:
    print('Becomes {} By {} to {} \n'.format(action.card_slots, action.p_moves[0] + 1, action.p_moves[1] + 1))
print('at last {} to {}'.format(Solution.p_moves[0]+1,Solution.p_moves[1]+1))

# 5 4 5
# 19g 17g
# 8r 6r 5r
# 8b 5b 4b 1b 3r 7y
# 9y
# 4g 5y 6g
