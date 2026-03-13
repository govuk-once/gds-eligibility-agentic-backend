import pytest
from tests.scenario.universal_credit import UniversalCreditScenario

@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_ineligible_does_not_live_in_uk():
    await UniversalCreditScenario(
        short_description="Ineligible: User does not live in the UK.",
        user_intro="I've heard about universal credit and would like to apply.",
        user_should_be_eligible=False,
    ) \
    .clarify_question_1_terms() \
    .do_you_live_in_the_uk("No", previous_question_id=None) \
    .run()

@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_ineligible_over_state_pension_age():
    await UniversalCreditScenario(
        short_description="Ineligible: User is over State Pension age and not 16-17.",
        user_intro="I am over State Pension age and looking to see if I can apply for universal credit.",
        user_should_be_eligible=False,
    ) \
    .clarify_question_1_terms() \
    .do_you_live_in_the_uk("Yes", previous_question_id=None) \
    .clarify_question_2_terms() \
    .are_you_aged_16_or_17("No", previous_question_id=1) \
    .clarify_question_3_terms() \
    .are_you_aged_18_or_over_but_under_state_pension_age("No", previous_question_id=2) \
    .run()

@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_ineligible_savings_over_16000():
    await UniversalCreditScenario(
        short_description="Ineligible: User has more than £16,000 in savings.",
        user_intro="I am aged 25, have significant savings, and want to apply for universal credit.",
        user_should_be_eligible=False,
    ) \
    .clarify_question_1_terms() \
    .do_you_live_in_the_uk("Yes", previous_question_id=None) \
    .clarify_question_2_terms() \
    .are_you_aged_16_or_17("No", previous_question_id=1) \
    .clarify_question_3_terms() \
    .are_you_aged_18_or_over_but_under_state_pension_age("Yes", previous_question_id=2) \
    .clarify_question_4_terms() \
    .do_you_have_16000_or_less_in_money_savings_and_investments("No", previous_question_id=3) \
    .run()


@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_ineligible_eu_citizen_without_settled_status():
    await UniversalCreditScenario(
        short_description="Ineligible: EU citizen without settled or pre-settled status.",
        user_intro="I am an EU citizen living in the UK and I'm asking about universal credit.",
        user_should_be_eligible=False,
    ) \
    .clarify_question_1_terms() \
    .do_you_live_in_the_uk("Yes", previous_question_id=None) \
    .clarify_question_2_terms() \
    .are_you_aged_16_or_17("No", previous_question_id=1) \
    .clarify_question_3_terms() \
    .are_you_aged_18_or_over_but_under_state_pension_age("Yes", previous_question_id=2) \
    .clarify_question_4_terms() \
    .do_you_have_16000_or_less_in_money_savings_and_investments("Yes", previous_question_id=3) \
    .clarify_question_5_terms() \
    .are_you_an_eu_eea_or_swiss_citizen("Yes", previous_question_id=4) \
    .clarify_question_6_terms() \
    .do_you_have_settled_or_presettled_status_under_the_eu_settlement_scheme("No", previous_question_id=5) \
    .run()

@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_ineligible_both_partners_at_state_pension_age():
    await UniversalCreditScenario(
        short_description="Ineligible: Both partners have reached State Pension age.",
        user_intro="My partner and I have both reached State Pension age, but we want to see if we can get universal credit.",
        user_should_be_eligible=False,
    ) \
    .clarify_question_1_terms() \
    .do_you_live_in_the_uk("Yes", previous_question_id=None) \
    .clarify_question_2_terms() \
    .are_you_aged_16_or_17("No", previous_question_id=1) \
    .clarify_question_3_terms() \
    .are_you_aged_18_or_over_but_under_state_pension_age("Yes", previous_question_id=2) \
    .clarify_question_4_terms() \
    .do_you_have_16000_or_less_in_money_savings_and_investments("Yes", previous_question_id=3) \
    .clarify_question_5_terms() \
    .are_you_an_eu_eea_or_swiss_citizen("No", previous_question_id=4) \
    .clarify_question_7_terms() \
    .do_you_live_with_a_partner("Yes", previous_question_id=5) \
    .clarify_question_9_terms() \
    .has_either_you_or_your_partner_reached_state_pension_age("Yes", previous_question_id=7) \
    .clarify_question_10_terms() \
    .have_both_you_and_your_partner_reached_state_pension_age("Yes", previous_question_id=9) \
    .run()

@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_ineligible_student_no_exemption():
    await UniversalCreditScenario(
        short_description="Ineligible: Full-time student without any exemption criteria.",
        user_intro="I am a full-time university student wondering if I can get universal credit.",
        user_should_be_eligible=False,
    ) \
    .clarify_question_1_terms() \
    .do_you_live_in_the_uk("Yes", previous_question_id=None) \
    .clarify_question_2_terms() \
    .are_you_aged_16_or_17("No", previous_question_id=1) \
    .clarify_question_3_terms() \
    .are_you_aged_18_or_over_but_under_state_pension_age("Yes", previous_question_id=2) \
    .clarify_question_4_terms() \
    .do_you_have_16000_or_less_in_money_savings_and_investments("Yes", previous_question_id=3) \
    .clarify_question_5_terms() \
    .are_you_an_eu_eea_or_swiss_citizen("No", previous_question_id=4) \
    .clarify_question_7_terms() \
    .do_you_live_with_a_partner("No", previous_question_id=5) \
    .clarify_question_12_terms() \
    .are_you_in_fulltime_education_or_training("Yes", previous_question_id=7) \
    .clarify_question_13_terms() \
    .do_you_live_with_a_partner_who_is_eligible_for_universal_credit("No", previous_question_id=12) \
    .clarify_question_14_terms() \
    .are_you_responsible_for_a_child("No", previous_question_id=13) \
    .clarify_question_15_terms() \
    .have_you_reached_state_pension_age_and_live_with_a_partner_who_is_below_state_pension_age("No", previous_question_id=14) \
    .clarify_question_16_terms() \
    .have_you_received_a_migration_notice_letter_telling_you_to_move_to_universal_credit("No", previous_question_id=15) \
    .clarify_question_17_terms() \
    .are_you_21_or_under_studying_any_qualification_up_to_a_level_or_equivalent_and_do_not_have_parental_support("No", previous_question_id=16) \
    .clarify_question_18_terms() \
    .are_you_studying_parttime("No", previous_question_id=17) \
    .clarify_question_19_terms() \
    .is_your_course_one_for_which_no_student_loan_or_finance_is_available("No", previous_question_id=18) \
    .clarify_question_21_terms() \
    .were_you_assessed_as_having_limited_capability_for_work_by_a_work_capability_assessment_before_starting_your_course("No", previous_question_id=19) \
    .run()


