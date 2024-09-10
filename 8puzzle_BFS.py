from collections import deque

# A helper function to print the 3x3 grid
def print_puzzle(puzzle):
    for row in puzzle:
        print(row)
    print()

# A class to represent the state of the puzzle
class PuzzleState:
    def __init__(self, puzzle, parent=None, move=None, depth=0):
        self.puzzle = puzzle
        self.parent = parent
        self.move = move
        self.depth = depth

    # A method to check if the current state is the goal state
    def is_goal(self, goal):
        return self.puzzle == goal

    # A method to find the position of the blank (zero) tile
    def find_blank(self):
        for i, row in enumerate(self.puzzle):
            if 0 in row:
                return (i, row.index(0))

    # A method to generate the possible moves from the current state
    def generate_moves(self):
        blank_row, blank_col = self.find_blank()
        moves = []
        # Define possible directions: (row_offset, col_offset)
        directions = [('up', (-1, 0)), ('down', (1, 0)), ('left', (0, -1)), ('right', (0, 1))]

        for move_name, (row_offset, col_offset) in directions:
            new_row, new_col = blank_row + row_offset, blank_col + col_offset
            if 0 <= new_row < 3 and 0 <= new_col < 3:
                # Make a copy of the current puzzle
                new_puzzle = [row[:] for row in self.puzzle]
                # Swap the blank tile with the adjacent tile
                new_puzzle[blank_row][blank_col], new_puzzle[new_row][new_col] = new_puzzle[new_row][new_col], new_puzzle[blank_row][blank_col]
                moves.append(PuzzleState(new_puzzle, self, move_name, self.depth + 1))
        return moves

# BFS function to solve the puzzle
def bfs(initial_puzzle, goal_puzzle):
    # Initialize the queue for BFS
    queue = deque([PuzzleState(initial_puzzle)])
    # Set to keep track of visited states
    visited = set()
    visited.add(tuple(tuple(row) for row in initial_puzzle))

    while queue:
        current_state = queue.popleft()

        # Check if we have reached the goal state
        if current_state.is_goal(goal_puzzle):
            return current_state

        # Generate possible moves and add them to the queue
        for move in current_state.generate_moves():
            state_tuple = tuple(tuple(row) for row in move.puzzle)
            if state_tuple not in visited:
                visited.add(state_tuple)
                queue.append(move)

    return None

# Function to print the solution steps
def print_solution(solution):
    path = []
    current = solution
    while current:
        path.append(current)
        current = current.parent
    path.reverse()

    for step in path:
        print(f"Move: {step.move}")
        print_puzzle(step.puzzle)

# Main function to solve the 8-puzzle problem
if __name__ == '__main__':
    # Initial state of the puzzle (0 represents the blank space)
    initial_puzzle = [
        [1, 2, 3],
        [0, 4, 6],
        [7, 5, 8]
    ]

    # Goal state of the puzzle
    goal_puzzle = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 0]
    ]

    print("Initial Puzzle:")
    print_puzzle(initial_puzzle)

    # Solve the puzzle using BFS
    solution = bfs(initial_puzzle, goal_puzzle)

    # If a solution is found, print the steps
    if solution:
        print("Solution found:")
        print_solution(solution)
    else:
        print("No solution exists.")
