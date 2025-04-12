import streamlit as st
import random

def main():
    st.title("🤫 Guess the Number!")
    st.write("I'm thinking of a number between 1 and 100. Can you guess it?")

    if 'secret_number' not in st.session_state:
        st.session_state['secret_number'] = random.randint(1, 100)
        st.session_state['attempts'] = 0
        st.session_state['game_over'] = False

    if st.session_state['game_over']:
        st.success(f"🎉 You guessed it! The number was {st.session_state['secret_number']} in {st.session_state['attempts']} attempts.")
        if st.button("Play Again?"):
            st.session_state['secret_number'] = random.randint(1, 100)
            st.session_state['attempts'] = 0
            st.session_state['game_over'] = False
            st.rerun()
        return

    guess = st.number_input("Enter your guess:", min_value=1, max_value=100, step=1)

    if st.button("Submit Guess"):
        st.session_state['attempts'] += 1
        if guess < st.session_state['secret_number']:
            st.warning("Too low! Try again.")
        elif guess > st.session_state['secret_number']:
            st.warning("Too high! Try again.")
        else:
            st.session_state['game_over'] = True
            st.rerun()

if __name__ == "__main__":
    main()