@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_ineligible_student_disability_assessed_but_no_qualifying_benefit():
    await UniversalCreditScenario(
        short_description="Ineligible: Full-time student with disability assessed before course but no qualifying benefit.",
        user_intro="I am a full-time student with a disability seeking universal credit.",
        user_should_be_eligible=False,
    ) \
    .clarify_question_1_terms() \
    .do_you_live_in_the_uk("Yes", previous_question_id=None) \
    .clarify_question_2_terms() \
    .are_you_aged_16_or_17("No", previous_question_id=1) \
    .clarify_question_3_terms() \
    .are_you_aged_18_or_over_but_under_state_pension_age("Yes", previous_question_id=2) \
    .clarify_question_4_terms() \
    .do_you_have_16000_or_less_in_money_savings_and_investments("Yes", previous_question_id=3) \
    .clarify_question_5_terms() \
    .are_you_an_eu_eea_or_swiss_citizen("No", previous_question_id=4) \
    .clarify_question_7_terms() \
    .do_you_live_with_a_partner("No", previous_question_id=5) \
    .clarify_question_12_terms() \
    .are_you_in_fulltime_education_or_training("Yes", previous_question_id=7) \
    .clarify_question_13_terms() \
    .do_you_live_with_a_partner_who_is_eligible_for_universal_credit("No", previous_question_id=12) \
    .clarify_question_14_terms() \
    .are_you_responsible_for_a_child("No", previous_question_id=13) \
    .clarify_question_15_terms() \
    .have_you_reached_state_pension_age_and_live_with_a_partner_who_is_below_state_pension_age("No", previous_question_id=14) \
    .clarify_question_16_terms() \
    .have_you_received_a_migration_notice_letter_telling_you_to_move_to_universal_credit("No", previous_question_id=15) \
    .clarify_question_17_terms() \
    .are_you_21_or_under_studying_any_qualification_up_to_a_level_or_equivalent_and_do_not_have_parental_support("No", previous_question_id=16) \
    .clarify_question_18_terms() \
    .are_you_studying_parttime("No", previous_question_id=17) \
    .clarify_question_19_terms() \
    .is_your_course_one_for_which_no_student_loan_or_finance_is_available("No", previous_question_id=18) \
    .clarify_question_21_terms() \
    .were_you_assessed_as_having_limited_capability_for_work_by_a_work_capability_assessment_before_starting_your_course("Yes", previous_question_id=19) \
    .clarify_question_22_terms() \
    .are_you_entitled_to_pip_dla_attendance_allowance_or_other_qualifying_disability_benefits("No", previous_question_id=21) \
    .run()

@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_ineligible_16_17_with_parental_support():
    await UniversalCreditScenario(
        short_description="Ineligible: Age 16-17 with parental support and no other qualifying criteria.",
        user_intro="I am 17 years old, live with my parents, and want to claim universal credit.",
        user_should_be_eligible=False,
    ) \
    .clarify_question_1_terms() \
    .do_you_live_in_the_uk("Yes", previous_question_id=None) \
    .clarify_question_2_terms() \
    .are_you_aged_16_or_17("Yes", previous_question_id=1) \
    .clarify_question_23_terms() \
    .do_you_have_a_health_condition_or_disability_with_medical_evidence_for_it("No", previous_question_id=2) \
    .clarify_question_24_terms() \
    .are_you_caring_for_someone_who_gets_a_health_or_disability_related_benefit("No", previous_question_id=23) \
    .clarify_question_25_terms() \
    .has_a_medical_professional_said_you_are_nearing_the_end_of_life("No", previous_question_id=24) \
    .clarify_question_14_terms() \
    .are_you_responsible_for_a_child("No", previous_question_id=25) \
    .clarify_question_26_terms() \
    .are_you_pregnant_and_expecting_your_baby_in_the_next_11_weeks("No", previous_question_id=14) \
    .clarify_question_27_terms() \
    .have_you_had_a_baby_in_the_last_15_weeks("No", previous_question_id=26) \
    .clarify_question_28_terms() \
    .do_you_have_parental_support("Yes", previous_question_id=27) \
    .run()


@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_eligible_basic_no_partner_not_studying():
    await UniversalCreditScenario(
        short_description="Eligible: Basic eligibility - 18+, UK resident, savings ≤£16k, no partner, not studying.",
        user_intro="I am 30 years old and looking to apply for universal credit.",
        user_should_be_eligible=True,
    ) \
    .clarify_question_1_terms() \
    .do_you_live_in_the_uk("Yes", previous_question_id=None) \
    .clarify_question_2_terms() \
    .are_you_aged_16_or_17("No", previous_question_id=1) \
    .clarify_question_3_terms() \
    .are_you_aged_18_or_over_but_under_state_pension_age("Yes", previous_question_id=2) \
    .clarify_question_4_terms() \
    .do_you_have_16000_or_less_in_money_savings_and_investments("Yes", previous_question_id=3) \
    .clarify_question_5_terms() \
    .are_you_an_eu_eea_or_swiss_citizen("No", previous_question_id=4) \
    .clarify_question_7_terms() \
    .do_you_live_with_a_partner("No", previous_question_id=5) \
    .clarify_question_12_terms() \
    .are_you_in_fulltime_education_or_training("No", previous_question_id=7) \
    .clarify_question_20_terms() \
    .do_you_have_a_disability_or_health_condition("No", previous_question_id=12) \
    .clarify_question_29_terms() \
    .are_you_in_the_armed_forces_and_stationed_abroad("No", previous_question_id=20) \
    .would_you_like_me_to_check_what_implications_there_are_with_other_benefits_if_you_were_apply_and_be_found_eligible("Yes") \
    .run()

