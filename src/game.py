"""
Main game class managing the game loop and state.
"""
import pygame
import sys
from src.board import Board
from src.constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, BOARD_PADDING, STATUS_BAR_HEIGHT,
    ROWS, COLS, NUM_MINES,
    COLOR_BG, COLOR_BOARD_BG, COLOR_STATUS_BG, COLOR_STATUS_TEXT,
    COLOR_WIN, COLOR_LOSE, COLOR_TEXT,
    FONT_NAME, FONT_SIZE_LARGE, FONT_SIZE_MEDIUM, FONT_SIZE_SMALL,
    DIFFICULTIES, NUMBER_COLORS
)


class Game:
    """Main game class."""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Minesweeper Clone")

        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.SysFont(FONT_NAME, FONT_SIZE_LARGE)
        self.font_medium = pygame.font.SysFont(FONT_NAME, FONT_SIZE_MEDIUM)
        self.font_small = pygame.font.SysFont(FONT_NAME, FONT_SIZE_SMALL)

        # Color dictionary for easy access
        self.colors = {
            "BG": COLOR_BG,
            "BOARD_BG": COLOR_BOARD_BG,
            "CELL_HIDDEN": (120, 120, 120),
            "CELL_HIDDEN_HOVER": (140, 140, 140),
            "CELL_REVEALED": (220, 220, 220),
            "CELL_BORDER": (160, 160, 160),
            "MINE": (255, 0, 0),
            "FLAG": (255, 50, 50),
            "WRONG_FLAG": (255, 200, 200),
            "NUMBER": NUMBER_COLORS,
            "STATUS_BG": COLOR_STATUS_BG,
            "STATUS_TEXT": COLOR_STATUS_TEXT,
            "TEXT": COLOR_TEXT,
            "WIN": COLOR_WIN,
            "LOSE": COLOR_LOSE,
        }

        self.difficulty = "Easy"
        self.board = None
        self.mouse_pos = (0, 0)

        # UI buttons for difficulty
        self.difficulty_buttons = []
        self._create_difficulty_buttons()

        # Reset game
        self.reset_game()

    def _create_difficulty_buttons(self):
        """Create difficulty selection buttons."""
        button_width = 70
        button_height = 30
        y = 10
        x_start = WINDOW_WIDTH - 250

        for i, (name, _) in enumerate(DIFFICULTIES.items()):
            x = x_start + i * (button_width + 5)
            rect = pygame.Rect(x, y, button_width, button_height)
            self.difficulty_buttons.append({
                "rect": rect,
                "name": name,
                "hovered": False
            })

    def reset_game(self):
        """Reset the game board with current difficulty."""
        diff = DIFFICULTIES[self.difficulty]
        self.board = Board(diff["rows"], diff["cols"], diff["mines"])
        self.board.initialize(WINDOW_WIDTH, WINDOW_HEIGHT, BOARD_PADDING, STATUS_BAR_HEIGHT)

    def handle_events(self):
        """Handle pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.MOUSEMOTION:
                self.mouse_pos = event.pos
                # Update hover for difficulty buttons
                for btn in self.difficulty_buttons:
                    btn["hovered"] = btn["rect"].collidepoint(event.pos)
                # Update board hover
                if self.board:
                    self.board.update_hover(event.pos)

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check difficulty buttons
                for btn in self.difficulty_buttons:
                    if btn["rect"].collidepoint(event.pos):
                        self.difficulty = btn["name"]
                        self.reset_game()
                        return True

                # Check board clicks
                if self.board and not self.board.game_over:
                    pos = self.board.get_cell_at(event.pos)
                    if pos:
                        row, col = pos
                        if event.button == 1:  # Left click
                            self.board.reveal_cell(row, col)
                        elif event.button == 3:  # Right click
                            self.board.toggle_flag(row, col)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.reset_game()
                if event.key == pygame.K_1:
                    self.difficulty = "Easy"
                    self.reset_game()
                if event.key == pygame.K_2:
                    self.difficulty = "Medium"
                    self.reset_game()
                if event.key == pygame.K_3:
                    self.difficulty = "Hard"
                    self.reset_game()

        return True

    def draw(self):
        """Draw everything on the screen."""
        self.screen.fill(self.colors["BG"])

        # Draw board background
        if self.board:
            board_rect = pygame.Rect(
                BOARD_PADDING,
                STATUS_BAR_HEIGHT + BOARD_PADDING,
                self.board.size * self.board.cols,
                self.board.size * self.board.rows
            )
            pygame.draw.rect(self.screen, self.colors["BOARD_BG"], board_rect)
            self.board.draw(self.screen, self.colors, self.font_medium)

        # Draw status bar
        self._draw_status_bar()

        # Draw difficulty buttons
        self._draw_difficulty_buttons()

        # Draw game over overlay
        if self.board and self.board.game_over:
            self._draw_game_over_overlay()

        pygame.display.flip()

    def _draw_status_bar(self):
        """Draw the status bar at the top."""
        status_rect = pygame.Rect(0, 0, WINDOW_WIDTH, STATUS_BAR_HEIGHT)
        pygame.draw.rect(self.screen, self.colors["STATUS_BG"], status_rect)

        if self.board:
            # Mines remaining
            mines_left = self.board.num_mines - self.board.flags_placed
            text = f"💣 {mines_left}  |  Flags: {self.board.flags_placed}  |  {self.difficulty}  |  [R]eset"
            rendered = self.font_small.render(text, True, self.colors["STATUS_TEXT"])
            self.screen.blit(rendered, (10, 20))

            # Game status
            if self.board.game_over:
                if self.board.won:
                    status_text = "🎉 YOU WIN!"
                    color = self.colors["WIN"]
                else:
                    status_text = "💥 GAME OVER"
                    color = self.colors["LOSE"]
                rendered = self.font_large.render(status_text, True, color)
                text_rect = rendered.get_rect(center=(WINDOW_WIDTH // 2, STATUS_BAR_HEIGHT // 2))
                self.screen.blit(rendered, text_rect)

    def _draw_difficulty_buttons(self):
        """Draw difficulty selection buttons."""
        for btn in self.difficulty_buttons:
            rect = btn["rect"]
            is_selected = btn["name"] == self.difficulty

            # Button background
            color = (100, 200, 100) if is_selected else (80, 80, 80)
            if btn["hovered"] and not is_selected:
                color = (100, 100, 100)
            pygame.draw.rect(self.screen, color, rect)
            pygame.draw.rect(self.screen, (200, 200, 200), rect, 1)

            # Button text
            text = self.font_small.render(btn["name"], True, (255, 255, 255))
            text_rect = text.get_rect(center=rect.center)
            self.screen.blit(text, text_rect)

    def _draw_game_over_overlay(self):
        """Draw a semi-transparent overlay when game is over."""
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))

        # Only cover the board area
        if self.board:
            board_rect = pygame.Rect(
                BOARD_PADDING,
                STATUS_BAR_HEIGHT + BOARD_PADDING,
                self.board.size * self.board.cols,
                self.board.size * self.board.rows
            )
            overlay.fill((0, 0, 0, 100), board_rect)

        self.screen.blit(overlay, (0, 0))

    def run(self):
        """Main game loop."""
        running = True
        while running:
            running = self.handle_events()
            self.draw()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()
