import streamlit as st
import random
import time

def main():
    st.title("Snake Game")
    st.write("Use the buttons to control the snake!")

    # Initialize game state
    if 'snake' not in st.session_state:
        st.session_state.snake = [(5, 5)]  # Initial snake position
        st.session_state.food = (10, 10)  # Initial food position
        st.session_state.direction = 'right'  # Initial direction
        st.session_state.score = 0
        st.session_state.game_over = False
        st.session_state.paused = True # Start paused initially
        st.session_state.message = "Press Start to Play"

    # --- Helper Functions ---

    def display_game():
        """
        Displays the game board, snake, and food using Streamlit elements.
        """
        # Create a placeholder for the game board.  This will be updated
        # in each iteration of the game.  Using a placeholder avoids
        # having the board "flicker" as it is redrawn.
        if 'game_board_placeholder' not in st.session_state:
            st.session_state.game_board_placeholder = st.empty()

        # Calculate the size of the game board based on the number of rows
        # and columns, with a maximum size of 500x500.
        board_width = 20  # Number of columns
        board_height = 20  # Number of rows
        max_board_size = 500
        cell_size = int(min(max_board_size / board_width, max_board_size / board_height))

        # Create an empty game board
        board = [[' ' for _ in range(board_width)] for _ in range(board_height)]

        # Place the snake on the board
        for x, y in st.session_state.snake:
            if 0 <= y < board_height and 0 <= x < board_width: #check within bounds
                board[y][x] = 'S'

        # Place the food on the board
        if 0 <= st.session_state.food[1] < board_height and 0 <= st.session_state.food[0] < board_width: #check within bounds
            board[st.session_state.food[1]][st.session_state.food[0]] = 'F'

        # Display the board using st.text.  We use st.text because it
        # handles monospacing correctly, which is essential for
        # displaying a grid.  We use a placeholder to update the board
        # without adding new elements to the Streamlit app.
        game_board_string = ""
        for row in board:
            game_board_string += ''.join(row) + '\n'
        st.session_state.game_board_placeholder.text(game_board_string)

        # Display the score
        st.write(f"Score: {st.session_state.score}")
        st.write(st.session_state.message) #display messages

    def generate_food():
        """Generates a new random position for the food."""
        board_width = 20
        board_height = 20
        while True:
            x = random.randint(0, board_width - 1)
            y = random.randint(0, board_height - 1)
            if (x, y) not in st.session_state.snake:
                break
        st.session_state.food = (x, y)

    def move_snake():
        """Moves the snake in the current direction."""
        if st.session_state.game_over or st.session_state.paused:
            return

        head_x, head_y = st.session_state.snake[0]
        board_width = 20
        board_height = 20

        if st.session_state.direction == 'up':
            new_head = (head_x, head_y - 1)
        elif st.session_state.direction == 'down':
            new_head = (head_x, head_y + 1)
        elif st.session_state.direction == 'left':
            new_head = (head_x - 1, head_y)
        elif st.session_state.direction == 'right':
            new_head = (head_x + 1, head_y)

        # Game over if snake hits a wall
        if (
            new_head[0] < 0
            or new_head[0] >= board_width
            or new_head[1] < 0
            or new_head[1] >= board_height
        ):
            st.session_state.game_over = True
            st.session_state.message = "Game Over - Hit Wall!"
            return

        # Game over if snake hits itself
        if new_head in st.session_state.snake[1:]:
            st.session_state.game_over = True
            st.session_state.message = "Game Over - Hit Self!"
            return

        st.session_state.snake.insert(0, new_head)

        # Eat food
        if new_head == st.session_state.food:
            st.session_state.score += 1
            generate_food()
        else:
            st.session_state.snake.pop()

    def game_loop():
        """Main game loop, called every interval."""
        if not st.session_state.game_over and not st.session_state.paused:
            move_snake()
            display_game()
            # Rerun the script after a delay to update the game state.
            time.sleep(0.5)  # Adjust for game speed
            st.rerun()

    # --- Button Handlers ---
    def button_start():
        """Starts or resumes the game."""
        if st.session_state.paused or st.session_state.game_over:
            st.session_state.paused = False
            st.session_state.game_over = False #reset
            st.session_state.snake = [(5,5)]
            st.session_state.direction = 'right'
            st.session_state.score = 0
            generate_food()
            st.session_state.message = "Game Started!"
            st.rerun()  # Force a rerun to start the game loop
        else:
            st.session_state.message = "Game Resumed!"

    def button_pause():
        """Pauses the game."""
        if not st.session_state.paused and not st.session_state.game_over:
            st.session_state.paused = True
            st.session_state.message = "Game Paused!"

    def button_up():
        """Sets snake direction to up."""
        if st.session_state.direction != 'down' and not st.session_state.paused:
            st.session_state.direction = 'up'
    def button_down():
        """Sets snake direction to down."""
        if st.session_state.direction != 'up' and not st.session_state.paused:
            st.session_state.direction = 'down'
    def button_left():
        """Sets snake direction to left."""
        if st.session_state.direction != 'right' and not st.session_state.paused:
            st.session_state.direction = 'left'
    def button_right():
        """Sets snake direction to right."""
        if st.session_state.direction != 'left' and not st.session_state.paused:
            st.session_state.direction = 'right'

    # --- UI ---
    col1, col2, col3 = st.columns(3)
    col2.button("Start", on_click=button_start)
    col2.button("Pause", on_click=button_pause)

    st.button("↑", on_click=button_up)
    st.button("↓", on_click=button_down)
    col1, col2, col3 = st.columns(3)
    col1.button("←", on_click=button_left)
    col3.button("→", on_click=button_right)

    display_game() #show the board

    game_loop() #start the loop

if __name__ == "__main__":
    main()