@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_eligible_with_eligible_partner():
    await UniversalCreditScenario(
        short_description="Eligible: With an eligible partner - joint claim required.",
        user_intro="I am 28 and my partner and I want to apply for universal credit.",
        user_should_be_eligible=True,
    ) \
    .clarify_question_1_terms() \
    .do_you_live_in_the_uk("Yes", previous_question_id=None) \
    .clarify_question_2_terms() \
    .are_you_aged_16_or_17("No", previous_question_id=1) \
    .clarify_question_3_terms() \
    .are_you_aged_18_or_over_but_under_state_pension_age("Yes", previous_question_id=2) \
    .clarify_question_4_terms() \
    .do_you_have_16000_or_less_in_money_savings_and_investments("Yes", previous_question_id=3) \
    .clarify_question_5_terms() \
    .are_you_an_eu_eea_or_swiss_citizen("No", previous_question_id=4) \
    .clarify_question_7_terms() \
    .do_you_live_with_a_partner("Yes", previous_question_id=5) \
    .clarify_question_9_terms() \
    .has_either_you_or_your_partner_reached_state_pension_age("No", previous_question_id=7) \
    .clarify_question_8_terms() \
    .is_your_partner_eligible_for_universal_credit("Yes", previous_question_id=9) \
    .would_you_like_me_to_check_what_implications_there_are_with_other_benefits_if_you_were_apply_and_be_found_eligible("Yes") \
    .run()

@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_eligible_with_ineligible_partner():
    await UniversalCreditScenario(
        short_description="Eligible: With an ineligible partner - still need joint claim.",
        user_intro="I live with my partner who is not eligible for Universal Credit.",
        user_should_be_eligible=True,
    ) \
    .clarify_question_1_terms() \
    .do_you_live_in_the_uk("Yes", previous_question_id=None) \
    .clarify_question_2_terms() \
    .are_you_aged_16_or_17("No", previous_question_id=1) \
    .clarify_question_3_terms() \
    .are_you_aged_18_or_over_but_under_state_pension_age("Yes", previous_question_id=2) \
    .clarify_question_4_terms() \
    .do_you_have_16000_or_less_in_money_savings_and_investments("Yes", previous_question_id=3) \
    .clarify_question_5_terms() \
    .are_you_an_eu_eea_or_swiss_citizen("No", previous_question_id=4) \
    .clarify_question_7_terms() \
    .do_you_live_with_a_partner("Yes", previous_question_id=5) \
    .clarify_question_9_terms() \
    .has_either_you_or_your_partner_reached_state_pension_age("No", previous_question_id=7) \
    .clarify_question_8_terms() \
    .is_your_partner_eligible_for_universal_credit("No", previous_question_id=9) \
    .would_you_like_me_to_check_what_implications_there_are_with_other_benefits_if_you_were_apply_and_be_found_eligible("Yes") \
    .run()


@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_eligible_eu_citizen_with_settled_status():
    await UniversalCreditScenario(
        short_description="Eligible: EU citizen with settled or pre-settled status.",
        user_intro="I am an EU citizen with settled status in the UK hoping to get universal credit.",
        user_should_be_eligible=True,
    ) \
    .clarify_question_1_terms() \
    .do_you_live_in_the_uk("Yes", previous_question_id=None) \
    .clarify_question_2_terms() \
    .are_you_aged_16_or_17("No", previous_question_id=1) \
    .clarify_question_3_terms() \
    .are_you_aged_18_or_over_but_under_state_pension_age("Yes", previous_question_id=2) \
    .clarify_question_4_terms() \
    .do_you_have_16000_or_less_in_money_savings_and_investments("Yes", previous_question_id=3) \
    .clarify_question_5_terms() \
    .are_you_an_eu_eea_or_swiss_citizen("Yes", previous_question_id=4) \
    .clarify_question_6_terms() \
    .do_you_have_settled_or_presettled_status_under_the_eu_settlement_scheme("Yes", previous_question_id=5) \
    .clarify_question_7_terms() \
    .do_you_live_with_a_partner("No", previous_question_id=6) \
    .clarify_question_12_terms() \
    .are_you_in_fulltime_education_or_training("No", previous_question_id=7) \
    .clarify_question_20_terms() \
    .do_you_have_a_disability_or_health_condition("No", previous_question_id=12) \
    .clarify_question_29_terms() \
    .are_you_in_the_armed_forces_and_stationed_abroad("No", previous_question_id=20) \
    .would_you_like_me_to_check_what_implications_there_are_with_other_benefits_if_you_were_apply_and_be_found_eligible("Yes") \
    .run()

@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_eligible_one_partner_at_pension_age_no_pension_credit():
    await UniversalCreditScenario(
        short_description="Eligible: One partner at State Pension age, not receiving Pension Credit.",
        user_intro="My partner has reached State Pension age but I have not, and we need universal credit.",
        user_should_be_eligible=True,
    ) \
    .clarify_question_1_terms() \
    .do_you_live_in_the_uk("Yes", previous_question_id=None) \
    .clarify_question_2_terms() \
    .are_you_aged_16_or_17("No", previous_question_id=1) \
    .clarify_question_3_terms() \
    .are_you_aged_18_or_over_but_under_state_pension_age("Yes", previous_question_id=2) \
    .clarify_question_4_terms() \
    .do_you_have_16000_or_less_in_money_savings_and_investments("Yes", previous_question_id=3) \
    .clarify_question_5_terms() \
    .are_you_an_eu_eea_or_swiss_citizen("No", previous_question_id=4) \
    .clarify_question_7_terms() \
    .do_you_live_with_a_partner("Yes", previous_question_id=5) \
    .clarify_question_9_terms() \
    .has_either_you_or_your_partner_reached_state_pension_age("Yes", previous_question_id=7) \
    .clarify_question_10_terms() \
    .have_both_you_and_your_partner_reached_state_pension_age("No", previous_question_id=9) \
    .clarify_question_11_terms() \
    .are_you_currently_getting_pension_credit("No", previous_question_id=10) \
    .clarify_question_8_terms() \
    .is_your_partner_eligible_for_universal_credit("Yes", previous_question_id=11) \
    .would_you_like_me_to_check_what_implications_there_are_with_other_benefits_if_you_were_apply_and_be_found_eligible("Yes") \
    .run()

