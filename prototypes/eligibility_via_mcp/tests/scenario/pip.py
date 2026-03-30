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

    def _get_judge_criteria_for_implicated_benefits(self) -> str:
        return """
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
        """
