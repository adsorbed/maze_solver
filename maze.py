from tkinter import Tk, BOTH, Canvas
import time
import random

class Line:
    def __init__(self, point1: tuple, point2: tuple, win=None) -> None:
        if win: self.canvas = win.canvas
        self.point1 = point1
        self.point2 = point2
        
    
    def draw(self, fill_color, canvas = None):
        if not canvas: canvas = self.canvas
        x1, y1 = self.point1
        x2, y2 = self.point2
        canvas.create_line(x1,y1,x2,y2, fill = fill_color, width = 2)
        canvas.pack(fill=BOTH, expand=1)

class Cell:
    def __init__(self, point1, point2, win = None, lwall=True, rwall=True, twall=True, bwall=True) -> None:
        self.win = win
        if self.win: self.canvas = win.canvas
        self.lwall = lwall
        self.rwall = rwall
        self.twall = twall
        self.bwall = bwall
        self.point1 = point1
        self.point2 = point2
        self.centre = (self.point1[0]+self.point2[0])//2, (self.point1[1]+self.point2[1])//2
        self.visited = False
        
    def draw(self, fill_color, canvas = None):
        if not self.win:
            return
        if not canvas: canvas = self.canvas
        x1, y1 = self.point1
        x2, y2 = self.point2
        x_left, x_right = min(x1,x2), max(x1,x2)
        y_bottom, y_top = max(y1,y2), min(y1,y2) # note the strange ordering; y=0 at the top of the window and increases down the screen
        if self.lwall:
            canvas.create_line(x_left,y1,x_left,y2, fill = fill_color, width = 2)
        else:
            canvas.create_line(x_left,y1,x_left,y2, fill = "white", width = 2)
        if self.rwall:
            canvas.create_line(x_right,y1,x_right,y2, fill = fill_color, width = 2)
        else:
            canvas.create_line(x_right,y1,x_right,y2, fill = "white", width = 2)
        if self.twall:
            canvas.create_line(x1,y_top,x2,y_top, fill = fill_color, width = 2)
        else:
            canvas.create_line(x1,y_top,x2,y_top, fill = "white", width = 2)
        if self.bwall:
            canvas.create_line(x1,y_bottom,x2,y_bottom, fill = fill_color, width = 2)
        else:
            canvas.create_line(x1,y_bottom,x2,y_bottom, fill = "white", width = 2)
        canvas.pack(fill=BOTH, expand=1)


    def draw_move(self, to_cell, undo = False):
        if not self.win:
            return
        if undo:
            color = "gray"
        else:
            color = "red"
        line = Line(self.centre, to_cell.centre, self.win)
        line.draw(color)

    def undraw_lines(self, neighbours):
        # takes a list of neighbouring cells that aren't blocked by walls and 
        # draws gray lines between them, drawing over the red lines that should be connecting them before the function is called
        for cell in neighbours:
            self.draw_move(cell, undo=True)


