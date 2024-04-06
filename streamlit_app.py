import streamlit as st

from home_page import HomePage
from plan_trip_page import PlanTripPage

st.set_page_config(page_icon="✈️", layout="wide")



class AboutPage:
    def display(self):
        st.header("About Page!")
        # Add content for About page here

if __name__ == "__main__":
    # Define the pages
    pages = {
        "Home": HomePage(),
        "Plan Trip": PlanTripPage(),
        "About": AboutPage()
    }

    # Create a sidebar selectbox for navigation
    selected_page = st.sidebar.selectbox("Navigate", list(pages.keys()))

    # Display the selected page
    pages[selected_page].display()