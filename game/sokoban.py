import pygame
from maze import *

# Initialize Pygame
pygame.init()

# Set up the display
screen_width = 1000
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))


class Man:
    def __init__(self, pos):
        self.pos = pos
        self.direction = "right"
        self.is_pushing = False

    def set_Direction(self, newDirection):
        self.direction = newDirection

    def set_Pushing(self, ispushing):
        self.is_pushing = ispushing

    def draw(self, sprite_sheet, offset_x, offset_y):
        sprites = {
            "up": (0, 1),
            "right": (0, 55),
            "down": (0, 109),
            "left": (0, 163)
        }

        push_spriters = {
            "up": (200, 1),
            "right": (200, 55),
            "down": (200, 109),
            "left": (200, 163),
        }

        man_sprite_rect = pygame.Rect(sprites[self.direction][0], sprites[self.direction][1], 40, 54)

        if self.is_pushing:
            man_sprite_rect = pygame.Rect(push_spriters[self.direction][0], push_spriters[self.direction][1], 40, 54)

        screen.blit(
            sprite_sheet,
            (self.pos.line * 39 + offset_x, self.pos.col * 53 + offset_y),
            man_sprite_rect
        )

    def __str__(self):
        return f"Man Position: {self.pos}"


class Boxes:
    def __init__(self, positions):
        self.positions = positions

    def draw(self, sprite_sheet, offset_x, offset_y, target_positions):
        BOX = (80, 218)
        BoxOnTarget = (120, 218)

        box_sprite_rect = pygame.Rect(BOX[0], BOX[1], 40, 54)
        BoxOnTarget = pygame.Rect(BoxOnTarget[0], BoxOnTarget[1], 40, 54)

        for element in self.positions:
            spriteImage = box_sprite_rect
            if element in target_positions:
                spriteImage = BoxOnTarget

            screen.blit(
                sprite_sheet,
                (element.line * 39 + offset_x, element.col * 53 + offset_y),
                spriteImage
            )

    def __str__(self):
        positions_str = ", ".join(str(pos) for pos in self.positions)
        return f"Box Positions: [{positions_str}]"


class Target:
    def __init__(self, positions):
        self.positions = positions

    def draw(self, sprite_sheet, offset_x, offset_y):
        TARGET = (0, 218)
        box_sprite_rect = pygame.Rect(TARGET[0], TARGET[1], 40, 54)

        for element in self.positions:
            screen.blit(
                sprite_sheet,
                (element.line * 39 + offset_x, element.col * 53 + offset_y),
                box_sprite_rect
            )

    def __str__(self):
        positions_str = ", ".join(str(pos) for pos in self.positions)
        return f"Target Positions: [{positions_str}]"


class Wall:
    def __init__(self, positions):
        self.positions = positions

    def draw(self, sprite_sheet, offset_x, offset_y):
        WALL = (40, 218)
        box_sprite_rect = pygame.Rect(WALL[0], WALL[1], 40, 54)

        for element in self.positions:
            screen.blit(
                sprite_sheet,
                (element.line * 39 + offset_x, element.col * 53 + offset_y),
                box_sprite_rect
            )

    def __str__(self):
        positions_str = ", ".join(str(pos) for pos in self.positions)
        return f"Wall Positions: [{positions_str}]"


class Game:
    def __init__(self):
        self.sokoban_level = load_level("maps.txt")
        self.sprite_sheet = pygame.image.load("soko.png")

        # Calculate the dimensions of the grid
        self.num_rows = self.sokoban_level.height
        self.num_cols = self.sokoban_level.width

        # Calculate the centering offset
        self.offset_x = (screen_width - (self.num_cols * 39)) // 2
        self.offset_y = (screen_height - (self.num_rows * 53)) // 2

        # Initialize the positions
        self.man = Man(self.sokoban_level.find_element("MAN"))
        self.boxes = Boxes(self.sokoban_level.find_elements("BOX"))
        self.target = Target(self.sokoban_level.find_elements("TARGET"))
        self.walls = Wall(self.sokoban_level.find_elements("WALL"))

        self.steps = 0

        # Main loop
        self.running = True

    def draw(self):
        self.target.draw(self.sprite_sheet, self.offset_x, self.offset_y)
        self.boxes.draw(self.sprite_sheet, self.offset_x, self.offset_y, self.target.positions)
        self.walls.draw(self.sprite_sheet, self.offset_x, self.offset_y)
        self.man.draw(self.sprite_sheet, self.offset_x, self.offset_y)

        # Add the step count at the bottom of the screen
        steps_font = pygame.font.Font(None, 36)
        steps_text = f"Steps: {self.steps}"
        steps_rendered_text = steps_font.render(steps_text, True, (255, 255, 255))
        steps_text_width, steps_text_height = steps_rendered_text.get_size()
        steps_text_position = (
            (screen_width - steps_text_width) // 2,
            screen_height - steps_text_height - 20,
        )
        screen.blit(steps_rendered_text, steps_text_position)

    def can_push_box(self, box_position, direction):
        # Calculate the position of the box if it's pushed in the given direction
        new_box_position = box_position.plus(direction)

        # Check if the new position is within the game boundaries
        if (
                0 <= new_box_position.line < self.num_cols
                and 0 <= new_box_position.col < self.num_rows
        ):
            # Check if the new position is a wall
            if new_box_position in self.walls.positions:
                return False

            # Check if there's another box in the new position
            if new_box_position in self.boxes.positions:
                return False

            return True

        return False

    def is_game_over(self):
        # Check if any box is stuck and not on a target
        for box_position in self.boxes.positions:
            if (
                box_position not in self.target.positions
                and not any(self.can_push_box(box_position, direction) for direction in [(1, 0), (-1, 0), (0, 1), (0, -1)])
            ):
                return True
        return False

    def check_win(self):
        return all(box in self.target.positions for box in self.boxes.positions)

    def move_man(self, direction):
        game.man.is_pushing = False
        future_position = self.man.pos.plus(direction)

        if self.manInLimiter(future_position, direction):
            if future_position in self.boxes.positions:
                # Check if the box can be pushed
                if self.can_push_box(future_position, direction):
                    # Move the box to its new position
                    box_index = self.boxes.positions.index(future_position)
                    self.boxes.positions[box_index] = future_position.plus(direction)
                    game.man.is_pushing = True

            # Move the player
            self.man.pos = future_position

            # Increment the step counter
            self.steps += 1

    def manInLimiter(self, futureposition, direction):
        box_position_if_moved = futureposition.plus(direction)

        if futureposition in game.boxes.positions:
            return box_position_if_moved not in game.walls.positions and box_position_if_moved not in game.boxes.positions
        else:
            return futureposition not in game.walls.positions

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.move_man((-1, 0))
                        game.man.set_Direction("up")
                    elif event.key == pygame.K_DOWN:
                        self.move_man((1, 0))
                        game.man.set_Direction("down")
                    elif event.key == pygame.K_LEFT:
                        self.move_man((0, -1))
                        game.man.set_Direction("left")
                    elif event.key == pygame.K_RIGHT:
                        self.move_man((0, 1))
                        game.man.set_Direction("right")
                    elif event.key == pygame.K_q:
                        self.running = False
                    elif event.key == pygame.K_r:  # Check for the 'R' key press
                        self.__init__()  # Reset the game


            # Clear the screen
            screen.fill((0, 0, 0))

            self.draw()

            if self.check_win():
                print("Congratulations! You've won!")
                print(self.steps)
                self.running = False

            if self.is_game_over():
                print("Game over! You cannot move any boxes.")
                self.running = False

            # Update the display
            pygame.display.flip()

        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
