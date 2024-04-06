from crewai import Crew
from features.trip.trip_agents import TripAgents
from features.trip.trip_tasks import TripTasks
import streamlit as st
import datetime
import schema
from features.trip.trip_details import TripDetails
from features.trip.trip_crew import TripCrew
from home_page import HomePage


# Constants
LOCATION_PLACEHOLDER = "San Mateo, CA"
CITIES_PLACEHOLDER = "Bali, Indonesia"

class PlanTripPage:
    def __init__(self):
        self.trip_details = TripDetails()

    def display_form(self):
        with st.sidebar:
            st.header("👇 Enter your trip details")
            with st.form("my_form"):
                self.get_location_input()
                self.get_cities_input()
                self.get_date_range_input()
                self.get_interests_input()
                self.get_submit_button()

    def get_location_input(self):
        self.trip_details.location = st.text_input("Where are you currently located?", placeholder=LOCATION_PLACEHOLDER)

    def get_cities_input(self):
        self.trip_details.cities = st.text_input("City and country are you interested in vacationing at?", placeholder=CITIES_PLACEHOLDER)

    def get_date_range_input(self):
        today = datetime.datetime.now().date()
        next_year = today.year + 1
        jan_16_next_year = datetime.date(next_year, 1, 10)
        self.trip_details.date_range = st.date_input("Date range you are interested in traveling?", min_value=today, value=(today, jan_16_next_year + datetime.timedelta(days=6)), format="MM/DD/YYYY")

    def get_interests_input(self):
        self.trip_details.interests = st.text_area("High level interests and hobbies or extra details about your trip?", placeholder="2 adults who love swimming, dancing, hiking, and eating")

    def get_submit_button(self):
        self.trip_details.submitted = st.form_submit_button("Submit")

    def process_data(self):
        if self.trip_details.submitted:
            self.run_trip_crew()

    def run_trip_crew(self):
        with st.status("🤖 **Agents at work...**", state="running", expanded=True) as status:
            with st.container(height=500, border=False):
                trip_crew = TripCrew(self.trip_details.location, self.trip_details.cities, self.trip_details.date_range, self.trip_details.interests)
                result = trip_crew.run()
            status.update(label="✅ Trip Plan Ready!", state="complete", expanded=False)

        st.subheader("Here is your Trip Plan", anchor=False, divider="rainbow")
        trip_crew.display_result(result)   
            

    def display(self):
        HomePage.icon("🏖️ VacAIgent")
        st.subheader("Let AI agents plan your next vacation!", divider="rainbow", anchor=False)
        self.display_form()
        self.process_data()