@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_eligible_one_partner_at_pension_age_getting_pension_credit():
    await UniversalCreditScenario(
        short_description="Eligible: One partner at State Pension age, receiving Pension Credit (with warning).",
        user_intro="My partner has reached State Pension age and we receive Pension Credit, can we get universal credit too?",
        user_should_be_eligible=True,
    ) \
    .clarify_question_1_terms() \
    .do_you_live_in_the_uk("Yes", previous_question_id=None) \
    .clarify_question_2_terms() \
    .are_you_aged_16_or_17("No", previous_question_id=1) \
    .clarify_question_3_terms() \
    .are_you_aged_18_or_over_but_under_state_pension_age("Yes", previous_question_id=2) \
    .clarify_question_4_terms() \
    .do_you_have_16000_or_less_in_money_savings_and_investments("Yes", previous_question_id=3) \
    .clarify_question_5_terms() \
    .are_you_an_eu_eea_or_swiss_citizen("No", previous_question_id=4) \
    .clarify_question_7_terms() \
    .do_you_live_with_a_partner("Yes", previous_question_id=5) \
    .clarify_question_9_terms() \
    .has_either_you_or_your_partner_reached_state_pension_age("Yes", previous_question_id=7) \
    .clarify_question_10_terms() \
    .have_both_you_and_your_partner_reached_state_pension_age("No", previous_question_id=9) \
    .clarify_question_11_terms() \
    .are_you_currently_getting_pension_credit("Yes", previous_question_id=10) \
    .would_you_like_me_to_check_what_implications_there_are_with_other_benefits_if_you_were_apply_and_be_found_eligible("Yes") \
    .run()


@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_eligible_student_with_eligible_partner():
    await UniversalCreditScenario(
        short_description="Eligible: Full-time student living with eligible partner.",
        user_intro="I am a full-time student and my partner is eligible for Universal Credit.",
        user_should_be_eligible=True,
    ) \
    .clarify_question_1_terms() \
    .do_you_live_in_the_uk("Yes", previous_question_id=None) \
    .clarify_question_2_terms() \
    .are_you_aged_16_or_17("No", previous_question_id=1) \
    .clarify_question_3_terms() \
    .are_you_aged_18_or_over_but_under_state_pension_age("Yes", previous_question_id=2) \
    .clarify_question_4_terms() \
    .do_you_have_16000_or_less_in_money_savings_and_investments("Yes", previous_question_id=3) \
    .clarify_question_5_terms() \
    .are_you_an_eu_eea_or_swiss_citizen("No", previous_question_id=4) \
    .clarify_question_7_terms() \
    .do_you_live_with_a_partner("No", previous_question_id=5) \
    .clarify_question_12_terms() \
    .are_you_in_fulltime_education_or_training("Yes", previous_question_id=7) \
    .clarify_question_13_terms() \
    .do_you_live_with_a_partner_who_is_eligible_for_universal_credit("Yes", previous_question_id=12) \
    .would_you_like_me_to_check_what_implications_there_are_with_other_benefits_if_you_were_apply_and_be_found_eligible("Yes") \
    .run()

@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_eligible_student_with_child():
    await UniversalCreditScenario(
        short_description="Eligible: Full-time student responsible for a child.",
        user_intro="I am a full-time student with a young child checking my universal credit eligibility.",
        user_should_be_eligible=True,
    ) \
    .clarify_question_1_terms() \
    .do_you_live_in_the_uk("Yes", previous_question_id=None) \
    .clarify_question_2_terms() \
    .are_you_aged_16_or_17("No", previous_question_id=1) \
    .clarify_question_3_terms() \
    .are_you_aged_18_or_over_but_under_state_pension_age("Yes", previous_question_id=2) \
    .clarify_question_4_terms() \
    .do_you_have_16000_or_less_in_money_savings_and_investments("Yes", previous_question_id=3) \
    .clarify_question_5_terms() \
    .are_you_an_eu_eea_or_swiss_citizen("No", previous_question_id=4) \
    .clarify_question_7_terms() \
    .do_you_live_with_a_partner("No", previous_question_id=5) \
    .clarify_question_12_terms() \
    .are_you_in_fulltime_education_or_training("Yes", previous_question_id=7) \
    .clarify_question_13_terms() \
    .do_you_live_with_a_partner_who_is_eligible_for_universal_credit("No", previous_question_id=12) \
    .clarify_question_14_terms() \
    .are_you_responsible_for_a_child("Yes", previous_question_id=13) \
    .would_you_like_me_to_check_what_implications_there_are_with_other_benefits_if_you_were_apply_and_be_found_eligible("Yes") \
    .run()

