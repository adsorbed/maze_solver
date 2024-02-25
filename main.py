from window import *
from maze import *


def main():
    win = Window(540, 540)
    maze = Maze(20, 20, 25, 25, 20, 20, win)
    maze._create_cells()
    maze._break_entrance_and_exit()
    maze._break_walls_r(0,0)
    maze._reset_cells_visited()
    maze._solve_r(0, 0)
    win.wait_for_close()

main()