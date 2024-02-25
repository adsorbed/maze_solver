import unittest 
from maze import Maze

class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        m1._break_entrance_and_exit()
        m1._break_walls_r(0,0)
        m1._reset_cells_visited()
        self.assertEqual(
            len(m1._cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_rows,
        )
        # self.assertEqual(
        #     type(m1._cells[0][0]),
        #     'class maze.Cell',
        # )
        self.assertEqual(
            m1._cells[0][0].point1,
            (0,0),
        )
        self.assertEqual(
            m1._cells[0][0].twall,
            False,
        )
        for col in m1._cells:
            for cell in col:
                self.assertEqual(
                    cell.visited, 
                    False,
                )
        solved = m1._solve_r(0,0)
        self.assertEqual(
            solved,
            True,
        )

if __name__ == "__main__":
    unittest.main()