@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_eligible_student_at_pension_age_with_younger_partner():
    await UniversalCreditScenario(
        short_description="Eligible: Full-time student at State Pension age with partner below State Pension age.",
        user_intro="I am a full-time student at State Pension age and my partner is younger, looking into universal credit.",
        user_should_be_eligible=True,
    ) \
    .clarify_question_1_terms() \
    .do_you_live_in_the_uk("Yes", previous_question_id=None) \
    .clarify_question_2_terms() \
    .are_you_aged_16_or_17("No", previous_question_id=1) \
    .clarify_question_3_terms() \
    .are_you_aged_18_or_over_but_under_state_pension_age("Yes", previous_question_id=2) \
    .clarify_question_4_terms() \
    .do_you_have_16000_or_less_in_money_savings_and_investments("Yes", previous_question_id=3) \
    .clarify_question_5_terms() \
    .are_you_an_eu_eea_or_swiss_citizen("No", previous_question_id=4) \
    .clarify_question_7_terms() \
    .do_you_live_with_a_partner("No", previous_question_id=5) \
    .clarify_question_12_terms() \
    .are_you_in_fulltime_education_or_training("Yes", previous_question_id=7) \
    .clarify_question_13_terms() \
    .do_you_live_with_a_partner_who_is_eligible_for_universal_credit("No", previous_question_id=12) \
    .clarify_question_14_terms() \
    .are_you_responsible_for_a_child("No", previous_question_id=13) \
    .clarify_question_15_terms() \
    .have_you_reached_state_pension_age_and_live_with_a_partner_who_is_below_state_pension_age("Yes", previous_question_id=14) \
    .would_you_like_me_to_check_what_implications_there_are_with_other_benefits_if_you_were_apply_and_be_found_eligible("Yes") \
    .run()


@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_eligible_student_with_migration_notice():
    await UniversalCreditScenario(
        short_description="Eligible: Full-time student with Migration Notice letter.",
        user_intro="I am a full-time student and received a Migration Notice letter about universal credit.",
        user_should_be_eligible=True,
    ) \
    .clarify_question_1_terms() \
    .do_you_live_in_the_uk("Yes", previous_question_id=None) \
    .clarify_question_2_terms() \
    .are_you_aged_16_or_17("No", previous_question_id=1) \
    .clarify_question_3_terms() \
    .are_you_aged_18_or_over_but_under_state_pension_age("Yes", previous_question_id=2) \
    .clarify_question_4_terms() \
    .do_you_have_16000_or_less_in_money_savings_and_investments("Yes", previous_question_id=3) \
    .clarify_question_5_terms() \
    .are_you_an_eu_eea_or_swiss_citizen("No", previous_question_id=4) \
    .clarify_question_7_terms() \
    .do_you_live_with_a_partner("No", previous_question_id=5) \
    .clarify_question_12_terms() \
    .are_you_in_fulltime_education_or_training("Yes", previous_question_id=7) \
    .clarify_question_13_terms() \
    .do_you_live_with_a_partner_who_is_eligible_for_universal_credit("No", previous_question_id=12) \
    .clarify_question_14_terms() \
    .are_you_responsible_for_a_child("No", previous_question_id=13) \
    .clarify_question_15_terms() \
    .have_you_reached_state_pension_age_and_live_with_a_partner_who_is_below_state_pension_age("No", previous_question_id=14) \
    .clarify_question_16_terms() \
    .have_you_received_a_migration_notice_letter_telling_you_to_move_to_universal_credit("Yes", previous_question_id=15) \
    .would_you_like_me_to_check_what_implications_there_are_with_other_benefits_if_you_were_apply_and_be_found_eligible("Yes") \
    .run()

@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_eligible_student_21_or_under_a_level_no_parental_support():
    await UniversalCreditScenario(
        short_description="Eligible: Student aged 21 or under, studying up to A-level, no parental support.",
        user_intro="I am 20 years old studying for my A-levels without parental support, seeking universal credit.",
        user_should_be_eligible=True,
    ) \
    .clarify_question_1_terms() \
    .do_you_live_in_the_uk("Yes", previous_question_id=None) \
    .clarify_question_2_terms() \
    .are_you_aged_16_or_17("No", previous_question_id=1) \
    .clarify_question_3_terms() \
    .are_you_aged_18_or_over_but_under_state_pension_age("Yes", previous_question_id=2) \
    .clarify_question_4_terms() \
    .do_you_have_16000_or_less_in_money_savings_and_investments("Yes", previous_question_id=3) \
    .clarify_question_5_terms() \
    .are_you_an_eu_eea_or_swiss_citizen("No", previous_question_id=4) \
    .clarify_question_7_terms() \
    .do_you_live_with_a_partner("No", previous_question_id=5) \
    .clarify_question_12_terms() \
    .are_you_in_fulltime_education_or_training("Yes", previous_question_id=7) \
    .clarify_question_13_terms() \
    .do_you_live_with_a_partner_who_is_eligible_for_universal_credit("No", previous_question_id=12) \
    .clarify_question_14_terms() \
    .are_you_responsible_for_a_child("No", previous_question_id=13) \
    .clarify_question_15_terms() \
    .have_you_reached_state_pension_age_and_live_with_a_partner_who_is_below_state_pension_age("No", previous_question_id=14) \
    .clarify_question_16_terms() \
    .have_you_received_a_migration_notice_letter_telling_you_to_move_to_universal_credit("No", previous_question_id=15) \
    .clarify_question_17_terms() \
    .are_you_21_or_under_studying_any_qualification_up_to_a_level_or_equivalent_and_do_not_have_parental_support("Yes", previous_question_id=16) \
    .would_you_like_me_to_check_what_implications_there_are_with_other_benefits_if_you_were_apply_and_be_found_eligible("Yes") \
    .run()

@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_eligible_parttime_student():
    await UniversalCreditScenario(
        short_description="Eligible: Part-time student.",
        user_intro="I am studying part-time and want to apply for universal credit.",
        user_should_be_eligible=True,
    ) \
    .clarify_question_1_terms() \
    .do_you_live_in_the_uk("Yes", previous_question_id=None) \
    .clarify_question_2_terms() \
    .are_you_aged_16_or_17("No", previous_question_id=1) \
    .clarify_question_3_terms() \
    .are_you_aged_18_or_over_but_under_state_pension_age("Yes", previous_question_id=2) \
    .clarify_question_4_terms() \
    .do_you_have_16000_or_less_in_money_savings_and_investments("Yes", previous_question_id=3) \
    .clarify_question_5_terms() \
    .are_you_an_eu_eea_or_swiss_citizen("No", previous_question_id=4) \
    .clarify_question_7_terms() \
    .do_you_live_with_a_partner("No", previous_question_id=5) \
    .clarify_question_12_terms() \
    .are_you_in_fulltime_education_or_training("Yes", previous_question_id=7) \
    .clarify_question_13_terms() \
    .do_you_live_with_a_partner_who_is_eligible_for_universal_credit("No", previous_question_id=12) \
    .clarify_question_14_terms() \
    .are_you_responsible_for_a_child("No", previous_question_id=13) \
    .clarify_question_15_terms() \
    .have_you_reached_state_pension_age_and_live_with_a_partner_who_is_below_state_pension_age("No", previous_question_id=14) \
    .clarify_question_16_terms() \
    .have_you_received_a_migration_notice_letter_telling_you_to_move_to_universal_credit("No", previous_question_id=15) \
    .clarify_question_17_terms() \
    .are_you_21_or_under_studying_any_qualification_up_to_a_level_or_equivalent_and_do_not_have_parental_support("No", previous_question_id=16) \
    .clarify_question_18_terms() \
    .are_you_studying_parttime("Yes", previous_question_id=17) \
    .would_you_like_me_to_check_what_implications_there_are_with_other_benefits_if_you_were_apply_and_be_found_eligible("Yes") \
    .run()


