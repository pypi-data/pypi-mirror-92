class Problem:
    def __init__(self, initial, goal=None):
        # 指定搜索问题的初始状态和目标状态
        self.initial = initial
        self.goal = goal

    def actions(self, state):
        # 返回在给定状态下可以采取的动作
        raise NotImplementedError

    def transition(self, state, action):
        # 执行给定动作后达到的状态
        raise NotImplementedError

    def goal_test(self, state):
        # 给定状态是目标状态则返回True
        return state == self.goal


class Node:
    def __init__(self, state, parent=None, action=None):
        # 构造节点，记录当前状态、父节点和采取的动作
        self.state = state
        self.parent = parent
        self.action = action

    def __eq__(self, other):
        return isinstance(other, Node) and self.state == other.state

    def expand(self, problem: Problem):
        # 展开当前问题可以到达的所有子节点
        child = []
        for action in problem.actions(self.state):
            next_state = problem.transition(self.state, action)
            child.append(Node(next_state, self, action))
        return child

    def path(self):
        # 返回从根节点到该节点的路径
        if self.parent is None:
            return [self]
        return self.parent.path() + [self]


class LeapForward(Problem):
    def __init__(self, road=(), allowed_steps=()):
        self.road = road
        self.allowed_steps = allowed_steps
        super().__init__(initial=1, goal=len(self.road))

    def actions(self, state):
        if self.road[state - 1] == 0:
            return []
        return [s for s in self.allowed_steps if state + s <= self.goal]

    def transition(self, state, action):
        return state + action


class RiverCrossing(Problem):
    def __init__(self, forbidden_states=set()):
        super().__init__(initial=(1, 1, 1, 1), goal=(-1, -1, -1, -1))
        self.forbidden_states = set(forbidden_states)

    def actions(self, state):
        if state in self.forbidden_states:
            return []
        allowed_actions = [(-1, 1, 1, 1)]
        for n in range(1, len(state)):
            if state[n] == state[0]:
                action = tuple([-1 if i in [0, n] else 1 for i in range(4)])
                allowed_actions.append(action)

        return allowed_actions

    def transition(self, state, action):
        return tuple(s * a for s, a in zip(state, action))


class JumpingFrogs(Problem):
    def __init__(self, n=3):
        self.initial = n*'L' + '.' + n*'R'
        self.goal = self.initial[::-1]
        super().__init__(initial=self.initial, goal=self.goal)

    def actions(self, state):
        ids = range(len(state))
        return ({(i, i + 1) for i in ids if state[i: i + 2] == "L."}
                | {(i, i + 2) for i in ids if state[i: i + 3] == "LR."}
                | {(i + 1, i) for i in ids if state[i: i + 2] == ".R"}
                | {(i + 2, i) for i in ids if state[i: i + 3] == ".LR"})

    def transition(self, state, action):
        i, j = action
        result = list(state)
        result[i], result[j] = state[j], state[i]
        return "".join(result)


def TreeSearch(problem: Problem):
    # 实现树搜索算法
    frontier = [Node(problem.initial)]
    explored = set()
    while frontier:
        node = frontier.pop()
        if problem.goal_test(node.state):
            return node
        explored.add(node.state)
        frontier.extend(n for n in node.expand(problem) if n.state not in explored)
    return None


def leapForward():
    import random
    allowed_steps = (2, 3, 4)
    road = [1]
    for _ in range(11):
        road.append(random.randint(0, 1))
    road.append(1)

    display_road = ["_" if s == 1 else "^" for s in road]
    print(" ".join(display_road))
    print("\n")

    leap_forward = LeapForward(road, allowed_steps)
    result = TreeSearch(leap_forward)
    if result:
        # print([node.action for node in result.path() if node.action])
        for node in result.path():
            copy = display_road.copy()
            copy[node.state - 1] = "@"
            print(" ".join(copy))
            print("\n")
    else:
        print("未找到有效路径")


def riverCrossing():
    forbidden_states = {
        (1, 1, -1, -1),
        (1, -1, -1, 1),
        (1, -1, -1, -1),
        (-1, -1, 1, 1),
        (-1, 1, 1, -1),
        (-1, 1, 1, 1)
    }
    river_crossing = RiverCrossing(forbidden_states=forbidden_states)
    result = TreeSearch(river_crossing)
    if result:
        for node in result.path():
            print("".join(["N" if s == 1 else "F" for s in node.state]))
    else:
        print("未找到可行路径")


def jumpingFrogs():
    jumping_frogs = JumpingFrogs()
    result = TreeSearch(jumping_frogs)
    if result:
        for node in result.path():
            print(node.state)
    else:
        print("未找到有效路径")


if __name__ == "__main__":
    # leapForward()
    # riverCrossing()
    jumpingFrogs()
