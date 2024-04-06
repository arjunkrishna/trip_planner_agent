from crewai import Crew
from trip_agents import TripAgents
from trip_tasks import TripTasks
import streamlit as st
import datetime
import schema
from dataclasses import dataclass
from trip_details import TripDetails
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

class TripCrew:

    def __init__(self, origin, cities, date_range, interests):
        self.cities = cities
        self.origin = origin
        self.interests = interests
        self.date_range = date_range
        self.output_placeholder = st.empty()

    def run(self):
        agents = TripAgents()
        tasks = TripTasks()

        city_selector_agent = agents.city_selection_agent()
        local_expert_agent = agents.local_expert()
        travel_concierge_agent = agents.travel_concierge()

        identify_task = tasks.identify_task(
            city_selector_agent,
            self.origin,
            self.cities,
            self.interests,
            self.date_range
        )

        gather_task = tasks.gather_task(
            local_expert_agent,
            self.origin,
            self.interests,
            self.date_range
        )

        plan_task = tasks.plan_task(
            travel_concierge_agent,
            self.origin,
            self.interests,
            self.date_range
        )

        crew = Crew(
            agents=[
                city_selector_agent, local_expert_agent, travel_concierge_agent
            ],
            tasks=[identify_task, gather_task, plan_task],
            verbose=True
        )

        result = crew.kickoff()
        return result

    def display_result(self, result):
        self.output_placeholder.markdown(result)        