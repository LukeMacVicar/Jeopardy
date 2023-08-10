import pygame
import mysql.connector
import random

# Constants for the grid
GRID_WIDTH = 6
GRID_HEIGHT = 6
RECT_WIDTH_RATIO = 0.16 # Ratio of the screen width for the rectangle width
RECT_HEIGHT_RATIO = 0.142  # Ratio of the screen height for the rectangle height
GRID_SPACING = 5
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Calculate the rectangle dimensions based on the screen size
RECT_WIDTH = int(SCREEN_WIDTH * RECT_WIDTH_RATIO)
RECT_HEIGHT = int(SCREEN_HEIGHT * RECT_HEIGHT_RATIO)
# Colors
BLUE = (6, 12, 233)
YELLOW = (255, 204, 0)
BORDER_COLOR = (50, 50, 50)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def conn_mysql():
    # Connect to the MySQL database
    num = 4977
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="sys"
        )

    except mysql.connector.Error as e:
        print("Error connecting to MySQL:", e)
        exit(1)

    try:
        cursor = conn.cursor()
        cursor.execute(f"SELECT Category, Question, Answer, Value FROM game_show WHERE ShowNumber = {num}")
        rows = cursor.fetchall()

    except mysql.connector.Error as e:
        print("Error executing the query:", e)
        cursor.close()
        conn.close()
        exit(1)

    cursor.close()
    conn.close()

    return rows

class fonts():
    def __init__(self):
        pygame.font.init()

    def custom_font(text, size, color):
        font_path = "/Users/lukemacvicar/Desktop/THIS_IS_JEOPARDY!/KorinnaStd-Bold.otf"
        custom_font = pygame.font.Font(font_path, size)
        value_text = custom_font.render(text, True, color)
        return value_text

def split_string_on_nth_space(input_string, spaces, splits):
    words = input_string.split(" ")
    ##print("WORDS:  ", words)
    n = int(spaces / splits)
    if n <= 0 or n > len(words):
        return None
    
    parts = []
    counter = 0
    for n in range(len(words)):
        part = " ".join(words[:n])
        if part != '':
            parts.append(part)
            words = words[n:]
        counter += 1
    #print("Space: ", spaces)
    #print("Splits: ", splits)
    #print("N: ", n)
    #print("Counter: ",counter) 
    parts.append(" ".join(words))
    #print("Parts: ", parts)
    return parts

def resize_text(text_width, text_height, box_width, box_height, font_size, text, color):
    while True:
        if text_width <= box_width and text_height <= box_height:
            #print("Text: ", text)
            text = [text]
            return text; 

        if font_size < 19:
            #print("Text: ", text)
            spaces = text.count(" ")
            div = int(text_width/box_width)
            #print("Spaces: ", spaces)
            parts = []
            parts = split_string_on_nth_space(text, spaces, div)
            #print("Text Width: ", text_width, "     Rect Width: ", RECT_WIDTH, "     Font Size: ", font_size)
            return parts

        # Reduce font size
        font_size -= 1
        value_text = fonts.custom_font(text, font_size, color)
        text_rect = value_text.get_rect()
        text_width = text_rect.width
        text_height = text_rect.height

