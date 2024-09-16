import streamlit as st

st.page_link('hello.py', label='Go back', icon='↩️')
        
# Title and Subtitle
st.title("Welcome to the Ultimate Challenge Game! 🎮")

# Collecting user input
name = st.text_input("Enter your Name:")
company = st.text_input("Enter your Company:")
contact = st.text_input("Contact (Optional):")

# Instructions
st.markdown("""
### Game Instructions
1. **Three Challenges Ahead**: You will face three exciting challenges.
2. **Scoring**: Try to get the maximum points! You can attempt each challenge as many times as you want.
3. **Time Matters**: The faster you complete the challenges, the more points you will earn. Don't take too long!
""")

# Button to start the game
#if st.button("Start Game"):
if name and company:
    st.success(f"Click the button below to start the game. Good luck, {name} from {company}!")
    disabled = False  
else:
    st.error("Please enter both your name and company to start the game.")
    disabled = True
st.page_link('pages/game.py', label='START', icon='🚀', use_container_width=True, disabled=disabled)
    