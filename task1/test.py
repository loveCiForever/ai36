import pygame
import sys
import tkinter as tk
from tkinter import simpledialog
from pygame.locals import *
from copy import deepcopy
import time
delay = 0.5
goal_states = [
    [[1, 2, 3],
     [4, 5, 6],
     [7, 8, 0]],

    [[8, 7, 6],
     [5, 4, 3],
     [2, 1, 0]],

    [[0, 1, 2],
     [3, 4, 5],
     [6, 7, 8]],

    [[0, 8, 7],
     [6, 5, 4],
     [3, 2, 1]]
]

class Puzzle:
    def __init__(self, state, action=None, parent=None, g=0, h=0):
        self.state = state
        self.id = str(self.state)
        self.action = action
        self.parent = parent
        self.g = g
        self.h = h
        self.f = g + h

    def __eq__(self, other):
        return self.state == other.state

    def __hash__(self):
        return hash(str(self.state))

    def __lt__(self, other):
        return self.f < other.f

    @staticmethod
    def get_pos(state, val):
        for i in range(3):
            for j in range(3):
                if state[i][j] == val:
                    return i, j
        return None

    @staticmethod
    def check_neighbor(state, a, b):
        pos_a, pos_b = Puzzle.get_pos(state, a), Puzzle.get_pos(state, b)
        if not pos_a or not pos_b:
            return False
        return (pos_a[0] == pos_b[0] and abs(pos_a[1] - pos_b[1]) == 1) or \
               (pos_a[1] == pos_b[1] and abs(pos_a[0] - pos_b[0]) == 1)

    @staticmethod
    def swap(state, a, b):
        a_i, a_j = Puzzle.get_pos(state, a)
        b_i, b_j = Puzzle.get_pos(state, b)
        state[a_i][a_j], state[b_i][b_j] = state[b_i][b_j], state[a_i][a_j]

    def get_dest_pos(self, action, pi, pj):
        return {
            'L': (pi, pj + 1),
            'R': (pi, pj - 1),
            'U': (pi + 1, pj),
            'D': (pi - 1, pj),
        }.get(action, (pi, pj))

    def get_successor(self, action, state):
        pi, pj = Puzzle.get_pos(state, 0)
        ni, nj = self.get_dest_pos(action, pi, pj)
        if 0 <= ni < 3 and 0 <= nj < 3:
            state[pi][pj], state[ni][nj] = state[ni][nj], 0
            return state
        return None

    def get_successors(self):
        was_13 = Puzzle.check_neighbor(self.state, 1, 3)
        was_24 = Puzzle.check_neighbor(self.state, 2, 4)
        successors = []

        for act in ['L', 'R', 'U', 'D']:
            new_state = self.get_successor(act, deepcopy(self.state))
            if new_state is None:
                continue
            if Puzzle.check_neighbor(new_state, 1, 3) and not was_13:
                Puzzle.swap(new_state, 1, 3)
            if Puzzle.check_neighbor(new_state, 2, 4) and not was_24:
                Puzzle.swap(new_state, 2, 4)
            successors.append(Puzzle(new_state, act, self))

        return successors

class PuzzleGame:
    def __init__(self, puzzle):
        pygame.init()
        self.puzzle = puzzle
        self.screen = pygame.display.set_mode((300, 400))
        pygame.display.set_caption('8 Puzzle Game')
        self.font = pygame.font.SysFont(None, 60)
        self.small_font = pygame.font.SysFont(None, 30)
        self.goal_font = pygame.font.SysFont(None, 40)
        self.running = True
        self.completed = False
        self.solution = []
        self.auto_playing = False
        self.solution_loaded = False
        self.start_button_rect = pygame.Rect(10, 350, 100, 40)
        self.import_button_rect = pygame.Rect(10, 320,160, 30)

    def draw_board(self):
        self.screen.fill((255, 255, 255))
        for i in range(3):
            for j in range(3):
                value = self.puzzle.state[i][j]
                rect = pygame.Rect(j * 100, i * 100, 100, 100)
                pygame.draw.rect(self.screen, (0, 0, 0), rect, 3)
                if value != 0:
                    text = self.font.render(str(value), True, (0, 0, 0))
                    text_rect = text.get_rect(center=rect.center)
                    self.screen.blit(text, text_rect)

        pygame.draw.rect(self.screen, (200, 200, 200), self.import_button_rect)
        imp_text = self.small_font.render("Import solution", True, (0, 0, 0))
        self.screen.blit(imp_text, (15, 325))

        if self.solution_loaded and not self.auto_playing:
            pygame.draw.rect(self.screen, (100, 200, 100), self.start_button_rect)
            start_text = self.small_font.render("Start", True, (0, 0, 0))
            self.screen.blit(start_text, (35,360))

        if self.completed:
            msg = self.goal_font.render("Complete", True, (0, 128, 0))
            self.screen.blit(msg, (30, 130))

        pygame.display.flip()

    def is_goal_state(self):
        return any(self.puzzle.state == goal for goal in goal_states)

    def import_solution(self):
        root = tk.Tk()
        root.withdraw()
        moves_str = simpledialog.askstring("Solution", "input action list (Ex: 'D','L','U'):")
        if moves_str:
            try:
                self.solution = [s.strip(" '") for s in moves_str.strip().split(',')]
                self.solution_loaded = True
            except:
                print("Error input")

    def auto_play(self):
        if not self.auto_playing:
            return
        if not self.solution:
            self.auto_playing = False
            return
        action = self.solution.pop(0)
        for next_puzzle in self.puzzle.get_successors():
            if next_puzzle.action == action:
                self.puzzle = next_puzzle
                if self.is_goal_state():
                    self.completed = True
                    self.auto_playing = False
                break
        time.sleep(delay)

    def handle_mouse(self, pos):
        if self.import_button_rect.collidepoint(pos):
            self.import_solution()
        elif self.start_button_rect.collidepoint(pos) and self.solution_loaded and not self.auto_playing:
            self.auto_playing = True

    def run(self):
        while self.running:
            self.draw_board()
            self.auto_play()
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                elif event.type == MOUSEBUTTONDOWN:
                    self.handle_mouse(event.pos)
                elif event.type == KEYDOWN:
                    if not self.completed and not self.auto_playing:
                        move_map = {
                            K_LEFT: 'L',
                            K_RIGHT: 'R',
                            K_UP: 'U',
                            K_DOWN: 'D'
                        }
                        if event.key in move_map:
                            action = move_map[event.key]
                            for next_puzzle in self.puzzle.get_successors():
                                if next_puzzle.action == action:
                                    self.puzzle = next_puzzle
                                    if self.is_goal_state():
                                        self.completed = True
                                    break
        pygame.quit()
        sys.exit()

def get_initial_state():
    root = tk.Tk()
    root.withdraw()
    raw = simpledialog.askstring("Initial State", "Input initial state (ex: 123_45678):")
    if raw:
        raw = ''.join(raw.split()).replace('_', '0')
        if len(raw) == 9 and all(c.isdigit() for c in raw):
            nums = [int(c) for c in raw]
            if sorted(nums) == list(range(9)):
                return [nums[:3], nums[3:6], nums[6:]]
    print("error input")
    sys.exit()

if __name__ == '__main__':
    initial_state = get_initial_state()
    puzzle = Puzzle(initial_state)
    game = PuzzleGame(puzzle)
    game.run()