def draw_grid(screen, fonts, rows):
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            values = ["","$200","$400","$600","$800","$1000"]
            category, question, answer, value = rows[row]
            # Calculate the position of the rectangle inside the border
            x = col * (RECT_WIDTH + GRID_SPACING) 
            y = row * (RECT_HEIGHT + GRID_SPACING)

            # Draw the rectangle
            pygame.draw.rect(screen, BLUE, (x + 4, y + 55, RECT_WIDTH, RECT_HEIGHT))
            dollar_text = fonts.custom_font(values[row], 36, YELLOW)
            screen.blit(dollar_text, (x + 25, y + 75))

        font_size = 24
        categories_text = fonts.custom_font(category, font_size, WHITE)
        text_rect = categories_text.get_rect()
        text_width = text_rect.width
        text_height = text_rect.height
        #RESIZE AND BREAK INTO N PIECES
        if text_width > RECT_WIDTH:
            parts = []
            x = 0
            parts = resize_text(text_width, text_height, RECT_WIDTH, RECT_HEIGHT,font_size, category, WHITE)
            #print("Len Parts: ",len(parts),"    Parts: ", parts)
            if len(parts) > 1:
                while x < len(parts):
                    categories_text = fonts.custom_font(parts[x], 18, WHITE)
                    text_rect = categories_text.get_rect()
                    text_width = text_rect.width
                    screen.blit(categories_text, (((RECT_WIDTH + GRID_SPACING) * row) + GRID_SPACING + 15,(x * 25) + 65))
                    x += 1
            else:
                categories_text = fonts.custom_font(category, 18, WHITE)
                screen.blit(categories_text, (((RECT_WIDTH + GRID_SPACING) * row) + GRID_SPACING + 15, 75))

        else:
            #DO NOT BREAK
            screen.blit(categories_text, (((RECT_WIDTH + GRID_SPACING) * row) + GRID_SPACING + 15, 75))

def main_menu(screen, fonts):
    menu_done = False
    while not menu_done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 300 <= x <= 500 and 300 <= y <= 350:
                    # Rectangle grid option selected
                    menu_done = True

        screen.fill(BLUE)

        # Draw the menu options
        menu_text = fonts.custom_font("THIS IS JEOPARDY!", 76, YELLOW)
        screen.blit(menu_text, (100, 100))

        start_text = fonts.custom_font("START GAME", 36, WHITE)
        screen.blit(start_text, (300, 300))

        pygame.display.flip()

def single_jeopardy(screen, fonts, rows):
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the mouse click is inside any rectangle
                x, y = event.pos
                for row in range(GRID_HEIGHT):
                    for col in range(GRID_WIDTH):
                        if row != 0:
                            rect_x = col * (RECT_WIDTH + GRID_SPACING)
                            rect_y = row * (RECT_HEIGHT + GRID_SPACING)
                            if rect_x <= x <= rect_x + RECT_WIDTH and rect_y + 55 <= y <= rect_y + RECT_HEIGHT + 55:
                                # Rectangle clicked, perform your action here
                                print(f"Clicked on rectangle at row {row}, column {col}")
                                display_question(screen, fonts, rows, row-1, col)

        screen.fill(BLACK)

        # Draw the grid of rectangles with a border
        draw_grid(screen, fonts, rows)

        pygame.display.flip()

def display_question(screen, fonts, rows, val, cat):
    menu_done = False
    while not menu_done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 300 <= x <= 500 and 300 <= y <= 350:
                    # Rectangle grid option selected
                    menu_done = True

        screen.fill(BLUE)

        question = []
        for i in range(31):
            if((i % 6) == cat):
                question.append(rows[i][1])
        # Draw the menu options
        menu_text = fonts.custom_font(question[val], 36, WHITE)
        text_rect = menu_text.get_rect()
        text_width = text_rect.width
        text_height = text_rect.height
        #RESIZE AND BREAK INTO N PIECES
        parts = []
        if text_width > 600:
            parts = resize_text(text_width, text_height, 600, 600, 36, question[val], WHITE)
            if len(parts) > 1:
                x = 0
                while x < len(parts):
                    menu_text = fonts.custom_font(parts[x], 24, WHITE)
                    text_rect = menu_text.get_rect()
                    text_width = text_rect.width
                    screen.blit(menu_text, (30, 100 + (x * 30)))
                    x += 1
            else:
                categories_text = fonts.custom_font(question[val], 36, WHITE)
                screen.blit(menu_text, (30, 100))
        #setup picture capabilities
        pygame.display.flip()

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("KA-CHOW!")

    rows = conn_mysql()

    for i in range(len(rows)):
        category, question, answer, value = rows[i]

    main_menu(screen, fonts)

    single_jeopardy(screen, fonts, rows)

    pygame.quit()

if __name__ == "__main__":
    main()