import pytest
from tests.scenario.pip import PipScenario

@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_pip_happy_path():
    await PipScenario(
        short_description="Eligibile",
        user_should_be_eligible=True,
        user_intro="I've just been diagnosed with type 1 diabetes"
    ) \
    .how_old_are_you("18 to 67") \
    .do_you_live_in_England_or_Wales("Yes") \
    .have_you_lived_in_the_UK_for_at_least_2_of_last_3_years("Yes") \
    .have_you_had_a_health_condition_for_3_months_or_more_and_is_it_expected_to_continue_for_more_than_9_months_or_are_you_not_expected_to_live_more_than_12_months("Yes") \
    .clarify_health_condition_tasks_terms() \
    .do_you_need_help_or_struggle_with_any_of_the_following_tasks_for_over_half_of_any_given_day("Yes") \
    .clarify_health_condition_tasks_qualification_terms() \
    .with_respect_to_those_tasks_do_any_of_the_following_apply("Yes") \
    .would_you_like_me_to_check_what_implications_there_are_with_other_benefits_if_you_were_apply_and_be_found_eligible("Yes") \
    .run()

@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_pip_too_old():
    await PipScenario(
        short_description="Too old",
        user_should_be_eligible=False,
        user_intro="I've just been diagnosed with type 1 diabetes",
        decision_addendum="but they should look at 'Attendance Allowance' instead"
    ) \
    .how_old_are_you("68+") \
    .run()

@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_pip_too_young():
    await PipScenario(
        short_description="Too young",
        user_intro="I've just been diagnosed with type 1 diabetes",
        user_should_be_eligible=False
    ) \
    .how_old_are_you("17-") \
    .run()

@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_pip_residence_country_ineligible():
    await PipScenario(
        short_description="Residence country issue",
        user_intro="I've just been diagnosed with type 1 diabetes",
        user_should_be_eligible=False
    ) \
    .how_old_are_you("18 to 67") \
    .do_you_live_in_England_or_Wales("No") \
    .run()

@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_pip_residence_time_ineligible():
    await PipScenario(
        short_description="Residence time too short",
        user_intro="I've just been diagnosed with type 1 diabetes",
        user_should_be_eligible=False
    ) \
    .how_old_are_you("18 to 67") \
    .do_you_live_in_England_or_Wales("Yes") \
    .have_you_lived_in_the_UK_for_at_least_2_of_last_3_years("No") \
    .run()

@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_pip_health_condition_time_ineligible():
    
    await PipScenario(
        short_description="Health condition time issue",
        user_should_be_eligible=False,
        user_intro="I've just been diagnosed with type 1 diabetes",
    ) \
    .how_old_are_you("18 to 67") \
    .do_you_live_in_England_or_Wales("Yes") \
    .have_you_lived_in_the_UK_for_at_least_2_of_last_3_years("Yes") \
    .have_you_had_a_health_condition_for_3_months_or_more_and_is_it_expected_to_continue_for_more_than_9_months_or_are_you_not_expected_to_live_more_than_12_months("No") \
    .run()

@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_pip_health_condition_issue_ineligible():

    await PipScenario(
        short_description="Doesn't need help with daily tasks",
        user_should_be_eligible=False,
        user_intro="I've just been diagnosed with type 1 diabetes"
    ) \
    .how_old_are_you("18 to 67") \
    .do_you_live_in_England_or_Wales("Yes") \
    .have_you_lived_in_the_UK_for_at_least_2_of_last_3_years("Yes") \
    .have_you_had_a_health_condition_for_3_months_or_more_and_is_it_expected_to_continue_for_more_than_9_months_or_are_you_not_expected_to_live_more_than_12_months("Yes") \
    .do_you_need_help_or_struggle_with_any_of_the_following_tasks_for_over_half_of_any_given_day("No") \
    .run()

@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_pip_health_condition_issue_qualification_ineligible():

    await PipScenario(
        short_description="No health issue qualifiers apply",
        user_should_be_eligible=False,
        user_intro="I've just been diagnosed with type 1 diabetes"
    ) \
    .how_old_are_you("18 to 67") \
    .do_you_live_in_England_or_Wales("Yes") \
    .have_you_lived_in_the_UK_for_at_least_2_of_last_3_years("Yes") \
    .have_you_had_a_health_condition_for_3_months_or_more_and_is_it_expected_to_continue_for_more_than_9_months_or_are_you_not_expected_to_live_more_than_12_months("Yes") \
    .do_you_need_help_or_struggle_with_any_of_the_following_tasks_for_over_half_of_any_given_day("Yes") \
    .with_respect_to_those_tasks_do_any_of_the_following_apply("No") \
    .run()