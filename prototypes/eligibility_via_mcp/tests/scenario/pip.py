from typing import Literal
from tests.scenario.runner import run_scenario

class PipScenario():
    short_scenario_description: str
    should_user_be_eligible: bool
    decision_addendum: str | None
    user_intro: str
    continue_with_check_answer: bool = True

    age_answer: None | Literal["68+", "18 to 67", "17-"] = None
    residence_country_answer: None | Literal["Yes", "No"] = None
    residence_country_timeframe_answer: None | Literal["Yes", "No"] = None
    health_condition_time_answer: None | Literal["Yes", "No"] = None
    health_condition_tasks_term_clarification: list[str] | None = None
    health_condition_tasks_answer: None | Literal["Yes", "No"] | None = None
    health_condition_tasks_qualification_term_clarification: list[str] | None = None
    health_condition_tasks_qualification_answer: None | Literal["Yes", "No"] | None = None

    def __init__(self, short_description: str, user_intro: str, user_should_be_eligible: bool, decision_addendum: str | None = None) -> None:
        self.short_scenario_description = short_description
        self.user_intro = user_intro
        self.should_user_be_eligible = user_should_be_eligible
        self.decision_addendum = decision_addendum

    def how_old_are_you(self, value: Literal["68+", "18 to 67", "17-"]) -> PipScenario:
        self.age_answer = value
        return self
    
    def do_you_live_in_England_or_Wales(self, value: Literal["Yes", "No"]) -> PipScenario:
        self.residence_country_answer = value
        return self

    def have_you_lived_in_the_UK_for_at_least_2_of_last_3_years(self, value: Literal["Yes", "No"]) -> PipScenario:
        self.residence_country_timeframe_answer = value
        return self

    def have_you_had_a_health_condition_for_3_months_or_more_and_is_it_expected_to_continue_for_more_than_9_months_or_are_you_not_expected_to_live_more_than_12_months(self, value: Literal["Yes", "No"]) -> PipScenario:
        self.health_condition_time_answer = value
        return self
    
    def clarify_health_condition_tasks_terms(self) -> PipScenario:
        self.health_condition_tasks_term_clarification = [
            "What is meant by 'needing help'?",
            "What is meant by 'preparing and eating'?",
            "What is meant by 'hygiene'?",
            "What is meant by 'dressing'?",
            "What is meant by 'managing health'?",
            "What is meant by 'communication'?",
            "What is meant by 'socializing'?",
            "What is meant by 'finances'?",
            "What is meant by 'planning a journey'?",
            "What is meant by 'moving around'?"
        ]
        return self
    
    def do_you_need_help_or_struggle_with_any_of_the_following_tasks_for_over_half_of_any_given_day(self, value: Literal["Yes", "No"]) -> PipScenario:
        self.health_condition_tasks_answer = value
        return self

    def clarify_health_condition_tasks_qualification_terms(self) -> PipScenario:
        self.health_condition_tasks_qualification_term_clarification = [
            "What is meant by 'safety'?",
            "What is meant by 'time'?",
            "What is meant by 'frequency'?",
            "What is meant by 'standard'?",
        ]
        return self

    def with_respect_to_those_tasks_do_any_of_the_following_apply(self, value: Literal["Yes", "No"]) -> PipScenario:
        self.health_condition_tasks_qualification_answer = value
        return self

    async def run(self):

        # Build user inputs
        user_inputs: list[str | None] = [
            self.user_intro, 
            "yes, continue with check",
            self.age_answer,
            self.residence_country_answer,
            self.residence_country_timeframe_answer,
            self.health_condition_time_answer,
            self.health_condition_tasks_answer,
            self.health_condition_tasks_qualification_answer
        ]

        # Build criteria
        all_criteria = [
            "The agent should identify that personal independence payments is the most suitable eligibility to check, and ask the user if they want to proceed" ,
            """
                When starting the eligibility check, the agent should ask the user's age, and offer 3 options:
                - 68+ 
                - 18 to 67
                - 17-
            """,
            """
            After the user answers with their age, the agent should ask if the user lives in England or Wales, and offer 2 options:
            - Yes
            - No
            """,
            """
                After the user answers with their country of residence, the agent should ask the user if they've lived in the UK 
                for at least 2 of the last 3 years, and offer 2 options: 
                - Yes
                - No
            """,
            """
                After the user answers how long they've lived in the UK, the agent should ask the user if:
                1. They've had a health condition for at least 3 months that they expect to continue for at least another 9
                2. Not expected to live more than 12 months
                The agent should offer 2 options:
                - Yes
                - No
            """,
            """
                After the user answers the question about health condition time, the agent should ask the user if they need help or 
                struggle with any of the following:
                - Preparing & Eating 
                - Hygiene
                - Dressing
                - Managing Health
                - Communication
                - Socializing
                - Finances
                - Planning a Journey
                - Moving Around
            """,
            "The agent should offer the following definition for 'needing help' when asked: 'Only being able to do a task by using an aid (like a grab rail, a walking stick, or a dossette box for pills) counts.'",
            "The agent should offer the following definition for 'Preparing & Eating' when asked: 'cooking a simple meal, cutting up food, or being reminded to eat'",
            "The agent should offer the following definition for 'Hygiene' when asked: 'washing, bathing, or using the toilet'",
            "The agent should offer the following definition for 'Dressing' when asked: 'putting on or taking off clothes'",
            "The agent should offer the following definition for 'Managing Health' when asked: 'managing medication, monitoring a health condition, or using medical equipment'",
            "The agent should offer the following definition for 'Communication' when asked: 'speaking to others, hearing/understanding what is being said, or reading basic information'",
            "The agent should offer the following definition for 'Socializing' when asked: 'difficulty being around other people, or interacting with them'",
            "The agent should offer the following definition for 'Finances' when asked: 'managing money or making decisions about spending'",
            "The agent should offer the following definition for 'Planning a Journey' when asked: 'planning or following a route because of a mental health condition, sensory impairment, or learning disability e.g., getting overwhelmed or lost'",
            "The agent should offer the following definition for 'Moving Around' when asked: 'physical difficulty walking e.g., you are only able to walk a short distance (20 or 50 meters), before needing to stop'",
            """
                After the user answers about their struggles with tasks, the agent should ask whether any of the following apply to the tasks they struggle with:
                - Safety
                - Time
                - Frequency
                - Standard
            """,
            "The agent should offer the following definition for 'Safety' when asked: 'you can't do the task without putting yourself or others at risk'",
            "The agent should offer the following definition for 'Time' when asked: 'it takes you much longer (more than twice as long) than it would take a person without your condition'",
            "The agent should offer the following definition for 'Frequency' when asked: 'you can't do it as often as you need to throughout the day'",
            "The agent should offer the following definition for 'Standard' when asked: 'you can't do it to an acceptable standard'",
        ]

        user_eligibility_str: str = "eligible" if self.should_user_be_eligible else "ineligible"
        final_criteria = all_criteria[:len(user_inputs) - 1] + \
            [f"Finally, the agent should tell the user that they are {user_eligibility_str}, {self.decision_addendum + ", " if self.decision_addendum else ""} and the conversation should conclude."]

        await run_scenario(
            scenario_name=f"Personal Independence Payments ({self.short_scenario_description})",
            scenario_description="The user's situation indicates that personal independence payments would be an appropriate benefit, " \
                "so they should be taken through a personsal independence payment eligibility check. The agent should " \
                f"determine that the user is {user_eligibility_str}.",
            judge_criteria=final_criteria,
            user_inputs=[item for item in user_inputs if item is not None]
        )