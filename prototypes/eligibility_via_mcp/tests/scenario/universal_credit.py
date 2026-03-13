from tests.scenario.base import BaseScenario

class UniversalCreditScenario(BaseScenario):

    def _get_eligibility_name(self) -> str:
        return "Universal Credit"

    def _get_judge_criteria_for_implicated_benefits(self) -> str:
        return """
        The agent should tell the user the following:
        - Housing Benefit: If you're eligible for Universal Credit, you cannot claim Housing Benefit. Universal Credit includes help with housing costs instead. If you're currently receiving Housing Benefit, it will stop when you claim Universal Credit.
        - Income Support: Universal Credit replaces Income Support. If you're currently receiving Income Support, you cannot receive both at the same time. You would need to move to Universal Credit.
        - Income-based Jobseeker's Allowance (JSA): Universal Credit replaces income-based Jobseeker's Allowance. If you're currently receiving income-based JSA, you cannot receive both at the same time. You would need to move to Universal Credit.
        - Income-related Employment and Support Allowance (ESA): Universal Credit replaces income-related Employment and Support Allowance. If you're currently receiving income-related ESA, you cannot receive both at the same time. You would need to move to Universal Credit.
        - Working Tax Credit: Universal Credit replaces Working Tax Credit. If you're currently receiving Working Tax Credit, you cannot receive both at the same time. You would need to move to Universal Credit.
        - Child Tax Credit: Universal Credit replaces Child Tax Credit. If you're currently receiving Child Tax Credit, you cannot receive both at the same time. Universal Credit includes support for children instead.
        - Pension Credit: If you or your partner are receiving Pension Credit and one of you is under State Pension age, claiming Universal Credit will stop your Pension Credit payments. You're usually better off staying on Pension Credit. Check with a benefits calculator before applying.
        - Council Tax Reduction: If you're eligible for Universal Credit, you may also be eligible for Council Tax Reduction (also called Council Tax Support). This is a separate benefit administered by your local council that can help reduce your council tax bill. You need to apply separately to your local council.
        - Free School Meals: If you're eligible for Universal Credit and have children, they may be eligible for free school meals if your household income (after tax and not including any benefits) is less than £7,400 per year.
        - Healthy Start Vouchers: If you're eligible for Universal Credit and are pregnant or have children under 4, you may be eligible for Healthy Start vouchers to help buy healthy food and milk. Your household income must be £408 or less per month after tax, not including any benefits.
        - Sure Start Maternity Grant: If you're eligible for Universal Credit and expecting your first child or expecting a multiple birth, you may be eligible for a Sure Start Maternity Grant of £500 to help with the costs of a new baby.
        - Budgeting Advances: If you're eligible for Universal Credit and have been receiving it for at least 6 months, you may be able to get a Budgeting Advance - an interest-free loan to help with emergency household costs or getting a job.
        - NHS Low Income Scheme: If you're eligible for Universal Credit, you may qualify for help with health costs through the NHS Low Income Scheme, including free prescriptions, dental treatment, eye tests, and travel to hospital for NHS treatment.
        - Carer's Allowance: If you're eligible for Universal Credit and caring for someone for at least 35 hours a week, you may also be eligible for Carer's Allowance. However, if you receive Carer's Allowance, it will be taken into account as income when calculating your Universal Credit payment.
        """

    def clarify_question_1_terms(self) -> 'UniversalCreditScenario':
        # No glossary terms for question 1
        return self

    def do_you_live_in_the_uk(self, answer: str, previous_question_id: int | None = None) -> 'UniversalCreditScenario':
        self.user_inputs.append(answer)
        
        expected_question = "Do you live in the UK?"
        if previous_question_id:
            self.judge_criteria.append(f"After Question {previous_question_id} was answered, the agent must ask '{expected_question}'. The user answered '{answer}'.")
        else:
            self.judge_criteria.append(f"The agent must start the assessment by asking '{expected_question}'. The user answered '{answer}'.")
            
        return self

    def clarify_question_2_terms(self) -> 'UniversalCreditScenario':
        # No glossary terms for question 2
        return self

    def are_you_aged_16_or_17(self, answer: str, previous_question_id: int | None = None) -> 'UniversalCreditScenario':
        self.user_inputs.append(answer)
        
        expected_question = "Are you aged 16 or 17?"
        if previous_question_id:
            self.judge_criteria.append(f"After Question {previous_question_id} was answered, the agent must ask '{expected_question}'. The user answered '{answer}'.")
        else:
            self.judge_criteria.append(f"The agent must start the assessment by asking '{expected_question}'. The user answered '{answer}'.")
            
        return self

    def clarify_question_3_terms(self) -> 'UniversalCreditScenario':
        self.user_inputs.append("What is meant by 'State Pension age'?")
        self.judge_criteria.append("The agent should offer the following definition for 'State Pension age': The age at which you can start claiming your State Pension. This varies depending on when you were born.")
        return self

    def are_you_aged_18_or_over_but_under_state_pension_age(self, answer: str, previous_question_id: int | None = None) -> 'UniversalCreditScenario':
        self.user_inputs.append(answer)
        
        expected_question = "Are you aged 18 or over but under State Pension age?"
        if previous_question_id:
            self.judge_criteria.append(f"After Question {previous_question_id} was answered, the agent must ask '{expected_question}'. The user answered '{answer}'.")
        else:
            self.judge_criteria.append(f"The agent must start the assessment by asking '{expected_question}'. The user answered '{answer}'.")
            
        return self

    def clarify_question_4_terms(self) -> 'UniversalCreditScenario':
        # No glossary terms for question 4
        return self

    def do_you_have_16000_or_less_in_money_savings_and_investments(self, answer: str, previous_question_id: int | None = None) -> 'UniversalCreditScenario':
        self.user_inputs.append(answer)
        
        expected_question = "Do you have £16,000 or less in money, savings and investments?"
        if previous_question_id:
            self.judge_criteria.append(f"After Question {previous_question_id} was answered, the agent must ask '{expected_question}'. The user answered '{answer}'.")
        else:
            self.judge_criteria.append(f"The agent must start the assessment by asking '{expected_question}'. The user answered '{answer}'.")
            
        return self

    def clarify_question_5_terms(self) -> 'UniversalCreditScenario':
        self.user_inputs.append("What is meant by 'EU'?")
        self.judge_criteria.append("The agent should offer the following definition for 'EU': European Union - a political and economic union of member states located primarily in Europe.")
        self.user_inputs.append("What is meant by 'EEA'?")
        self.judge_criteria.append("The agent should offer the following definition for 'EEA': European Economic Area - includes EU countries and also Iceland, Liechtenstein and Norway.")
        return self

    def are_you_an_eu_eea_or_swiss_citizen(self, answer: str, previous_question_id: int | None = None) -> 'UniversalCreditScenario':
        self.user_inputs.append(answer)
        
        expected_question = "Are you an EU, EEA or Swiss citizen?"
        if previous_question_id:
            self.judge_criteria.append(f"After Question {previous_question_id} was answered, the agent must ask '{expected_question}'. The user answered '{answer}'.")
        else:
            self.judge_criteria.append(f"The agent must start the assessment by asking '{expected_question}'. The user answered '{answer}'.")
            
        return self

    def clarify_question_6_terms(self) -> 'UniversalCreditScenario':
        self.user_inputs.append("What is meant by 'EU Settlement Scheme'?")
        self.judge_criteria.append("The agent should offer the following definition for 'EU Settlement Scheme': A scheme that allows EU, EEA and Swiss citizens and their family members to continue living in the UK after Brexit. It grants either settled or pre-settled status.")
        return self

    def do_you_have_settled_or_presettled_status_under_the_eu_settlement_scheme(self, answer: str, previous_question_id: int | None = None) -> 'UniversalCreditScenario':
        self.user_inputs.append(answer)
        
        expected_question = "Do you have settled or pre-settled status under the EU Settlement Scheme?"
        if previous_question_id:
            self.judge_criteria.append(f"After Question {previous_question_id} was answered, the agent must ask '{expected_question}'. The user answered '{answer}'.")
        else:
            self.judge_criteria.append(f"The agent must start the assessment by asking '{expected_question}'. The user answered '{answer}'.")
            
        return self

    def clarify_question_7_terms(self) -> 'UniversalCreditScenario':
        # No glossary terms for question 7
        return self

    def do_you_live_with_a_partner(self, answer: str, previous_question_id: int | None = None) -> 'UniversalCreditScenario':
        self.user_inputs.append(answer)
        
        expected_question = "Do you live with a partner?"
        if previous_question_id:
            self.judge_criteria.append(f"After Question {previous_question_id} was answered, the agent must ask '{expected_question}'. The user answered '{answer}'.")
        else:
            self.judge_criteria.append(f"The agent must start the assessment by asking '{expected_question}'. The user answered '{answer}'.")
            
        return self

    def clarify_question_8_terms(self) -> 'UniversalCreditScenario':
        # No glossary terms for question 8
        return self

    def is_your_partner_eligible_for_universal_credit(self, answer: str, previous_question_id: int | None = None) -> 'UniversalCreditScenario':
        self.user_inputs.append(answer)
        
        expected_question = "Is your partner eligible for Universal Credit?"
        if previous_question_id:
            self.judge_criteria.append(f"After Question {previous_question_id} was answered, the agent must ask '{expected_question}'. The user answered '{answer}'.")
        else:
            self.judge_criteria.append(f"The agent must start the assessment by asking '{expected_question}'. The user answered '{answer}'.")
            
        return self

    def clarify_question_9_terms(self) -> 'UniversalCreditScenario':
        # No glossary terms for question 9
        return self

    def has_either_you_or_your_partner_reached_state_pension_age(self, answer: str, previous_question_id: int | None = None) -> 'UniversalCreditScenario':
        self.user_inputs.append(answer)
        
        expected_question = "Has either you or your partner reached State Pension age?"
        if previous_question_id:
            self.judge_criteria.append(f"After Question {previous_question_id} was answered, the agent must ask '{expected_question}'. The user answered '{answer}'.")
        else:
            self.judge_criteria.append(f"The agent must start the assessment by asking '{expected_question}'. The user answered '{answer}'.")
            
        return self

    def clarify_question_10_terms(self) -> 'UniversalCreditScenario':
        # No glossary terms for question 10
        return self

    def have_both_you_and_your_partner_reached_state_pension_age(self, answer: str, previous_question_id: int | None = None) -> 'UniversalCreditScenario':
        self.user_inputs.append(answer)
        
        expected_question = "Have both you and your partner reached State Pension age?"
        if previous_question_id:
            self.judge_criteria.append(f"After Question {previous_question_id} was answered, the agent must ask '{expected_question}'. The user answered '{answer}'.")
        else:
            self.judge_criteria.append(f"The agent must start the assessment by asking '{expected_question}'. The user answered '{answer}'.")
            
        return self

    def clarify_question_11_terms(self) -> 'UniversalCreditScenario':
        self.user_inputs.append("What is meant by 'Pension Credit'?")
        self.judge_criteria.append("The agent should offer the following definition for 'Pension Credit': A means-tested benefit for people over State Pension age who are on a low income. It tops up your weekly income to a guaranteed minimum level.")
        return self

    def are_you_currently_getting_pension_credit(self, answer: str, previous_question_id: int | None = None) -> 'UniversalCreditScenario':
        self.user_inputs.append(answer)
        
        expected_question = "Are you currently getting Pension Credit?"
        if previous_question_id:
            self.judge_criteria.append(f"After Question {previous_question_id} was answered, the agent must ask '{expected_question}'. The user answered '{answer}'.")
        else:
            self.judge_criteria.append(f"The agent must start the assessment by asking '{expected_question}'. The user answered '{answer}'.")
            
        return self

    def clarify_question_12_terms(self) -> 'UniversalCreditScenario':
        # No glossary terms for question 12
        return self

    def are_you_in_fulltime_education_or_training(self, answer: str, previous_question_id: int | None = None) -> 'UniversalCreditScenario':
        self.user_inputs.append(answer)
        
        expected_question = "Are you in full-time education or training?"
        if previous_question_id:
            self.judge_criteria.append(f"After Question {previous_question_id} was answered, the agent must ask '{expected_question}'. The user answered '{answer}'.")
        else:
            self.judge_criteria.append(f"The agent must start the assessment by asking '{expected_question}'. The user answered '{answer}'.")
            
        return self

    def clarify_question_13_terms(self) -> 'UniversalCreditScenario':
        # No glossary terms for question 13
        return self

    def do_you_live_with_a_partner_who_is_eligible_for_universal_credit(self, answer: str, previous_question_id: int | None = None) -> 'UniversalCreditScenario':
        self.user_inputs.append(answer)
        
        expected_question = "Do you live with a partner who is eligible for Universal Credit?"
        if previous_question_id:
            self.judge_criteria.append(f"After Question {previous_question_id} was answered, the agent must ask '{expected_question}'. The user answered '{answer}'.")
        else:
            self.judge_criteria.append(f"The agent must start the assessment by asking '{expected_question}'. The user answered '{answer}'.")
            
        return self

    def clarify_question_14_terms(self) -> 'UniversalCreditScenario':
        # No glossary terms for question 14
        return self

    def are_you_responsible_for_a_child(self, answer: str, previous_question_id: int | None = None) -> 'UniversalCreditScenario':
        self.user_inputs.append(answer)
        
        expected_question = "Are you responsible for a child (either as a single person or as a couple)?"
        if previous_question_id:
            self.judge_criteria.append(f"After Question {previous_question_id} was answered, the agent must ask '{expected_question}'. The user answered '{answer}'.")
        else:
            self.judge_criteria.append(f"The agent must start the assessment by asking '{expected_question}'. The user answered '{answer}'.")
            
        return self

    def clarify_question_15_terms(self) -> 'UniversalCreditScenario':
        # No glossary terms for question 15
        return self

    def have_you_reached_state_pension_age_and_live_with_a_partner_who_is_below_state_pension_age(self, answer: str, previous_question_id: int | None = None) -> 'UniversalCreditScenario':
        self.user_inputs.append(answer)
        
        expected_question = "Have you reached State Pension age and live with a partner who is below State Pension age?"
        if previous_question_id:
            self.judge_criteria.append(f"After Question {previous_question_id} was answered, the agent must ask '{expected_question}'. The user answered '{answer}'.")
        else:
            self.judge_criteria.append(f"The agent must start the assessment by asking '{expected_question}'. The user answered '{answer}'.")
            
        return self

    def clarify_question_16_terms(self) -> 'UniversalCreditScenario':
        self.user_inputs.append("What is meant by 'Migration Notice letter'?")
        self.judge_criteria.append("The agent should offer the following definition for 'Migration Notice letter': A letter sent to people on certain legacy benefits telling them to move to Universal Credit by a specific date.")
        return self

    def have_you_received_a_migration_notice_letter_telling_you_to_move_to_universal_credit(self, answer: str, previous_question_id: int | None = None) -> 'UniversalCreditScenario':
        self.user_inputs.append(answer)
        
        expected_question = "Have you received a Migration Notice letter telling you to move to Universal Credit?"
        if previous_question_id:
            self.judge_criteria.append(f"After Question {previous_question_id} was answered, the agent must ask '{expected_question}'. The user answered '{answer}'.")
        else:
            self.judge_criteria.append(f"The agent must start the assessment by asking '{expected_question}'. The user answered '{answer}'.")
            
        return self

    def clarify_question_17_terms(self) -> 'UniversalCreditScenario':
        # No glossary terms for question 17
        return self

    def are_you_21_or_under_studying_any_qualification_up_to_a_level_or_equivalent_and_do_not_have_parental_support(self, answer: str, previous_question_id: int | None = None) -> 'UniversalCreditScenario':
        self.user_inputs.append(answer)
        
        expected_question = "Are you 21 or under, studying any qualification up to A level or equivalent, and do not have parental support?"
        if previous_question_id:
            self.judge_criteria.append(f"After Question {previous_question_id} was answered, the agent must ask '{expected_question}'. The user answered '{answer}'.")
        else:
            self.judge_criteria.append(f"The agent must start the assessment by asking '{expected_question}'. The user answered '{answer}'.")
            
        return self

    def clarify_question_18_terms(self) -> 'UniversalCreditScenario':
        # No glossary terms for question 18
        return self

    def are_you_studying_parttime(self, answer: str, previous_question_id: int | None = None) -> 'UniversalCreditScenario':
        self.user_inputs.append(answer)
        
        expected_question = "Are you studying part-time?"
        if previous_question_id:
            self.judge_criteria.append(f"After Question {previous_question_id} was answered, the agent must ask '{expected_question}'. The user answered '{answer}'.")
        else:
            self.judge_criteria.append(f"The agent must start the assessment by asking '{expected_question}'. The user answered '{answer}'.")
            
        return self

    def clarify_question_19_terms(self) -> 'UniversalCreditScenario':
        # No glossary terms for question 19
        return self

    def is_your_course_one_for_which_no_student_loan_or_finance_is_available(self, answer: str, previous_question_id: int | None = None) -> 'UniversalCreditScenario':
        self.user_inputs.append(answer)
        
        expected_question = "Is your course one for which no student loan or finance is available?"
        if previous_question_id:
            self.judge_criteria.append(f"After Question {previous_question_id} was answered, the agent must ask '{expected_question}'. The user answered '{answer}'.")
        else:
            self.judge_criteria.append(f"The agent must start the assessment by asking '{expected_question}'. The user answered '{answer}'.")
            
        return self

    def clarify_question_20_terms(self) -> 'UniversalCreditScenario':
        # No glossary terms for question 20
        return self

    def do_you_have_a_disability_or_health_condition(self, answer: str, previous_question_id: int | None = None) -> 'UniversalCreditScenario':
        self.user_inputs.append(answer)
        
        expected_question = "Do you have a disability or health condition?"
        if previous_question_id:
            self.judge_criteria.append(f"After Question {previous_question_id} was answered, the agent must ask '{expected_question}'. The user answered '{answer}'.")
        else:
            self.judge_criteria.append(f"The agent must start the assessment by asking '{expected_question}'. The user answered '{answer}'.")
            
        return self

    def clarify_question_21_terms(self) -> 'UniversalCreditScenario':
        self.user_inputs.append("What is meant by 'Work Capability Assessment'?")
        self.judge_criteria.append("The agent should offer the following definition for 'Work Capability Assessment': An assessment used to determine whether your health condition or disability limits your ability to work. It decides if you have limited capability for work or limited capability for work-related activity.")
        return self

    def were_you_assessed_as_having_limited_capability_for_work_by_a_work_capability_assessment_before_starting_your_course(self, answer: str, previous_question_id: int | None = None) -> 'UniversalCreditScenario':
        self.user_inputs.append(answer)
        
        expected_question = "Were you assessed as having limited capability for work by a Work Capability Assessment before starting your course?"
        if previous_question_id:
            self.judge_criteria.append(f"After Question {previous_question_id} was answered, the agent must ask '{expected_question}'. The user answered '{answer}'.")
        else:
            self.judge_criteria.append(f"The agent must start the assessment by asking '{expected_question}'. The user answered '{answer}'.")
            
        return self

    def clarify_question_22_terms(self) -> 'UniversalCreditScenario':
        self.user_inputs.append("What is meant by 'Personal Independence Payment (PIP)'?")
        self.judge_criteria.append("The agent should offer the following definition for 'Personal Independence Payment (PIP)': A benefit for people aged 16 to State Pension age who have long-term ill-health or disability and need help with daily living activities or mobility.")
        self.user_inputs.append("What is meant by 'Disability Living Allowance (DLA)'?")
        self.judge_criteria.append("The agent should offer the following definition for 'Disability Living Allowance (DLA)': A benefit to help with the extra costs of looking after a child under 16 with disabilities. Adults who were getting DLA before April 2013 may still receive it.")
        self.user_inputs.append("What is meant by 'Attendance Allowance'?")
        self.judge_criteria.append("The agent should offer the following definition for 'Attendance Allowance': A benefit for people over State Pension age who need help with personal care or supervision because of illness or disability.")
        self.user_inputs.append("What is meant by 'Armed Forces Independence Payment'?")
        self.judge_criteria.append("The agent should offer the following definition for 'Armed Forces Independence Payment': A tax-free payment for service personnel and veterans who have been seriously injured as a result of military service.")
        self.user_inputs.append("What is meant by 'Adult Disability Payment (ADP)'?")
        self.judge_criteria.append("The agent should offer the following definition for 'Adult Disability Payment (ADP)': A Scottish benefit replacing PIP in Scotland for people aged 16 to State Pension age with a disability or long-term health condition.")
        self.user_inputs.append("What is meant by 'Child Disability Payment (CDP)'?")
        self.judge_criteria.append("The agent should offer the following definition for 'Child Disability Payment (CDP)': A Scottish benefit replacing DLA for children in Scotland under 18 with a disability or long-term health condition.")
        self.user_inputs.append("What is meant by 'Pension Age Disability Payment (PADP)'?")
        self.judge_criteria.append("The agent should offer the following definition for 'Pension Age Disability Payment (PADP)': A Scottish benefit replacing Attendance Allowance in Scotland for people over State Pension age.")
        self.user_inputs.append("What is meant by 'Scottish Adult Disability Living Allowance (SADLA)'?")
        self.judge_criteria.append("The agent should offer the following definition for 'Scottish Adult Disability Living Allowance (SADLA)': A transitional disability benefit in Scotland for those previously receiving DLA.")
        return self

    def are_you_entitled_to_pip_dla_attendance_allowance_or_other_qualifying_disability_benefits(self, answer: str, previous_question_id: int | None = None) -> 'UniversalCreditScenario':
        self.user_inputs.append(answer)
        
        expected_question = "Are you entitled to Personal Independence Payment (PIP), Disability Living Allowance (DLA), Attendance Allowance, Armed Forces Independence Payment, Adult Disability Payment (ADP) in Scotland, Child Disability Payment (CDP) in Scotland, Pension Age Disability Payment (PADP) in Scotland, or Scottish Adult Disability Living Allowance (SADLA) in Scotland?"
        if previous_question_id:
            self.judge_criteria.append(f"After Question {previous_question_id} was answered, the agent must ask '{expected_question}'. The user answered '{answer}'.")
        else:
            self.judge_criteria.append(f"The agent must start the assessment by asking '{expected_question}'. The user answered '{answer}'.")
            
        return self

    def clarify_question_23_terms(self) -> 'UniversalCreditScenario':
        self.user_inputs.append("What is meant by 'fit note'?")
        self.judge_criteria.append("The agent should offer the following definition for 'fit note': A statement from a doctor or medical professional that provides evidence of your health condition. Previously known as a sick note.")
        return self

    def do_you_have_a_health_condition_or_disability_with_medical_evidence_for_it(self, answer: str, previous_question_id: int | None = None) -> 'UniversalCreditScenario':
        self.user_inputs.append(answer)
        
        expected_question = "Do you have a health condition or disability with medical evidence for it, such as a fit note?"
        if previous_question_id:
            self.judge_criteria.append(f"After Question {previous_question_id} was answered, the agent must ask '{expected_question}'. The user answered '{answer}'.")
        else:
            self.judge_criteria.append(f"The agent must start the assessment by asking '{expected_question}'. The user answered '{answer}'.")
            
        return self

    def clarify_question_24_terms(self) -> 'UniversalCreditScenario':
        # No glossary terms for question 24
        return self

    def are_you_caring_for_someone_who_gets_a_health_or_disability_related_benefit(self, answer: str, previous_question_id: int | None = None) -> 'UniversalCreditScenario':
        self.user_inputs.append(answer)
        
        expected_question = "Are you caring for someone who gets a health or disability-related benefit?"
        if previous_question_id:
            self.judge_criteria.append(f"After Question {previous_question_id} was answered, the agent must ask '{expected_question}'. The user answered '{answer}'.")
        else:
            self.judge_criteria.append(f"The agent must start the assessment by asking '{expected_question}'. The user answered '{answer}'.")
            
        return self

    def clarify_question_25_terms(self) -> 'UniversalCreditScenario':
        self.user_inputs.append("What is meant by 'nearing the end of life'?")
        self.judge_criteria.append("The agent should offer the following definition for 'nearing the end of life': A clinical assessment that someone is likely to die within the next 12 months. This can provide access to fast-tracked benefits and support.")
        return self

    def has_a_medical_professional_said_you_are_nearing_the_end_of_life(self, answer: str, previous_question_id: int | None = None) -> 'UniversalCreditScenario':
        self.user_inputs.append(answer)
        
        expected_question = "Has a medical professional said you are nearing the end of life?"
        if previous_question_id:
            self.judge_criteria.append(f"After Question {previous_question_id} was answered, the agent must ask '{expected_question}'. The user answered '{answer}'.")
        else:
            self.judge_criteria.append(f"The agent must start the assessment by asking '{expected_question}'. The user answered '{answer}'.")
            
        return self

    def clarify_question_26_terms(self) -> 'UniversalCreditScenario':
        # No glossary terms for question 26
        return self

    def are_you_pregnant_and_expecting_your_baby_in_the_next_11_weeks(self, answer: str, previous_question_id: int | None = None) -> 'UniversalCreditScenario':
        self.user_inputs.append(answer)
        
        expected_question = "Are you pregnant and expecting your baby in the next 11 weeks?"
        if previous_question_id:
            self.judge_criteria.append(f"After Question {previous_question_id} was answered, the agent must ask '{expected_question}'. The user answered '{answer}'.")
        else:
            self.judge_criteria.append(f"The agent must start the assessment by asking '{expected_question}'. The user answered '{answer}'.")
            
        return self

    def clarify_question_27_terms(self) -> 'UniversalCreditScenario':
        # No glossary terms for question 27
        return self

    def have_you_had_a_baby_in_the_last_15_weeks(self, answer: str, previous_question_id: int | None = None) -> 'UniversalCreditScenario':
        self.user_inputs.append(answer)
        
        expected_question = "Have you had a baby in the last 15 weeks?"
        if previous_question_id:
            self.judge_criteria.append(f"After Question {previous_question_id} was answered, the agent must ask '{expected_question}'. The user answered '{answer}'.")
        else:
            self.judge_criteria.append(f"The agent must start the assessment by asking '{expected_question}'. The user answered '{answer}'.")
            
        return self

    def clarify_question_28_terms(self) -> 'UniversalCreditScenario':
        self.user_inputs.append("What is meant by 'local authority care'?")
        self.judge_criteria.append("The agent should offer the following definition for 'local authority care': When a child or young person is looked after by their local council, either in foster care, a children's home, or other accommodation provided by the council.")
        return self

    def do_you_have_parental_support(self, answer: str, previous_question_id: int | None = None) -> 'UniversalCreditScenario':
        self.user_inputs.append(answer)
        
        expected_question = "Do you have parental support (for example, do you live with your parents or are you under local authority care)?"
        if previous_question_id:
            self.judge_criteria.append(f"After Question {previous_question_id} was answered, the agent must ask '{expected_question}'. The user answered '{answer}'.")
        else:
            self.judge_criteria.append(f"The agent must start the assessment by asking '{expected_question}'. The user answered '{answer}'.")
            
        return self

    def clarify_question_29_terms(self) -> 'UniversalCreditScenario':
        # No glossary terms for question 29
        return self

    def are_you_in_the_armed_forces_and_stationed_abroad(self, answer: str, previous_question_id: int | None = None) -> 'UniversalCreditScenario':
        self.user_inputs.append(answer)
        
        expected_question = "Are you in the armed forces and stationed abroad?"
        if previous_question_id:
            self.judge_criteria.append(f"After Question {previous_question_id} was answered, the agent must ask '{expected_question}'. The user answered '{answer}'.")
        else:
            self.judge_criteria.append(f"The agent must start the assessment by asking '{expected_question}'. The user answered '{answer}'.")
            
        return self
