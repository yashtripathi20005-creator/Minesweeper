"""
Board class managing the Minesweeper grid and game logic.
"""
import random
import pygame
from src.cell import Cell
from src.constants import ROWS, COLS, NUM_MINES, NUMBER_COLORS


class Board:
    """The Minesweeper game board."""

    def __init__(self, rows=ROWS, cols=COLS, num_mines=NUM_MINES):
        self.rows = rows
        self.cols = cols
        self.num_mines = num_mines
        self.size = 0  # Will be calculated based on available space
        self.cells = []
        self.first_click = True
        self.game_over = False
        self.won = False
        self.flags_placed = 0
        self.revealed_count = 0

    def initialize(self, width, height, padding, status_height):
        """Calculate cell size and create the grid."""
        board_width = width - 2 * padding
        board_height = height - 2 * padding - status_height

        self.size = min(board_width // self.cols, board_height // self.rows)
        self.size = max(self.size, 20)  # Minimum size

        # Center the board
        self.offset_x = (width - self.size * self.cols) // 2
        self.offset_y = (height - self.size * self.rows - status_height) // 2 + status_height

        # Create cells
        self.cells = []
        for row in range(self.rows):
            cell_row = []
            for col in range(self.cols):
                cell = Cell(row, col, self.size)
                cell.x += self.offset_x
                cell.y += self.offset_y
                cell_row.append(cell)
            self.cells.append(cell_row)

    def place_mines(self, safe_row, safe_col):
        """Place mines randomly, avoiding the first click position."""
        positions = []
        for r in range(self.rows):
            for c in range(self.cols):
                if r != safe_row or c != safe_col:
                    positions.append((r, c))

        random.shuffle(positions)
        mine_positions = positions[:self.num_mines]

        for r, c in mine_positions:
            self.cells[r][c].is_mine = True

        # Calculate adjacent mine counts
        self._calculate_adjacent_counts()

    def _calculate_adjacent_counts(self):
        """Calculate the number of adjacent mines for each cell."""
        for row in range(self.rows):
            for col in range(self.cols):
                if self.cells[row][col].is_mine:
                    continue
                count = 0
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0:
                            continue
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < self.rows and 0 <= nc < self.cols:
                            if self.cells[nr][nc].is_mine:
                                count += 1
                self.cells[row][col].adjacent_mines = count

    def get_cell_at(self, pos):
        """Get the cell at the given screen position. Returns (row, col) or None."""
        x, y = pos
        for row in range(self.rows):
            for col in range(self.cols):
                if self.cells[row][col].get_rect().collidepoint(x, y):
                    return row, col
        return None

    def reveal_cell(self, row, col):
        """Reveal a cell. Returns True if mine was hit."""
        if self.game_over:
            return False

        cell = self.cells[row][col]

        if cell.is_flagged:
            return False

        if cell.is_revealed:
            return False

        # Check for mine
        if cell.is_mine:
            self._game_over_lose()
            return True

        # First click - place mines
        if self.first_click:
            self.place_mines(row, col)
            self.first_click = False

        # Reveal this cell
        self._reveal_cell_recursive(row, col)

        # Check win condition
        if self._check_win():
            self._game_over_win()

        return False

    def _reveal_cell_recursive(self, row, col):
        """Reveal a cell and recursively reveal empty neighbors."""
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            return

        cell = self.cells[row][col]

        if cell.is_revealed or cell.is_flagged:
            return

        if cell.is_mine:
            return

        cell.reveal()
        self.revealed_count += 1

        # If empty (0 adjacent mines), reveal neighbors
        if cell.adjacent_mines == 0:
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue
                    self._reveal_cell_recursive(row + dr, col + dc)

    def toggle_flag(self, row, col):
        """Toggle flag on a cell."""
        if self.game_over:
            return

        if self.first_click:
            # Can't flag before first click
            return

        cell = self.cells[row][col]
        if cell.is_revealed:
            return

        if cell.toggle_flag():
            self.flags_placed += 1 if cell.is_flagged else -1

    def _game_over_lose(self):
        """Handle game over (loss)."""
        self.game_over = True
        self.won = False
        # Reveal all mines and mark wrong flags
        for row in self.cells:
            for cell in row:
                if cell.is_mine:
                    cell.is_revealed = True
                if cell.is_flagged and not cell.is_mine:
                    cell.is_wrong_flag = True

    def _game_over_win(self):
        """Handle game over (win)."""
        self.game_over = True
        self.won = True
        # Flag all remaining mines
        for row in self.cells:
            for cell in row:
                if cell.is_mine and not cell.is_flagged:
                    cell.is_flagged = True

    def _check_win(self):
        """Check if the player has won."""
        total_non_mines = self.rows * self.cols - self.num_mines
        return self.revealed_count == total_non_mines

    def reveal_all_mines(self):
        """Reveal all mines (for debugging/visual)."""
        for row in self.cells:
            for cell in row:
                if cell.is_mine:
                    cell.is_revealed = True

    def draw(self, screen, colors, font):
        """Draw the entire board."""
        for row in self.cells:
            for cell in row:
                cell.draw(screen, colors, font)

    def update_hover(self, pos):
        """Update hover state for cells."""
        for row in self.cells:
            for cell in row:
                cell.is_hovered = cell.get_rect().collidepoint(pos)
