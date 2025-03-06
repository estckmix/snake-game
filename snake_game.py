## ===========================================================================
## NAME:        snake_game.py 
## CREATED:     06-MAR-2025
## BY:          DAVID RADOICIC
## VERSION:     1.0
## DESCRIPTION: A classic snake game.
##
## ===========================================================================

import curses
import random
import time
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN

def main(stdscr):
    # Setup initial game state
    curses.curs_set(0)  # Hide cursor
    sh, sw = stdscr.getmaxyx()  # Get screen height and width
    w = curses.newwin(sh, sw, 0, 0)  # Create a new window
    w.keypad(1)  # Enable keypad
    w.timeout(100)  # Set timeout for getch to 100ms

    # Colors
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Snake color
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)    # Food color
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK) # Score color

    # Initial snake position (middle of the screen)
    snake_x = sw // 4
    snake_y = sh // 2
    snake = [
        [snake_y, snake_x],
        [snake_y, snake_x - 1],
        [snake_y, snake_x - 2]
    ]

    # Initial food position (random)
    food = [sh // 2, sw // 2]
    w.addch(food[0], food[1], curses.ACS_PI, curses.color_pair(2))

    # Initial direction
    key = KEY_RIGHT

    # Initial score
    score = 0

    # Display instructions at the beginning
    w.addstr(0, sw // 2 - 12, "SNAKE GAME", curses.color_pair(3) | curses.A_BOLD)
    w.addstr(1, sw // 2 - 14, "Use WASD or Arrows to move", curses.color_pair(3))
    w.addstr(2, sw // 2 - 9, "Press Q to quit", curses.color_pair(3))
    w.addstr(3, sh - 1, f"Score: {score}", curses.color_pair(3))
    w.refresh()
    time.sleep(2)

    # Game loop
    while True:
        # Get next key
        next_key = w.getch()

        # If no key pressed, keep current direction
        if next_key == -1:
            pass
        # If Q pressed, quit game
        elif next_key == ord('q') or next_key == ord('Q'):
            break
        # Set direction based on key
        else:
            # Map WASD to arrow keys
            if next_key == ord('w') or next_key == ord('W'):
                next_key = KEY_UP
            elif next_key == ord('a') or next_key == ord('A'):
                next_key = KEY_LEFT
            elif next_key == ord('s') or next_key == ord('S'):
                next_key = KEY_DOWN
            elif next_key == ord('d') or next_key == ord('D'):
                next_key = KEY_RIGHT

            # Ensure snake can't immediately reverse direction
            if (key == KEY_DOWN and next_key == KEY_UP) or \
            (key == KEY_UP and next_key == KEY_DOWN) or \
            (key == KEY_LEFT and next_key == KEY_RIGHT) or \
            (key == KEY_RIGHT and next_key == KEY_LEFT):
                pass
            else:
                key = next_key

        # Calculate new head position based on direction
        new_head = [snake[0][0], snake[0][1]]
        if key == KEY_DOWN:
            new_head[0] += 1
        elif key == KEY_UP:
            new_head[0] -= 1
        elif key == KEY_LEFT:
            new_head[1] -= 1
        elif key == KEY_RIGHT:
            new_head[1] += 1

        # Add new head to snake
        snake.insert(0, new_head)

        # Check if snake hit the border
        if (snake[0][0] in [0, sh-1] or 
            snake[0][1] in [0, sw-1] or 
            snake[0] in snake[1:]):
            game_over(w, score, sh, sw)
            break

        # Check if snake ate the food
        if snake[0] == food:
            score += 1
            # Generate new food in a location not occupied by snake
            while True:
                food = [random.randint(1, sh-2), random.randint(1, sw-2)]
                if food not in snake:
                    break
            w.addch(food[0], food[1], curses.ACS_PI, curses.color_pair(2))
        else:
            # Remove tail if food wasn't eaten
            tail = snake.pop()
            w.addch(tail[0], tail[1], ' ')

        # Update score display
        w.addstr(3, sw - 15, f"Score: {score}", curses.color_pair(3))

        # Draw snake's head (and body)
        for i, point in enumerate(snake):
            if i == 0:  # Head
                w.addch(point[0], point[1], curses.ACS_CKBOARD, curses.color_pair(1))
            else:  # Body
                w.addch(point[0], point[1], curses.ACS_BLOCK, curses.color_pair(1))


def game_over(w, score, sh, sw):
    """Display game over screen"""
    w.clear()
    msg = "GAME OVER!"
    w.addstr(sh // 2 - 2, (sw - len(msg)) // 2, msg, curses.color_pair(2) | curses.A_BOLD)
    
    score_msg = f"Final Score: {score}"
    w.addstr(sh // 2, (sw - len(score_msg)) // 2, score_msg, curses.color_pair(3) | curses.A_BOLD)
    
    exit_msg = "Press any key to exit..."
    w.addstr(sh // 2 + 2, (sw - len(exit_msg)) // 2, exit_msg)
    
    w.refresh()
    w.getch()


if __name__ == "__main__":
    try:
        # Initialize curses
        curses.wrapper(main)
    except KeyboardInterrupt:
        pass
    finally:
        # Clean up and exit
        curses.endwin()
        print("Thanks for playing Snake!")