@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_eligible_student_course_with_no_finance_available():
    await UniversalCreditScenario(
        short_description="Eligible: Full-time student on course with no student loan or finance available.",
        user_intro="I am studying a course for which no student finance is available, can I claim universal credit?",
        user_should_be_eligible=True,
    ) \
    .clarify_question_1_terms() \
    .do_you_live_in_the_uk("Yes", previous_question_id=None) \
    .clarify_question_2_terms() \
    .are_you_aged_16_or_17("No", previous_question_id=1) \
    .clarify_question_3_terms() \
    .are_you_aged_18_or_over_but_under_state_pension_age("Yes", previous_question_id=2) \
    .clarify_question_4_terms() \
    .do_you_have_16000_or_less_in_money_savings_and_investments("Yes", previous_question_id=3) \
    .clarify_question_5_terms() \
    .are_you_an_eu_eea_or_swiss_citizen("No", previous_question_id=4) \
    .clarify_question_7_terms() \
    .do_you_live_with_a_partner("No", previous_question_id=5) \
    .clarify_question_12_terms() \
    .are_you_in_fulltime_education_or_training("Yes", previous_question_id=7) \
    .clarify_question_13_terms() \
    .do_you_live_with_a_partner_who_is_eligible_for_universal_credit("No", previous_question_id=12) \
    .clarify_question_14_terms() \
    .are_you_responsible_for_a_child("No", previous_question_id=13) \
    .clarify_question_15_terms() \
    .have_you_reached_state_pension_age_and_live_with_a_partner_who_is_below_state_pension_age("No", previous_question_id=14) \
    .clarify_question_16_terms() \
    .have_you_received_a_migration_notice_letter_telling_you_to_move_to_universal_credit("No", previous_question_id=15) \
    .clarify_question_17_terms() \
    .are_you_21_or_under_studying_any_qualification_up_to_a_level_or_equivalent_and_do_not_have_parental_support("No", previous_question_id=16) \
    .clarify_question_18_terms() \
    .are_you_studying_parttime("No", previous_question_id=17) \
    .clarify_question_19_terms() \
    .is_your_course_one_for_which_no_student_loan_or_finance_is_available("Yes", previous_question_id=18) \
    .would_you_like_me_to_check_what_implications_there_are_with_other_benefits_if_you_were_apply_and_be_found_eligible("Yes") \
    .run()

@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_eligible_student_with_disability_assessed_with_qualifying_benefit():
    await UniversalCreditScenario(
        short_description="Eligible: Full-time student with disability assessed before course and receiving qualifying benefit.",
        user_intro="I am a full-time student with limited capability for work, I receive PIP, and I want to check my universal credit eligibility.",
        user_should_be_eligible=True,
    ) \
    .clarify_question_1_terms() \
    .do_you_live_in_the_uk("Yes", previous_question_id=None) \
    .clarify_question_2_terms() \
    .are_you_aged_16_or_17("No", previous_question_id=1) \
    .clarify_question_3_terms() \
    .are_you_aged_18_or_over_but_under_state_pension_age("Yes", previous_question_id=2) \
    .clarify_question_4_terms() \
    .do_you_have_16000_or_less_in_money_savings_and_investments("Yes", previous_question_id=3) \
    .clarify_question_5_terms() \
    .are_you_an_eu_eea_or_swiss_citizen("No", previous_question_id=4) \
    .clarify_question_7_terms() \
    .do_you_live_with_a_partner("No", previous_question_id=5) \
    .clarify_question_12_terms() \
    .are_you_in_fulltime_education_or_training("Yes", previous_question_id=7) \
    .clarify_question_13_terms() \
    .do_you_live_with_a_partner_who_is_eligible_for_universal_credit("No", previous_question_id=12) \
    .clarify_question_14_terms() \
    .are_you_responsible_for_a_child("No", previous_question_id=13) \
    .clarify_question_15_terms() \
    .have_you_reached_state_pension_age_and_live_with_a_partner_who_is_below_state_pension_age("No", previous_question_id=14) \
    .clarify_question_16_terms() \
    .have_you_received_a_migration_notice_letter_telling_you_to_move_to_universal_credit("No", previous_question_id=15) \
    .clarify_question_17_terms() \
    .are_you_21_or_under_studying_any_qualification_up_to_a_level_or_equivalent_and_do_not_have_parental_support("No", previous_question_id=16) \
    .clarify_question_18_terms() \
    .are_you_studying_parttime("No", previous_question_id=17) \
    .clarify_question_19_terms() \
    .is_your_course_one_for_which_no_student_loan_or_finance_is_available("No", previous_question_id=18) \
    .clarify_question_21_terms() \
    .were_you_assessed_as_having_limited_capability_for_work_by_a_work_capability_assessment_before_starting_your_course("Yes", previous_question_id=19) \
    .clarify_question_22_terms() \
    .are_you_entitled_to_pip_dla_attendance_allowance_or_other_qualifying_disability_benefits("Yes", previous_question_id=21) \
    .would_you_like_me_to_check_what_implications_there_are_with_other_benefits_if_you_were_apply_and_be_found_eligible("Yes") \
    .run()

