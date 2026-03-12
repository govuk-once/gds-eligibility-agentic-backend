from tests.scenario.base import BaseScenario

class PipScenario(BaseScenario):

    def _get_eligibility_name(self) -> str:
        return "Personal Independence Payments"

    def how_old_are_you(self, value: str) -> PipScenario:
        self._add_user_input(value=value)
        self._add_judge_criteria(value="""
            When starting the eligibility check, the agent should ask the user's age, and offer 3 options:
            - 68+ 
            - 18 to 67
            - 17-
        """)
        return self
    
    def do_you_live_in_England_or_Wales(self, value: str) -> PipScenario:
        self._add_user_input(value=value)
        self._add_judge_criteria(value="""
            After the user answers with their age, the agent should ask if the user lives in England or Wales, and offer 2 options:
            - Yes
            - No
        """)
        return self

    def have_you_lived_in_the_UK_for_at_least_2_of_last_3_years(self, value: str) -> PipScenario:
        self._add_user_input(value=value)
        self._add_judge_criteria(value="""
            After the user answers with their country of residence, the agent should ask the user if they've lived in the UK 
            for at least 2 of the last 3 years, and offer 2 options: 
            - Yes
            - No
        """)
        return self

    def have_you_had_a_health_condition_for_3_months_or_more_and_is_it_expected_to_continue_for_more_than_9_months_or_are_you_not_expected_to_live_more_than_12_months(self, value: str) -> PipScenario:
        self._add_user_input(value=value)
        self._add_judge_criteria(value="""
            After the user answers how long they've lived in the UK, the agent should ask the user if:
            1. They've had a health condition for at least 3 months that they expect to continue for at least another 9
            2. Not expected to live more than 12 months
            The agent should offer 2 options:
            - Yes
            - No
        """)
        return self
    
    def do_you_need_help_or_struggle_with_any_of_the_following_tasks_for_over_half_of_any_given_day(self, value: str) -> PipScenario:
        self._add_user_input(value=value)
        self._add_judge_criteria(value="""
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
        """)
        return self
    
    def clarify_health_condition_tasks_terms(self) -> PipScenario:
        self._add_user_input(value="What is meant by 'needing help'?")
        self._add_judge_criteria(value="The agent should offer the following definition for 'needing help' when asked: 'Only being able to do a task by using an aid (like a grab rail, a walking stick, or a dossette box for pills) counts.'")
        
        self._add_user_input(value="What is meant by 'preparing and eating'?")
        self._add_judge_criteria(value="The agent should offer the following definition for 'Preparing & Eating' when asked: 'cooking a simple meal, cutting up food, or being reminded to eat'")
        
        self._add_user_input(value="What is meant by 'hygiene'?")
        self._add_judge_criteria(value="The agent should offer the following definition for 'Hygiene' when asked: 'washing, bathing, or using the toilet'")
        
        self._add_user_input(value="What is meant by 'dressing'?")
        self._add_judge_criteria(value="The agent should offer the following definition for 'Dressing' when asked: 'putting on or taking off clothes'")
        
        self._add_user_input(value="What is meant by 'managing health'?")
        self._add_judge_criteria(value="The agent should offer the following definition for 'Managing Health' when asked: 'managing medication, monitoring a health condition, or using medical equipment'")
        
        self._add_user_input(value="What is meant by 'communication'?")
        self._add_judge_criteria(value="The agent should offer the following definition for 'Communication' when asked: 'speaking to others, hearing/understanding what is being said, or reading basic information'")
        
        self._add_user_input(value="What is meant by 'socializing'?")
        self._add_judge_criteria(value="The agent should offer the following definition for 'Socializing' when asked: 'difficulty being around other people, or interacting with them'")
        
        self._add_user_input(value="What is meant by 'finances'?")
        self._add_judge_criteria(value="The agent should offer the following definition for 'Finances' when asked: 'managing money or making decisions about spending'")
        
        self._add_user_input(value="What is meant by 'planning a journey'?")
        self._add_judge_criteria(value="The agent should offer the following definition for 'Planning a Journey' when asked: 'planning or following a route because of a mental health condition, sensory impairment, or learning disability e.g., getting overwhelmed or lost'")
        
        self._add_user_input(value="What is meant by 'moving around'?")
        self._add_judge_criteria(value="The agent should offer the following definition for 'Moving Around' when asked: 'physical difficulty walking e.g., you are only able to walk a short distance (20 or 50 meters), before needing to stop'")

        return self    

    def with_respect_to_those_tasks_do_any_of_the_following_apply(self, value: str) -> PipScenario:
        self._add_user_input(value=value)
        self._add_judge_criteria(value="""
            After the user answers about their struggles with tasks, the agent should ask whether any of the following apply to the tasks they struggle with:
            - Safety
            - Time
            - Frequency
            - Standard
        """)
        return self
            
    def clarify_health_condition_tasks_qualification_terms(self) -> PipScenario:
        self._add_user_input(value="What is meant by 'safety'?")
        self._add_judge_criteria(value="The agent should offer the following definition for 'Safety' when asked: 'you can't do the task without putting yourself or others at risk'")

        self._add_user_input(value="What is meant by 'time'?")
        self._add_judge_criteria(value="The agent should offer the following definition for 'Time' when asked: 'it takes you much longer (more than twice as long) than it would take a person without your condition'")

        self._add_user_input(value="What is meant by 'frequency'?")
        self._add_judge_criteria(value="The agent should offer the following definition for 'Frequency' when asked: 'you can't do it as often as you need to throughout the day'")

        self._add_user_input(value="What is meant by 'standard'?")
        self._add_judge_criteria(value="The agent should offer the following definition for 'Standard' when asked: 'you can't do it to an acceptable standard'")

        return self

    def would_you_like_me_to_check_what_implications_there_are_with_other_benefits_if_you_were_apply_and_be_found_eligible(self, value: str) -> PipScenario:
        self._add_user_input(value)
        self._add_judge_criteria("""
            The agent should tell the user the following:
            
            - Benefit Cap: If you or your partner receive PIP, your household is completely exempt from the benefit cap (the limit on the total amount of benefits you can get).
            - Universal Credit: While PIP doesn't automatically increase your UC standard allowance, it can unlock extra help. For example, if you claim for a disabled child who gets PIP, you can get the disabled child addition.
            - Legacy Benefits: If you are still on older benefits like Housing Benefit, Income Support, or Working Tax Credit, getting PIP can entitle you to extra "disability premiums" which increase your overall payments.
            - Carer’s Allowance: If you are awarded the daily living component of PIP, someone who cares for you for at least 35 hours a week may become eligible to claim Carer’s Allowance or the Carer Element of Universal Credit.
            - Council Tax: Receiving PIP often makes you eligible for a reduction in your local Council Tax bill. You have to apply for this directly through your local council.
            - Blue Badge: You may automatically qualify for a Blue Badge for easier parking.
            - Vehicle Tax: You can get a 50% discount on your road tax if you get the standard mobility rate, or a 100% exemption if you get the enhanced mobility rate.
            - Motability Scheme: If you receive the enhanced mobility rate, you can use it to lease a new car, wheelchair-accessible vehicle, or mobility scooter through the Motability Scheme.
            - Public Transport: You become eligible for a Disabled Persons Railcard (1/3 off train fares) and a free or discounted local bus pass.
        """)
        return self