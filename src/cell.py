"""
Cell class representing a single square on the Minesweeper board.
"""
import pygame


class Cell:
    """A single cell in the Minesweeper grid."""

    def __init__(self, row, col, size):
        self.row = row
        self.col = col
        self.size = size
        self.x = col * size
        self.y = row * size
        self.is_mine = False
        self.is_revealed = False
        self.is_flagged = False
        self.is_wrong_flag = False  # For game over: flag on non-mine
        self.adjacent_mines = 0
        self.is_hovered = False

    def get_rect(self):
        """Return the pygame Rect for this cell."""
        return pygame.Rect(self.x, self.y, self.size, self.size)

    def reveal(self):
        """Reveal the cell. Returns True if it was a mine."""
        if self.is_flagged:
            return False
        self.is_revealed = True
        return self.is_mine

    def toggle_flag(self):
        """Toggle flag on this cell. Only if not revealed."""
        if not self.is_revealed:
            self.is_flagged = not self.is_flagged
            return True
        return False

    def draw(self, screen, colors, font):
        """Draw the cell on the screen."""
        rect = self.get_rect()

        if self.is_revealed:
            # Revealed cell
            if self.is_mine:
                # Mine cell (only shown on game over)
                pygame.draw.rect(screen, colors["CELL_REVEALED"], rect)
                pygame.draw.rect(screen, colors["CELL_BORDER"], rect, 1)
                # Draw mine
                center = (self.x + self.size // 2, self.y + self.size // 2)
                radius = self.size // 3
                pygame.draw.circle(screen, colors["MINE"], center, radius)
                # Small inner circle
                pygame.draw.circle(screen, colors["MINE"], center, radius // 2)
            else:
                # Normal revealed cell
                pygame.draw.rect(screen, colors["CELL_REVEALED"], rect)
                pygame.draw.rect(screen, colors["CELL_BORDER"], rect, 1)

                # Draw number if adjacent mines > 0
                if self.adjacent_mines > 0:
                    text = font.render(str(self.adjacent_mines), True, colors["NUMBER"][self.adjacent_mines])
                    text_rect = text.get_rect(center=rect.center)
                    screen.blit(text, text_rect)
        else:
            # Hidden cell
            color = colors["CELL_HIDDEN_HOVER"] if self.is_hovered else colors["CELL_HIDDEN"]
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, colors["CELL_BORDER"], rect, 1)

            # Draw flag if flagged
            if self.is_flagged:
                # Flag shape (simplified)
                center_x = self.x + self.size // 2
                center_y = self.y + self.size // 2
                flag_color = colors["WRONG_FLAG"] if self.is_wrong_flag else colors["FLAG"]

                # Flag pole
                pole_x = center_x - self.size // 4
                pygame.draw.line(screen, (0, 0, 0),
                                 (pole_x, center_y - self.size // 3),
                                 (pole_x, center_y + self.size // 3), 2)
                # Flag triangle
                points = [
                    (pole_x, center_y - self.size // 3),
                    (pole_x + self.size // 3, center_y - self.size // 6),
                    (pole_x, center_y)
                ]
                pygame.draw.polygon(screen, flag_color, points)
