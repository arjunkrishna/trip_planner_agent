import streamlit as st

class HomePage:
    @staticmethod
    def icon(emoji: str):
        """Shows an emoji as a Notion-style page icon."""
        st.write(
            f'<span style="font-size: 78px; line-height: 1">{emoji}</span>',
            unsafe_allow_html=True,
        )

    def display(self):
        st.header("Welcome to the Home Page!")
        # Add more content here