@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_eligible_armed_forces_stationed_abroad():
    await UniversalCreditScenario(
        short_description="Eligible: In armed forces and stationed abroad.",
        user_intro="I am in the armed forces stationed abroad checking if I can get universal credit.",
        user_should_be_eligible=True,
    ) \
    .clarify_question_1_terms() \
    .do_you_live_in_the_uk("Yes", previous_question_id=None) \
    .clarify_question_2_terms() \
    .are_you_aged_16_or_17("No", previous_question_id=1) \
    .clarify_question_3_terms() \
    .are_you_aged_18_or_over_but_under_state_pension_age("Yes", previous_question_id=2) \
    .clarify_question_4_terms() \
    .do_you_have_16000_or_less_in_money_savings_and_investments("Yes", previous_question_id=3) \
    .clarify_question_5_terms() \
    .are_you_an_eu_eea_or_swiss_citizen("No", previous_question_id=4) \
    .clarify_question_7_terms() \
    .do_you_live_with_a_partner("No", previous_question_id=5) \
    .clarify_question_12_terms() \
    .are_you_in_fulltime_education_or_training("No", previous_question_id=7) \
    .clarify_question_20_terms() \
    .do_you_have_a_disability_or_health_condition("No", previous_question_id=12) \
    .clarify_question_29_terms() \
    .are_you_in_the_armed_forces_and_stationed_abroad("Yes", previous_question_id=20) \
    .would_you_like_me_to_check_what_implications_there_are_with_other_benefits_if_you_were_apply_and_be_found_eligible("Yes") \
    .run()


@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_eligible_16_17_with_health_condition_medical_evidence():
    await UniversalCreditScenario(
        short_description="Eligible: Age 16-17 with health condition/disability and medical evidence.",
        user_intro="I am 16 years old with a health condition, have a fit note, and want to claim universal credit.",
        user_should_be_eligible=True,
    ) \
    .clarify_question_1_terms() \
    .do_you_live_in_the_uk("Yes", previous_question_id=None) \
    .clarify_question_2_terms() \
    .are_you_aged_16_or_17("Yes", previous_question_id=1) \
    .clarify_question_23_terms() \
    .do_you_have_a_health_condition_or_disability_with_medical_evidence_for_it("Yes", previous_question_id=2) \
    .would_you_like_me_to_check_what_implications_there_are_with_other_benefits_if_you_were_apply_and_be_found_eligible("Yes") \
    .run()

@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_eligible_16_17_caring_for_someone_with_disability_benefit():
    await UniversalCreditScenario(
        short_description="Eligible: Age 16-17 caring for someone who gets a health or disability-related benefit.",
        user_intro="I am 17 and care for my parent who receives disability benefits, seeking universal credit.",
        user_should_be_eligible=True,
    ) \
    .clarify_question_1_terms() \
    .do_you_live_in_the_uk("Yes", previous_question_id=None) \
    .clarify_question_2_terms() \
    .are_you_aged_16_or_17("Yes", previous_question_id=1) \
    .clarify_question_23_terms() \
    .do_you_have_a_health_condition_or_disability_with_medical_evidence_for_it("No", previous_question_id=2) \
    .clarify_question_24_terms() \
    .are_you_caring_for_someone_who_gets_a_health_or_disability_related_benefit("Yes", previous_question_id=23) \
    .would_you_like_me_to_check_what_implications_there_are_with_other_benefits_if_you_were_apply_and_be_found_eligible("Yes") \
    .run()

@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_eligible_16_17_nearing_end_of_life():
    await UniversalCreditScenario(
        short_description="Eligible: Age 16-17 nearing the end of life.",
        user_intro="I am 16, a medical professional has said I am nearing the end of life, and I need to apply for universal credit.",
        user_should_be_eligible=True,
    ) \
    .clarify_question_1_terms() \
    .do_you_live_in_the_uk("Yes", previous_question_id=None) \
    .clarify_question_2_terms() \
    .are_you_aged_16_or_17("Yes", previous_question_id=1) \
    .clarify_question_23_terms() \
    .do_you_have_a_health_condition_or_disability_with_medical_evidence_for_it("No", previous_question_id=2) \
    .clarify_question_24_terms() \
    .are_you_caring_for_someone_who_gets_a_health_or_disability_related_benefit("No", previous_question_id=23) \
    .clarify_question_25_terms() \
    .has_a_medical_professional_said_you_are_nearing_the_end_of_life("Yes", previous_question_id=24) \
    .would_you_like_me_to_check_what_implications_there_are_with_other_benefits_if_you_were_apply_and_be_found_eligible("Yes") \
    .run()


@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_eligible_16_17_with_child_single_person():
    await UniversalCreditScenario(
        short_description="Eligible: Age 16-17 responsible for a child as single person.",
        user_intro="I am 17, have a child, and want to see if I can get universal credit.",
        user_should_be_eligible=True,
    ) \
    .clarify_question_1_terms() \
    .do_you_live_in_the_uk("Yes", previous_question_id=None) \
    .clarify_question_2_terms() \
    .are_you_aged_16_or_17("Yes", previous_question_id=1) \
    .clarify_question_23_terms() \
    .do_you_have_a_health_condition_or_disability_with_medical_evidence_for_it("No", previous_question_id=2) \
    .clarify_question_24_terms() \
    .are_you_caring_for_someone_who_gets_a_health_or_disability_related_benefit("No", previous_question_id=23) \
    .clarify_question_25_terms() \
    .has_a_medical_professional_said_you_are_nearing_the_end_of_life("No", previous_question_id=24) \
    .clarify_question_14_terms() \
    .are_you_responsible_for_a_child("Yes", previous_question_id=25) \
    .would_you_like_me_to_check_what_implications_there_are_with_other_benefits_if_you_were_apply_and_be_found_eligible("Yes") \
    .run()

