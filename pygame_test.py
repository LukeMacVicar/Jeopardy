import pygame
import sys

# Pygame initialization
pygame.init()

# Constants for the window size
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set up the window
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Trivia Game")

# Font
font = pygame.font.Font(None, 36)

# Trivia question and answer
question = "What is the capital of France?"
correct_answer = "paris"

def game_loop():
    running = True
    user_answer = ""
    correct = None

    while running:
        window.fill(WHITE)

        # Display the question
        question_text = font.render(question, True, BLACK)
        window.blit(question_text, (50, 100))

        # Display the user's input and check if it matches the correct answer
        user_text = font.render("Your answer: " + user_answer, True, BLACK)
        window.blit(user_text, (50, 200))

        if correct is not None:
            result_text = font.render(correct, True, BLACK)
            window.blit(result_text, (50, 300))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # Check if the user's answer is correct
                    if user_answer.lower() == correct_answer:
                        correct = "Correct answer!"
                    else:
                        correct = "Incorrect answer!"
                elif event.key == pygame.K_BACKSPACE:
                    # Remove the last character from the user's answer
                    user_answer = user_answer[:-1]
                else:
                    # Add the pressed key to the user's answer
                    user_answer += event.unicode

        pygame.display.update()

# Start the game loop
game_loop()

# Quit the game
pygame.quit()
sys.exit()