class Maze:
    def __init__(
            self,
            x1,
            y1,
            num_rows,
            num_cols,
            cell_size_x,
            cell_size_y,
            win = None,
            seed = None
            ):
        random.seed(seed)
        self.win = win
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self._cells = self._create_cells()
        # add a check if the maze is too big to fit on the window?
           
    def _create_cells(self):
        column = [0]*self.num_rows
        all_cells = []
        for _ in range(self.num_cols):
            all_cells.append(column.copy())
        for i in range(self.num_cols):
            for j in range(self.num_rows):
                x_min = self.x1 + i*self.cell_size_x
                x_max = x_min + self.cell_size_x
                y_min = self.y1 + j*self.cell_size_y
                y_max = y_min + self.cell_size_y
                cell = Cell((x_min, y_min), (x_max, y_max), self.win)
                if self.win: cell.draw("black")
                all_cells[i][j] = cell
        return all_cells

    def draw_cell(self, I, J):
        if not self.win:
            return
        i = (I-self.x1)//self.cell_size_x
        j = (J-self.y1)//self.cell_size_y
        x_min = self.x1 + i*self.cell_size_x
        x_max = x_min + self.cell_size_x
        y_min = self.y1 + j*self.cell_size_y
        y_max = y_min + self.cell_size_y
        cell = Cell((x_min, y_min), (x_max, y_max), self.win)
        cell.draw("black")
        self.animate()
        
    def _break_entrance_and_exit(self):
        self._cells[0][0].twall = False
        self._cells[0][0].draw("black")
        self._cells[-1][-1].bwall = False
        self._cells[-1][-1].draw("black")

    def animate(self):
        if not self.win:
            return
        self.win.redraw()
        time.sleep(0.0003)

    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        # will call as self._break_walls_r(0, 0)
        while True:
            neighbours = self._find_unvisited_neighbours(i, j)
            if neighbours == []:
                return
            new_i, new_j = random.choice(neighbours)
            if new_i > i: # i.e. if we went right
                assert j == new_j
                assert new_i == i+1
                self._cells[i][j].rwall = False
                self._cells[new_i][j].lwall = False
            elif new_i < i: # i.e. if we went left
                assert j == new_j
                assert new_i == i-1
                self._cells[i][j].lwall = False
                self._cells[new_i][j].rwall = False
            elif new_j > j: # i.e. we went DOWN
                self._cells[i][j].bwall = False
                self._cells[i][new_j].twall = False
            elif new_j < j: # i.e. we went UP
                self._cells[i][j].twall = False
                self._cells[i][new_j].bwall = False
            self.animate()
            self._cells[i][j].draw("black")
            self._cells[new_i][new_j].draw("black")
            #time.sleep(0.2)
            self._break_walls_r(new_i, new_j)

            
    def _solve_r(self, i, j):
        self._cells[i][j].visited = True
        
        while True:
            if self._cells[-1][-1].visited:
                return True
            neighbours = self._find_accessible_unvisited_neighbours(i, j)
            if (self.num_cols-1, self.num_rows-1) in neighbours:
                neighbours = [(self.num_cols-1, self.num_rows-1)]
            if neighbours == []:
                accessible_neighbour_cells = [self._cells[i_][j_] for i_, j_ in self._find_accessible_neighbours(i, j)]
                self.animate()
                self._cells[i][j].undraw_lines(accessible_neighbour_cells) 
                # undraws the red lines connecting to this cell, because we have just found that this cell is a dead end
                return False
            
            new_i, new_j = random.choice(neighbours)
            self.animate()
            self._cells[i][j].draw_move(self._cells[new_i][new_j])
            self._solve_r(new_i, new_j)
            


    def _find_unvisited_neighbours(self, i, j):
        # returns a list of the neighbours as yet unvisited for the purpose of creating the maze
        # i is the column number,
        # j is the row number
        neighbours = []
        if i > 0 and self._cells[i-1][j].visited == False:
            neighbours.append((i-1,j))
        if j > 0 and self._cells[i][j-1].visited == False:
            neighbours.append((i,j-1))
        if i < self.num_cols-1 and self._cells[i+1][j].visited == False:
            neighbours.append((i+1,j))
        if j < self.num_rows-1 and self._cells[i][j+1].visited == False:
            neighbours.append((i,j+1))
        return neighbours
    
    def _find_accessible_neighbours(self, i, j):
        # returns a list of the presumably visited, accessible neighbours of the current cell for the purpose of undrawing paths that lead to a dead end
        # i is the column number
        # j is the row number
        neighbours = []
        if i > 0 and self._cells[i][j].lwall == False:
            neighbours.append((i-1,j))
        if j > 0 and  self._cells[i][j].twall == False:
            neighbours.append((i,j-1))
        if i < self.num_cols-1 and self._cells[i][j].rwall == False:
            neighbours.append((i+1,j))
        if j < self.num_rows-1 and self._cells[i][j].bwall == False:
            neighbours.append((i,j+1))
        return neighbours
    
    def _find_accessible_unvisited_neighbours(self, i, j):
        # returns a list of the unvisited, accessible neighbours of the current cell for the purpose of solving the maze
        # i is the column number,
        # j is the row number
        neighbours = []
        if i > 0 and self._cells[i-1][j].visited == False and self._cells[i][j].lwall == False:
            neighbours.append((i-1,j))
        if j > 0 and self._cells[i][j-1].visited == False and  self._cells[i][j].twall == False:
            neighbours.append((i,j-1))
        if i < self.num_cols-1 and self._cells[i+1][j].visited == False and self._cells[i][j].rwall == False:
            neighbours.append((i+1,j))
        if j < self.num_rows-1 and self._cells[i][j+1].visited == False and self._cells[i][j].bwall == False:
            neighbours.append((i,j+1))
        return neighbours

    def _reset_cells_visited(self):
        for col in self._cells:
            for cell in col:
                cell.visited = False
        return
