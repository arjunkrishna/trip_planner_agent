from crewai import Crew
from trip_agents import TripAgents
from trip_tasks import TripTasks
import streamlit as st
import datetime
import schema

st.set_page_config(page_icon="✈️", layout="wide")

def icon(emoji: str):
    """Shows an emoji as a Notion-style page icon."""
    st.write(
        f'<span style="font-size: 78px; line-height: 1">{emoji}</span>',
        unsafe_allow_html=True,
    )  

class HomePage:
    def display(self):
        st.header("Welcome to the Home Page!")
        # Add more content here

class PlanTripPage:
    def __init__(self):
        self.location = None
        self.cities = None
        self.date_range = None
        self.interests = None
        self.submitted = None

    def display_form(self):
        with st.sidebar:
            st.header("👇 Enter your trip details")
            with st.form("my_form"):
                self.location = st.text_input("Where are you currently located?", placeholder="San Mateo, CA")
                self.cities = st.text_input("City and country are you interested in vacationing at?", placeholder="Bali, Indonesia")
                self.date_range = self.get_date_range_input()
                self.interests = st.text_area("High level interests and hobbies or extra details about your trip?", placeholder="2 adults who love swimming, dancing, hiking, and eating")
                self.submitted = st.form_submit_button("Submit")

    def get_date_range_input(self):
        today = datetime.datetime.now().date()
        next_year = today.year + 1
        jan_16_next_year = datetime.date(next_year, 1, 10)
        return st.date_input("Date range you are interested in traveling?", min_value=today, value=(today, jan_16_next_year + datetime.timedelta(days=6)), format="MM/DD/YYYY")

    def process_data(self):
        if self.submitted:
            self.run_trip_crew()

    def run_trip_crew(self):
        with st.status("🤖 **Agents at work...**", state="running", expanded=True) as status:
            with st.container(height=500, border=False):
                trip_crew = TripCrew(self.location, self.cities, self.date_range, self.interests)
                result = trip_crew.run()
            status.update(label="✅ Trip Plan Ready!", state="complete", expanded=False)

        st.subheader("Here is your Trip Plan", anchor=False, divider="rainbow")
        trip_crew.display_result(result)   
            

    def display(self):
        icon("🏖️ VacAIgent")
        st.subheader("Let AI agents plan your next vacation!", divider="rainbow", anchor=False)
        self.display_form()
        self.process_data()

class AboutPage:
    def display(self):
        st.header("About Page!")
        # Add content for About page here

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