@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_eligible_16_17_pregnant_11_weeks():
    await UniversalCreditScenario(
        short_description="Eligible: Age 16-17 pregnant and expecting baby in next 11 weeks.",
        user_intro="I am 16, pregnant, expecting my baby in 10 weeks, and looking to claim universal credit.",
        user_should_be_eligible=True,
    ) \
    .clarify_question_1_terms() \
    .do_you_live_in_the_uk("Yes", previous_question_id=None) \
    .clarify_question_2_terms() \
    .are_you_aged_16_or_17("Yes", previous_question_id=1) \
    .clarify_question_23_terms() \
    .do_you_have_a_health_condition_or_disability_with_medical_evidence_for_it("No", previous_question_id=2) \
    .clarify_question_24_terms() \
    .are_you_caring_for_someone_who_gets_a_health_or_disability_related_benefit("No", previous_question_id=23) \
    .clarify_question_25_terms() \
    .has_a_medical_professional_said_you_are_nearing_the_end_of_life("No", previous_question_id=24) \
    .clarify_question_14_terms() \
    .are_you_responsible_for_a_child("No", previous_question_id=25) \
    .clarify_question_26_terms() \
    .are_you_pregnant_and_expecting_your_baby_in_the_next_11_weeks("Yes", previous_question_id=14) \
    .would_you_like_me_to_check_what_implications_there_are_with_other_benefits_if_you_were_apply_and_be_found_eligible("Yes") \
    .run()

@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_eligible_16_17_had_baby_15_weeks():
    await UniversalCreditScenario(
        short_description="Eligible: Age 16-17 had baby in last 15 weeks.",
        user_intro="I am 17, had a baby 10 weeks ago, and want to apply for universal credit.",
        user_should_be_eligible=True,
    ) \
    .clarify_question_1_terms() \
    .do_you_live_in_the_uk("Yes", previous_question_id=None) \
    .clarify_question_2_terms() \
    .are_you_aged_16_or_17("Yes", previous_question_id=1) \
    .clarify_question_23_terms() \
    .do_you_have_a_health_condition_or_disability_with_medical_evidence_for_it("No", previous_question_id=2) \
    .clarify_question_24_terms() \
    .are_you_caring_for_someone_who_gets_a_health_or_disability_related_benefit("No", previous_question_id=23) \
    .clarify_question_25_terms() \
    .has_a_medical_professional_said_you_are_nearing_the_end_of_life("No", previous_question_id=24) \
    .clarify_question_14_terms() \
    .are_you_responsible_for_a_child("No", previous_question_id=25) \
    .clarify_question_26_terms() \
    .are_you_pregnant_and_expecting_your_baby_in_the_next_11_weeks("No", previous_question_id=14) \
    .clarify_question_27_terms() \
    .have_you_had_a_baby_in_the_last_15_weeks("Yes", previous_question_id=26) \
    .would_you_like_me_to_check_what_implications_there_are_with_other_benefits_if_you_were_apply_and_be_found_eligible("Yes") \
    .run()


@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_eligible_16_17_without_parental_support():
    await UniversalCreditScenario(
        short_description="Eligible: Age 16-17 without parental support.",
        user_intro="I am 16, do not live with my parents, and want to apply for universal credit.",
        user_should_be_eligible=True,
    ) \
    .clarify_question_1_terms() \
    .do_you_live_in_the_uk("Yes", previous_question_id=None) \
    .clarify_question_2_terms() \
    .are_you_aged_16_or_17("Yes", previous_question_id=1) \
    .clarify_question_23_terms() \
    .do_you_have_a_health_condition_or_disability_with_medical_evidence_for_it("No", previous_question_id=2) \
    .clarify_question_24_terms() \
    .are_you_caring_for_someone_who_gets_a_health_or_disability_related_benefit("No", previous_question_id=23) \
    .clarify_question_25_terms() \
    .has_a_medical_professional_said_you_are_nearing_the_end_of_life("No", previous_question_id=24) \
    .clarify_question_14_terms() \
    .are_you_responsible_for_a_child("No", previous_question_id=25) \
    .clarify_question_26_terms() \
    .are_you_pregnant_and_expecting_your_baby_in_the_next_11_weeks("No", previous_question_id=14) \
    .clarify_question_27_terms() \
    .have_you_had_a_baby_in_the_last_15_weeks("No", previous_question_id=26) \
    .clarify_question_28_terms() \
    .do_you_have_parental_support("No", previous_question_id=27) \
    .would_you_like_me_to_check_what_implications_there_are_with_other_benefits_if_you_were_apply_and_be_found_eligible("Yes") \
    .run()

@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_eligible_with_disability_not_in_education():
    await UniversalCreditScenario(
        short_description="Eligible: Has disability or health condition, not in full-time education.",
        user_intro="I am 35 years old with a disability, not studying, and looking to apply for universal credit.",
        user_should_be_eligible=True,
    ) \
    .clarify_question_1_terms() \
    .do_you_live_in_the_uk("Yes", previous_question_id=None) \
    .clarify_question_2_terms() \
    .are_you_aged_16_or_17("No", previous_question_id=1) \
    .clarify_question_3_terms() \
    .are_you_aged_18_or_over_but_under_state_pension_age("Yes", previous_question_id=2) \
    .clarify_question_4_terms() \
    .do_you_have_16000_or_less_in_money_savings_and_investments("Yes", previous_question_id=3) \
    .clarify_question_5_terms() \
    .are_you_an_eu_eea_or_swiss_citizen("No", previous_question_id=4) \
    .clarify_question_7_terms() \
    .do_you_live_with_a_partner("No", previous_question_id=5) \
    .clarify_question_12_terms() \
    .are_you_in_fulltime_education_or_training("No", previous_question_id=7) \
    .clarify_question_20_terms() \
    .do_you_have_a_disability_or_health_condition("Yes", previous_question_id=12) \
    .clarify_question_29_terms() \
    .are_you_in_the_armed_forces_and_stationed_abroad("No", previous_question_id=20) \
    .would_you_like_me_to_check_what_implications_there_are_with_other_benefits_if_you_were_apply_and_be_found_eligible("Yes") \
    .run()