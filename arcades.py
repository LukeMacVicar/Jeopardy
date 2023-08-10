import arcade

# Constants for the grid dimensions and padding
GRID_ROWS = 6
GRID_COLS = 6
PADDING = 5

# Category labels for the top row
CATEGORIES = ["Category 1", "Category 2", "Category 3", "Category 4", "Category 5", "Category 6"]

# Dollar values for the bottom 5 rows
DOLLAR_VALUES = ["$100", "$200", "$300", "$400", "$500"]

class Button(arcade.Sprite):
    def __init__(self, row, col, text):
        super().__init__()
        self.row = row
        self.col = col
        self.text = text
        self.width = 100
        self.height = 100
        self.center_x = col * (self.width + PADDING)
        self.center_y = row * (self.height + PADDING)

    def draw(self):
        arcade.draw_rectangle_filled(self.center_x, self.center_y, self.width, self.height, arcade.color.BLUE)
        arcade.draw_rectangle_outline(self.center_x, self.center_y, self.width, self.height, arcade.color.BLACK)

class GridDrawer(arcade.View):
    def __init__(self):
        super().__init__()

        self.button_list = None

    def setup(self):
        arcade.set_background_color(arcade.color.WHITE)
        def on_draw(self):
            arcade.start_render()

            # Draw the buttons
            self.button_list.draw()

            # Draw labels on top of buttons
            for button in self.button_list:
                arcade.draw_text(button.text, button.center_x, button.center_y,
                                 arcade.color.BLACK, font_size=12, anchor_x="center", anchor_y="center")

        # Create the button list
        self.button_list = arcade.SpriteList()

        # Add category labels to the top row
        for col, category in enumerate(CATEGORIES):
            button = Button(GRID_ROWS, col, category)
            self.button_list.append(button)

        # Add buttons for the grid
        for row in range(GRID_ROWS - 1):
            for col in range(GRID_COLS):
                button = Button(row, col, DOLLAR_VALUES[row])
                self.button_list.append(button)

    def on_draw(self):
        arcade.start_render()
        self.button_list.draw()

        # Draw labels on top of buttons
        for button in self.button_list:
            arcade.draw_text(button.text, button.center_x, button.center_y,
                             arcade.color.BLACK, font_size=12, anchor_x="center", anchor_y="center")

    def on_resize(self, width, height):
        arcade.View.on_resize(self, width, height)

        # Recalculate the button positions and sizes
        for button in self.button_list:
            button.center_x = (button.col + 0.5) * (width / GRID_COLS)
            button.center_y = (GRID_ROWS - 1 - button.row + 0.5) * (height / GRID_ROWS)
            button.width = width / GRID_COLS - PADDING
            button.height = height / GRID_ROWS - PADDING

    def on_mouse_press(self, x, y, button, key_modifiers):
        # Check if a button was clicked
        for button in self.button_list:
            if button.collides_with_point((x, y)):
                if button.row != GRID_ROWS - 1:
                    value = DOLLAR_VALUES[button.row]
                    text_screen = TextScreen(value)
                    self.window.show_view(text_screen)
                    break


class TextScreen(arcade.View):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text(self.value, 400, 300, arcade.color.BLACK, font_size=36, anchor_x="center", anchor_y="center")
        arcade.draw_text("Press any key to go back", 400, 200, arcade.color.BLACK, font_size=18, anchor_x="center", anchor_y="center")

    def on_key_press(self, symbol, modifiers):
        grid_drawer = GridDrawer()
        self.window.show_view(grid_drawer)
        grid_drawer.setup()


def main():
    window = arcade.Window(800, 600, "6x6 Grid of Buttons with Categories in Arcade", resizable=True)
    grid_drawer = GridDrawer()
    window.show_view(grid_drawer)
    grid_drawer.setup()
    arcade.run()


if __name__ == "__main__":
    main()