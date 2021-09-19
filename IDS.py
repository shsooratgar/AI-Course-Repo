import copy

k = 5
m = 4
n = 5
explored_nodes = 0
created_nodes = 1


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
        self.p_moves = [-1 , -1]

    def __eq__(self, other):
        if isinstance(other, int):
            return False
        elif self.card_slots == other.card_slots:
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


def RECURSIVE_DLS(initial_board, limit):
    global created_nodes
    global explored_nodes
    explored_nodes += 1
    if initial_board.goal_test():

        return initial_board
    elif limit == 0:
        return 100
    else:
        cutoff_occurred = False
        for move in board_moves(initial_board):
            child = copy.deepcopy(initial_board)
            child.move(move[0], move[1])
            child.depth += 1
            child.parent = initial_board
            child.p_moves = move
            created_nodes +=1
            # print(child.card_slots)
            result = RECURSIVE_DLS(child, limit - 1)
            if result == 100:
                cutoff_occurred = True
            elif result != False:
                return result
        if cutoff_occurred == True:
            return 100
        else:
            return False


def DEPTH_LIMITED_SEARCH(initial_board, limit):
    return RECURSIVE_DLS(initial_board, limit)


def IDS(initial_board, initial_limit):
    print("start")
    limit = initial_limit
    while True:
        result = DEPTH_LIMITED_SEARCH(initial_board, limit)
        if result != 100:
            # print(result.depth)
            return result
        limit += 1
        # print(limit)


initial_input = []
initial_board =[[]]
arr = list(map(int, input().split()))
k = arr[0]
m = arr[1]
n = arr[2]
for i in range(k):
    arr = list(map(str, input().split()))
    initial_input.append(arr)

initial_board =toArr(initial_input,initial_board)
b = board(initial_board, None)

Solution = IDS(b, 1)
parent = Solution.parent
actions = []
while parent:
    actions.append(parent)
    parent = parent.parent
actions.reverse()
if Solution:
    print('The Solution Found At Depth {}'.format(Solution.depth))
    print(Solution.card_slots)
print('Explored Nodes {}'.format(explored_nodes))
print('{} Nodes Constructed'.format(created_nodes))
for action in actions:
    print('Becomes {} By {} to {} \n'.format(action.card_slots,action.p_moves[0] + 1,action.p_moves[1] + 1))
print('at last {} to {}'.format(Solution.p_moves[0]+1,Solution.p_moves[1]+1))