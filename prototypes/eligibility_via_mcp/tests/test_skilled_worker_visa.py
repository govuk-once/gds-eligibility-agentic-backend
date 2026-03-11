import pytest
from tests.scenario.skilled_worker_visa import SkilledWorkerVisaScenario

@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_ineligible_no_job_offer():
    await SkilledWorkerVisaScenario(
        short_description="Ineligible: User does not have a job offer.",
        user_intro="I am from India and I am interested in working in the UK.",
        user_should_be_eligible=False,
    ) \
    .clarify_question_1_terms() \
    .are_you_applying_for_the_first_time_extending_or_switching("Applying for the first time from outside the UK", previous_question_id=None) \
    .clarify_question_2_terms() \
    .do_you_have_a_confirmed_job_offer("No", previous_question_id=1) \
    .run()

@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_ineligible_employer_not_approved():
    await SkilledWorkerVisaScenario(
        short_description="Ineligible: Employer is not a licensed sponsor.",
        user_intro="I am from Brazil, I have a job offer to work in the UK.",
        user_should_be_eligible=False,
    ) \
    .clarify_question_1_terms() \
    .are_you_applying_for_the_first_time_extending_or_switching("Applying for the first time from outside the UK", previous_question_id=None) \
    .clarify_question_2_terms() \
    .do_you_have_a_confirmed_job_offer("Yes", previous_question_id=1) \
    .clarify_question_3_terms() \
    .has_your_employer_been_approved_by_home_office("No", previous_question_id=2) \
    .run()

@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_ineligible_no_certificate_of_sponsorship():
    await SkilledWorkerVisaScenario(
        short_description="Ineligible: User does not have certificate of sponsorship.",
        user_intro="I am from Nigeria, I have been offered a job in the UK.",
        user_should_be_eligible=False,
    ) \
    .clarify_question_1_terms() \
    .are_you_applying_for_the_first_time_extending_or_switching("Applying for the first time from outside the UK", previous_question_id=None) \
    .clarify_question_2_terms() \
    .do_you_have_a_confirmed_job_offer("Yes", previous_question_id=1) \
    .clarify_question_3_terms() \
    .has_your_employer_been_approved_by_home_office("Yes", previous_question_id=2) \
    .clarify_question_4_terms() \
    .do_you_have_certificate_of_sponsorship("No", previous_question_id=3) \
    .run()

@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_ineligible_occupation_code_unknown():
    await SkilledWorkerVisaScenario(
        short_description="Ineligible: User doesn't know their occupation code.",
        user_intro="I am from Pakistan, I have a job offer and certificate of sponsorship.",
        user_should_be_eligible=False,
    ) \
    .clarify_question_1_terms() \
    .are_you_applying_for_the_first_time_extending_or_switching("Applying for the first time from outside the UK", previous_question_id=None) \
    .clarify_question_2_terms() \
    .do_you_have_a_confirmed_job_offer("Yes", previous_question_id=1) \
    .clarify_question_3_terms() \
    .has_your_employer_been_approved_by_home_office("Yes", previous_question_id=2) \
    .clarify_question_4_terms() \
    .do_you_have_certificate_of_sponsorship("Yes", previous_question_id=3) \
    .clarify_question_5_terms() \
    .do_you_know_4_digit_occupation_code("No", previous_question_id=4) \
    .run()

@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_ineligible_occupation_not_eligible():
    await SkilledWorkerVisaScenario(
        short_description="Ineligible: Occupation code is not on the eligible list.",
        user_intro="I am from South Africa, I have a job offer for a role that may not be eligible.",
        user_should_be_eligible=False,
    ) \
    .clarify_question_1_terms() \
    .are_you_applying_for_the_first_time_extending_or_switching("Applying for the first time from outside the UK", previous_question_id=None) \
    .clarify_question_2_terms() \
    .do_you_have_a_confirmed_job_offer("Yes", previous_question_id=1) \
    .clarify_question_3_terms() \
    .has_your_employer_been_approved_by_home_office("Yes", previous_question_id=2) \
    .clarify_question_4_terms() \
    .do_you_have_certificate_of_sponsorship("Yes", previous_question_id=3) \
    .clarify_question_5_terms() \
    .do_you_know_4_digit_occupation_code("Yes", previous_question_id=4) \
    .clarify_question_6_terms() \
    .is_occupation_code_listed_in_eligible_jobs("No", previous_question_id=5) \
    .run()

@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_ineligible_medium_skilled_not_on_lists():
    await SkilledWorkerVisaScenario(
        short_description="Ineligible: Medium skilled job not on immigration salary or shortage list.",
        user_intro="I am from Philippines, I have a medium skilled job offer.",
        user_should_be_eligible=False,
    ) \
    .clarify_question_1_terms() \
    .are_you_applying_for_the_first_time_extending_or_switching("Applying for the first time from outside the UK", previous_question_id=None) \
    .clarify_question_2_terms() \
    .do_you_have_a_confirmed_job_offer("Yes", previous_question_id=1) \
    .clarify_question_3_terms() \
    .has_your_employer_been_approved_by_home_office("Yes", previous_question_id=2) \
    .clarify_question_4_terms() \
    .do_you_have_certificate_of_sponsorship("Yes", previous_question_id=3) \
    .clarify_question_5_terms() \
    .do_you_know_4_digit_occupation_code("Yes", previous_question_id=4) \
    .clarify_question_6_terms() \
    .is_occupation_code_listed_in_eligible_jobs("Yes", previous_question_id=5) \
    .clarify_question_7_terms() \
    .is_occupation_code_higher_or_medium_skilled("Medium skilled", previous_question_id=6) \
    .clarify_question_9_terms() \
    .is_job_on_immigration_salary_or_shortage_list("No", previous_question_id=7) \
    .run()

@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_ineligible_care_worker_employer_not_cqc_registered():
    await SkilledWorkerVisaScenario(
        short_description="Ineligible: Care worker employer not registered with CQC.",
        user_intro="I am from Zimbabwe, I have a care worker job offer in England.",
        user_should_be_eligible=False,
    ) \
    .clarify_question_1_terms() \
    .are_you_applying_for_the_first_time_extending_or_switching("Applying for the first time from outside the UK", previous_question_id=None) \
    .clarify_question_2_terms() \
    .do_you_have_a_confirmed_job_offer("Yes", previous_question_id=1) \
    .clarify_question_3_terms() \
    .has_your_employer_been_approved_by_home_office("Yes", previous_question_id=2) \
    .clarify_question_4_terms() \
    .do_you_have_certificate_of_sponsorship("Yes", previous_question_id=3) \
    .clarify_question_5_terms() \
    .do_you_know_4_digit_occupation_code("Yes", previous_question_id=4) \
    .clarify_question_6_terms() \
    .is_occupation_code_listed_in_eligible_jobs("Yes", previous_question_id=5) \
    .clarify_question_7_terms() \
    .is_occupation_code_higher_or_medium_skilled("Higher skilled", previous_question_id=6) \
    .for_higher_skilled_jobs_continue("Continue", previous_question_id=7) \
    .clarify_question_10_terms() \
    .are_you_applying_for_care_worker_role("Yes", previous_question_id=8) \
    .clarify_question_11_terms() \
    .is_employer_registered_with_cqc("No", previous_question_id=10) \
    .run()

@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_ineligible_salary_below_33400():
    await SkilledWorkerVisaScenario(
        short_description="Ineligible: Salary is below £33,400 minimum threshold.",
        user_intro="I am from Bangladesh, I have a job offer with a salary of £30,000 per year.",
        user_should_be_eligible=False,
    ) \
    .clarify_question_1_terms() \
    .are_you_applying_for_the_first_time_extending_or_switching("Applying for the first time from outside the UK", previous_question_id=None) \
    .clarify_question_2_terms() \
    .do_you_have_a_confirmed_job_offer("Yes", previous_question_id=1) \
    .clarify_question_3_terms() \
    .has_your_employer_been_approved_by_home_office("Yes", previous_question_id=2) \
    .clarify_question_4_terms() \
    .do_you_have_certificate_of_sponsorship("Yes", previous_question_id=3) \
    .clarify_question_5_terms() \
    .do_you_know_4_digit_occupation_code("Yes", previous_question_id=4) \
    .clarify_question_6_terms() \
    .is_occupation_code_listed_in_eligible_jobs("Yes", previous_question_id=5) \
    .clarify_question_7_terms() \
    .is_occupation_code_higher_or_medium_skilled("Higher skilled", previous_question_id=6) \
    .for_higher_skilled_jobs_continue("Continue", previous_question_id=7) \
    .clarify_question_10_terms() \
    .are_you_applying_for_care_worker_role("No", previous_question_id=8) \
    .clarify_question_12_terms() \
    .when_did_you_receive_cos("On or after 4 April 2024", previous_question_id=10) \
    .clarify_question_13_terms() \
    .what_is_your_annual_salary("£30,000", previous_question_id=12) \
    .clarify_question_14_terms() \
    .is_job_in_healthcare_or_education("No", previous_question_id=13) \
    .clarify_question_20_terms() \
    .what_is_standard_going_rate_for_occupation("£45,000", previous_question_id=14) \
    .is_salary_at_least_41700_and_going_rate("No", previous_question_id=20) \
    .is_salary_at_least_33400("No", previous_question_id=21) \
    .run()

@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_ineligible_no_reduced_salary_qualification():
    await SkilledWorkerVisaScenario(
        short_description="Ineligible: Salary £35,000 doesn't meet standard threshold and no reduced salary qualification.",
        user_intro="I am from China, I have a job offer with a salary of £35,000 per year.",
        user_should_be_eligible=False,
    ) \
    .clarify_question_1_terms() \
    .are_you_applying_for_the_first_time_extending_or_switching("Applying for the first time from outside the UK", previous_question_id=None) \
    .clarify_question_2_terms() \
    .do_you_have_a_confirmed_job_offer("Yes", previous_question_id=1) \
    .clarify_question_3_terms() \
    .has_your_employer_been_approved_by_home_office("Yes", previous_question_id=2) \
    .clarify_question_4_terms() \
    .do_you_have_certificate_of_sponsorship("Yes", previous_question_id=3) \
    .clarify_question_5_terms() \
    .do_you_know_4_digit_occupation_code("Yes", previous_question_id=4) \
    .clarify_question_6_terms() \
    .is_occupation_code_listed_in_eligible_jobs("Yes", previous_question_id=5) \
    .clarify_question_7_terms() \
    .is_occupation_code_higher_or_medium_skilled("Higher skilled", previous_question_id=6) \
    .for_higher_skilled_jobs_continue("Continue", previous_question_id=7) \
    .clarify_question_10_terms() \
    .are_you_applying_for_care_worker_role("No", previous_question_id=8) \
    .clarify_question_12_terms() \
    .when_did_you_receive_cos("On or after 4 April 2024", previous_question_id=10) \
    .clarify_question_13_terms() \
    .what_is_your_annual_salary("£35,000", previous_question_id=12) \
    .clarify_question_14_terms() \
    .is_job_in_healthcare_or_education("No", previous_question_id=13) \
    .clarify_question_20_terms() \
    .what_is_standard_going_rate_for_occupation("£42,000", previous_question_id=14) \
    .is_salary_at_least_41700_and_going_rate("No", previous_question_id=20) \
    .is_salary_at_least_33400("Yes", previous_question_id=21) \
    .is_job_on_immigration_salary_list("No", previous_question_id=22) \
    .are_you_under_26("No", previous_question_id=23) \
    .are_you_current_or_recent_student_visa_holder("No", previous_question_id=25) \
    .are_you_current_or_recent_graduate_visa_holder("No", previous_question_id=27) \
    .working_towards_uk_regulated_profession("No", previous_question_id=29) \
    .working_towards_chartered_status("No", previous_question_id=31) \
    .do_you_have_phd_relevant_to_job("No", previous_question_id=33) \
    .working_in_postdoctoral_position("No", previous_question_id=35) \
    .run()

@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_eligible_standard_salary_with_maintenance_funds():
    await SkilledWorkerVisaScenario(
        short_description="Eligible: Meets standard salary threshold with maintenance funds.",
        user_intro="I am from Japan, I have a software engineering job offer paying £50,000 per year.",
        user_should_be_eligible=True,
    ) \
    .clarify_question_1_terms() \
    .are_you_applying_for_the_first_time_extending_or_switching("Applying for the first time from outside the UK", previous_question_id=None) \
    .clarify_question_2_terms() \
    .do_you_have_a_confirmed_job_offer("Yes", previous_question_id=1) \
    .clarify_question_3_terms() \
    .has_your_employer_been_approved_by_home_office("Yes", previous_question_id=2) \
    .clarify_question_4_terms() \
    .do_you_have_certificate_of_sponsorship("Yes", previous_question_id=3) \
    .clarify_question_5_terms() \
    .do_you_know_4_digit_occupation_code("Yes", previous_question_id=4) \
    .clarify_question_6_terms() \
    .is_occupation_code_listed_in_eligible_jobs("Yes", previous_question_id=5) \
    .clarify_question_7_terms() \
    .is_occupation_code_higher_or_medium_skilled("Higher skilled", previous_question_id=6) \
    .for_higher_skilled_jobs_continue("Continue", previous_question_id=7) \
    .clarify_question_10_terms() \
    .are_you_applying_for_care_worker_role("No", previous_question_id=8) \
    .clarify_question_12_terms() \
    .when_did_you_receive_cos("On or after 4 April 2024", previous_question_id=10) \
    .clarify_question_13_terms() \
    .what_is_your_annual_salary("£50,000", previous_question_id=12) \
    .clarify_question_14_terms() \
    .is_job_in_healthcare_or_education("No", previous_question_id=13) \
    .clarify_question_20_terms() \
    .what_is_standard_going_rate_for_occupation("£45,000", previous_question_id=14) \
    .is_salary_at_least_41700_and_going_rate("Yes", previous_question_id=20) \
    .clarify_question_42_terms() \
    .are_you_from_english_speaking_country("No", previous_question_id=21) \
    .are_you_healthcare_professional_with_english_assessment("No", previous_question_id=42) \
    .have_you_proved_english_in_previous_visa("No", previous_question_id=43) \
    .can_you_prove_english_knowledge("Yes", previous_question_id=44) \
    .clarify_question_46_terms_ecctis() \
    .which_method_to_prove_english("Degree from non-UK institution taught in English with Ecctis confirmation", previous_question_id=45) \
    .clarify_question_48_terms() \
    .can_you_pay_application_fee("Yes", previous_question_id=46) \
    .clarify_question_49_terms() \
    .can_you_pay_healthcare_surcharge("Yes", previous_question_id=48) \
    .clarify_question_50_terms() \
    .do_you_have_1270_in_bank_account("Yes", previous_question_id=49) \
    .run()

@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_eligible_standard_salary_employer_certifies_maintenance():
    await SkilledWorkerVisaScenario(
        short_description="Eligible: Meets standard salary threshold, employer certifies maintenance.",
        user_intro="I am from Singapore, I have a data scientist job offer paying £55,000 per year.",
        user_should_be_eligible=True,
    ) \
    .clarify_question_1_terms() \
    .are_you_applying_for_the_first_time_extending_or_switching("Applying for the first time from outside the UK", previous_question_id=None) \
    .clarify_question_2_terms() \
    .do_you_have_a_confirmed_job_offer("Yes", previous_question_id=1) \
    .clarify_question_3_terms() \
    .has_your_employer_been_approved_by_home_office("Yes", previous_question_id=2) \
    .clarify_question_4_terms() \
    .do_you_have_certificate_of_sponsorship("Yes", previous_question_id=3) \
    .clarify_question_5_terms() \
    .do_you_know_4_digit_occupation_code("Yes", previous_question_id=4) \
    .clarify_question_6_terms() \
    .is_occupation_code_listed_in_eligible_jobs("Yes", previous_question_id=5) \
    .clarify_question_7_terms() \
    .is_occupation_code_higher_or_medium_skilled("Higher skilled", previous_question_id=6) \
    .for_higher_skilled_jobs_continue("Continue", previous_question_id=7) \
    .clarify_question_10_terms() \
    .are_you_applying_for_care_worker_role("No", previous_question_id=8) \
    .clarify_question_12_terms() \
    .when_did_you_receive_cos("On or after 4 April 2024", previous_question_id=10) \
    .clarify_question_13_terms() \
    .what_is_your_annual_salary("£55,000", previous_question_id=12) \
    .clarify_question_14_terms() \
    .is_job_in_healthcare_or_education("No", previous_question_id=13) \
    .clarify_question_20_terms() \
    .what_is_standard_going_rate_for_occupation("£48,000", previous_question_id=14) \
    .is_salary_at_least_41700_and_going_rate("Yes", previous_question_id=20) \
    .clarify_question_42_terms() \
    .are_you_from_english_speaking_country("No", previous_question_id=21) \
    .are_you_healthcare_professional_with_english_assessment("No", previous_question_id=42) \
    .have_you_proved_english_in_previous_visa("No", previous_question_id=43) \
    .can_you_prove_english_knowledge("Yes", previous_question_id=44) \
    .clarify_question_47_terms_selt() \
    .which_method_to_prove_english("Approved SELT at level B2 or higher", previous_question_id=45) \
    .can_you_pass_selt_at_b2("Yes", previous_question_id=46) \
    .clarify_question_48_terms() \
    .can_you_pay_application_fee("Yes", previous_question_id=47) \
    .clarify_question_49_terms() \
    .can_you_pay_healthcare_surcharge("Yes", previous_question_id=48) \
    .clarify_question_50_terms() \
    .do_you_have_1270_in_bank_account("No", previous_question_id=49) \
    .clarify_question_51_terms() \
    .can_employer_certify_maintenance("Yes", previous_question_id=50) \
    .run()

@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_eligible_english_speaking_country_national():
    await SkilledWorkerVisaScenario(
        short_description="Eligible: From USA (English-speaking country), exempt from English proof.",
        user_intro="I am from the United States, I have a management consultant job offer paying £60,000 per year.",
        user_should_be_eligible=True,
    ) \
    .clarify_question_1_terms() \
    .are_you_applying_for_the_first_time_extending_or_switching("Applying for the first time from outside the UK", previous_question_id=None) \
    .clarify_question_2_terms() \
    .do_you_have_a_confirmed_job_offer("Yes", previous_question_id=1) \
    .clarify_question_3_terms() \
    .has_your_employer_been_approved_by_home_office("Yes", previous_question_id=2) \
    .clarify_question_4_terms() \
    .do_you_have_certificate_of_sponsorship("Yes", previous_question_id=3) \
    .clarify_question_5_terms() \
    .do_you_know_4_digit_occupation_code("Yes", previous_question_id=4) \
    .clarify_question_6_terms() \
    .is_occupation_code_listed_in_eligible_jobs("Yes", previous_question_id=5) \
    .clarify_question_7_terms() \
    .is_occupation_code_higher_or_medium_skilled("Higher skilled", previous_question_id=6) \
    .for_higher_skilled_jobs_continue("Continue", previous_question_id=7) \
    .clarify_question_10_terms() \
    .are_you_applying_for_care_worker_role("No", previous_question_id=8) \
    .clarify_question_12_terms() \
    .when_did_you_receive_cos("On or after 4 April 2024", previous_question_id=10) \
    .clarify_question_13_terms() \
    .what_is_your_annual_salary("£60,000", previous_question_id=12) \
    .clarify_question_14_terms() \
    .is_job_in_healthcare_or_education("No", previous_question_id=13) \
    .clarify_question_20_terms() \
    .what_is_standard_going_rate_for_occupation("£50,000", previous_question_id=14) \
    .is_salary_at_least_41700_and_going_rate("Yes", previous_question_id=20) \
    .clarify_question_42_terms() \
    .are_you_from_english_speaking_country("Yes", previous_question_id=21) \
    .clarify_question_48_terms() \
    .can_you_pay_application_fee("Yes", previous_question_id=42) \
    .clarify_question_49_terms() \
    .can_you_pay_healthcare_surcharge("Yes", previous_question_id=48) \
    .clarify_question_50_terms() \
    .do_you_have_1270_in_bank_account("Yes", previous_question_id=49) \
    .run()

@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_eligible_under_26_reduced_salary():
    await SkilledWorkerVisaScenario(
        short_description="Eligible: Under 26 with 70% of going rate salary.",
        user_intro="I am from France, I am 24 years old, and I have a junior developer job offer paying £35,000 per year.",
        user_should_be_eligible=True,
    ) \
    .clarify_question_1_terms() \
    .are_you_applying_for_the_first_time_extending_or_switching("Applying for the first time from outside the UK", previous_question_id=None) \
    .clarify_question_2_terms() \
    .do_you_have_a_confirmed_job_offer("Yes", previous_question_id=1) \
    .clarify_question_3_terms() \
    .has_your_employer_been_approved_by_home_office("Yes", previous_question_id=2) \
    .clarify_question_4_terms() \
    .do_you_have_certificate_of_sponsorship("Yes", previous_question_id=3) \
    .clarify_question_5_terms() \
    .do_you_know_4_digit_occupation_code("Yes", previous_question_id=4) \
    .clarify_question_6_terms() \
    .is_occupation_code_listed_in_eligible_jobs("Yes", previous_question_id=5) \
    .clarify_question_7_terms() \
    .is_occupation_code_higher_or_medium_skilled("Higher skilled", previous_question_id=6) \
    .for_higher_skilled_jobs_continue("Continue", previous_question_id=7) \
    .clarify_question_10_terms() \
    .are_you_applying_for_care_worker_role("No", previous_question_id=8) \
    .clarify_question_12_terms() \
    .when_did_you_receive_cos("On or after 4 April 2024", previous_question_id=10) \
    .clarify_question_13_terms() \
    .what_is_your_annual_salary("£35,000", previous_question_id=12) \
    .clarify_question_14_terms() \
    .is_job_in_healthcare_or_education("No", previous_question_id=13) \
    .clarify_question_20_terms() \
    .what_is_standard_going_rate_for_occupation("£48,000", previous_question_id=14) \
    .is_salary_at_least_41700_and_going_rate("No", previous_question_id=20) \
    .is_salary_at_least_33400("Yes", previous_question_id=21) \
    .is_job_on_immigration_salary_list("No", previous_question_id=22) \
    .are_you_under_26("Yes", previous_question_id=23) \
    .is_salary_70_percent_going_rate_under_26("Yes", previous_question_id=25) \
    .clarify_question_41_terms() \
    .understand_4_year_limit("Yes, I understand", previous_question_id=26) \
    .clarify_question_42_terms() \
    .are_you_from_english_speaking_country("No", previous_question_id=41) \
    .are_you_healthcare_professional_with_english_assessment("No", previous_question_id=42) \
    .have_you_proved_english_in_previous_visa("No", previous_question_id=43) \
    .can_you_prove_english_knowledge("Yes", previous_question_id=44) \
    .which_method_to_prove_english("Degree from UK institution taught in English", previous_question_id=45) \
    .clarify_question_48_terms() \
    .can_you_pay_application_fee("Yes", previous_question_id=46) \
    .clarify_question_49_terms() \
    .can_you_pay_healthcare_surcharge("Yes", previous_question_id=48) \
    .clarify_question_50_terms() \
    .do_you_have_1270_in_bank_account("Yes", previous_question_id=49) \
    .run()

@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_eligible_stem_phd_reduced_salary():
    await SkilledWorkerVisaScenario(
        short_description="Eligible: STEM PhD holder with 80% of going rate salary.",
        user_intro="I am from Russia, I have a PhD in Computer Science and a research scientist job offer paying £40,000 per year.",
        user_should_be_eligible=True,
    ) \
    .clarify_question_1_terms() \
    .are_you_applying_for_the_first_time_extending_or_switching("Applying for the first time from outside the UK", previous_question_id=None) \
    .clarify_question_2_terms() \
    .do_you_have_a_confirmed_job_offer("Yes", previous_question_id=1) \
    .clarify_question_3_terms() \
    .has_your_employer_been_approved_by_home_office("Yes", previous_question_id=2) \
    .clarify_question_4_terms() \
    .do_you_have_certificate_of_sponsorship("Yes", previous_question_id=3) \
    .clarify_question_5_terms() \
    .do_you_know_4_digit_occupation_code("Yes", previous_question_id=4) \
    .clarify_question_6_terms() \
    .is_occupation_code_listed_in_eligible_jobs("Yes", previous_question_id=5) \
    .clarify_question_7_terms() \
    .is_occupation_code_higher_or_medium_skilled("Higher skilled", previous_question_id=6) \
    .for_higher_skilled_jobs_continue("Continue", previous_question_id=7) \
    .clarify_question_10_terms() \
    .are_you_applying_for_care_worker_role("No", previous_question_id=8) \
    .clarify_question_12_terms() \
    .when_did_you_receive_cos("On or after 4 April 2024", previous_question_id=10) \
    .clarify_question_13_terms() \
    .what_is_your_annual_salary("£40,000", previous_question_id=12) \
    .clarify_question_14_terms() \
    .is_job_in_healthcare_or_education("No", previous_question_id=13) \
    .clarify_question_20_terms() \
    .what_is_standard_going_rate_for_occupation("£50,000", previous_question_id=14) \
    .is_salary_at_least_41700_and_going_rate("No", previous_question_id=20) \
    .is_salary_at_least_33400("Yes", previous_question_id=21) \
    .is_job_on_immigration_salary_list("No", previous_question_id=22) \
    .are_you_under_26("No", previous_question_id=23) \
    .are_you_current_or_recent_student_visa_holder("No", previous_question_id=25) \
    .are_you_current_or_recent_graduate_visa_holder("No", previous_question_id=27) \
    .working_towards_uk_regulated_profession("No", previous_question_id=29) \
    .working_towards_chartered_status("No", previous_question_id=31) \
    .clarify_question_35_terms() \
    .do_you_have_phd_relevant_to_job("Yes", previous_question_id=33) \
    .clarify_question_36_terms() \
    .is_phd_in_stem_subject("Yes (STEM PhD)", previous_question_id=35) \
    .is_salary_80_percent_going_rate_stem_phd("Yes", previous_question_id=36) \
    .clarify_question_42_terms() \
    .are_you_from_english_speaking_country("No", previous_question_id=37) \
    .are_you_healthcare_professional_with_english_assessment("No", previous_question_id=42) \
    .have_you_proved_english_in_previous_visa("No", previous_question_id=43) \
    .can_you_prove_english_knowledge("Yes", previous_question_id=44) \
    .which_method_to_prove_english("Approved SELT at level B2 or higher", previous_question_id=45) \
    .can_you_pass_selt_at_b2("Yes", previous_question_id=46) \
    .clarify_question_48_terms() \
    .can_you_pay_application_fee("Yes", previous_question_id=47) \
    .clarify_question_49_terms() \
    .can_you_pay_healthcare_surcharge("Yes", previous_question_id=48) \
    .clarify_question_50_terms() \
    .do_you_have_1270_in_bank_account("Yes", previous_question_id=49) \
    .run()

@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_eligible_immigration_salary_list():
    await SkilledWorkerVisaScenario(
        short_description="Eligible: Job on immigration salary list at standard going rate.",
        user_intro="I am from Egypt, I have a job offer on the immigration salary list paying £42,000 per year.",
        user_should_be_eligible=True,
    ) \
    .clarify_question_1_terms() \
    .are_you_applying_for_the_first_time_extending_or_switching("Applying for the first time from outside the UK", previous_question_id=None) \
    .clarify_question_2_terms() \
    .do_you_have_a_confirmed_job_offer("Yes", previous_question_id=1) \
    .clarify_question_3_terms() \
    .has_your_employer_been_approved_by_home_office("Yes", previous_question_id=2) \
    .clarify_question_4_terms() \
    .do_you_have_certificate_of_sponsorship("Yes", previous_question_id=3) \
    .clarify_question_5_terms() \
    .do_you_know_4_digit_occupation_code("Yes", previous_question_id=4) \
    .clarify_question_6_terms() \
    .is_occupation_code_listed_in_eligible_jobs("Yes", previous_question_id=5) \
    .clarify_question_7_terms() \
    .is_occupation_code_higher_or_medium_skilled("Higher skilled", previous_question_id=6) \
    .for_higher_skilled_jobs_continue("Continue", previous_question_id=7) \
    .clarify_question_10_terms() \
    .are_you_applying_for_care_worker_role("No", previous_question_id=8) \
    .clarify_question_12_terms() \
    .when_did_you_receive_cos("On or after 4 April 2024", previous_question_id=10) \
    .clarify_question_13_terms() \
    .what_is_your_annual_salary("£42,000", previous_question_id=12) \
    .clarify_question_14_terms() \
    .is_job_in_healthcare_or_education("No", previous_question_id=13) \
    .clarify_question_20_terms() \
    .what_is_standard_going_rate_for_occupation("£42,000", previous_question_id=14) \
    .is_salary_at_least_41700_and_going_rate("No", previous_question_id=20) \
    .is_salary_at_least_33400("Yes", previous_question_id=21) \
    .clarify_question_9_terms() \
    .is_job_on_immigration_salary_list("Yes", previous_question_id=22) \
    .is_salary_at_least_standard_going_rate_for_isl_job("Yes", previous_question_id=23) \
    .clarify_question_42_terms() \
    .are_you_from_english_speaking_country("No", previous_question_id=24) \
    .are_you_healthcare_professional_with_english_assessment("No", previous_question_id=42) \
    .have_you_proved_english_in_previous_visa("No", previous_question_id=43) \
    .can_you_prove_english_knowledge("Yes", previous_question_id=44) \
    .which_method_to_prove_english("Approved SELT at level B2 or higher", previous_question_id=45) \
    .can_you_pass_selt_at_b2("Yes", previous_question_id=46) \
    .clarify_question_48_terms() \
    .can_you_pay_application_fee("Yes", previous_question_id=47) \
    .clarify_question_49_terms() \
    .can_you_pay_healthcare_surcharge("Yes", previous_question_id=48) \
    .clarify_question_50_terms() \
    .do_you_have_1270_in_bank_account("Yes", previous_question_id=49) \
    .run()

@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_eligible_healthcare_national_pay_scale():
    await SkilledWorkerVisaScenario(
        short_description="Eligible: Healthcare job with national pay scale at £28,000.",
        user_intro="I am from Kenya, I have a nurse job offer in the NHS paying £28,000 per year.",
        user_should_be_eligible=True,
    ) \
    .clarify_question_1_terms() \
    .are_you_applying_for_the_first_time_extending_or_switching("Applying for the first time from outside the UK", previous_question_id=None) \
    .clarify_question_2_terms() \
    .do_you_have_a_confirmed_job_offer("Yes", previous_question_id=1) \
    .clarify_question_3_terms() \
    .has_your_employer_been_approved_by_home_office("Yes", previous_question_id=2) \
    .clarify_question_4_terms() \
    .do_you_have_certificate_of_sponsorship("Yes", previous_question_id=3) \
    .clarify_question_5_terms() \
    .do_you_know_4_digit_occupation_code("Yes", previous_question_id=4) \
    .clarify_question_6_terms() \
    .is_occupation_code_listed_in_eligible_jobs("Yes", previous_question_id=5) \
    .clarify_question_7_terms() \
    .is_occupation_code_higher_or_medium_skilled("Higher skilled", previous_question_id=6) \
    .for_higher_skilled_jobs_continue("Continue", previous_question_id=7) \
    .clarify_question_10_terms() \
    .are_you_applying_for_care_worker_role("No", previous_question_id=8) \
    .clarify_question_12_terms() \
    .when_did_you_receive_cos("On or after 4 April 2024", previous_question_id=10) \
    .clarify_question_13_terms() \
    .what_is_your_annual_salary("£28,000", previous_question_id=12) \
    .clarify_question_14_terms() \
    .is_job_in_healthcare_or_education("Yes", previous_question_id=13) \
    .clarify_question_15_terms() \
    .does_job_appear_on_healthcare_education_list("Yes", previous_question_id=14) \
    .clarify_question_16_terms() \
    .what_is_national_pay_scale_going_rate("£28,000", previous_question_id=15) \
    .is_salary_at_least_25000("Yes", previous_question_id=16) \
    .is_salary_at_least_national_pay_scale_going_rate_q19("Yes", previous_question_id=17) \
    .clarify_question_42_terms() \
    .are_you_from_english_speaking_country("No", previous_question_id=19) \
    .clarify_question_43_terms() \
    .are_you_healthcare_professional_with_english_assessment("Yes", previous_question_id=42) \
    .clarify_question_48_terms() \
    .can_you_pay_application_fee("Yes", previous_question_id=43) \
    .clarify_question_49_terms() \
    .can_you_pay_healthcare_surcharge("Yes", previous_question_id=48) \
    .clarify_question_50_terms() \
    .do_you_have_1270_in_bank_account("Yes", previous_question_id=49) \
    .run()

@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_eligible_extension_same_job():
    await SkilledWorkerVisaScenario(
        short_description="Eligible: Extension with same job, employer, and occupation code.",
        user_intro="I am currently on a Skilled Worker visa in the UK and want to extend.",
        user_should_be_eligible=True,
    ) \
    .clarify_question_1_terms() \
    .are_you_applying_for_the_first_time_extending_or_switching("Extending an existing Skilled Worker visa", previous_question_id=None) \
    .clarify_question_52_terms() \
    .do_you_have_same_job_as_previous_permission("Yes", previous_question_id=1) \
    .is_job_same_occupation_code("Yes", previous_question_id=52) \
    .still_with_same_employer("Yes", previous_question_id=53) \
    .clarify_question_55_terms() \
    .did_you_get_first_cos_before_july_2025("Not applicable (higher skilled job)", previous_question_id=54) \
    .when_did_you_receive_first_cos("On or after 4 April 2024", previous_question_id=55) \
    .is_salary_at_least_41700_and_going_rate("Yes", previous_question_id=57) \
    .clarify_question_61_terms() \
    .have_you_already_proved_english_for_extension("Yes", previous_question_id=21) \
    .can_you_pay_extension_fee("Yes", previous_question_id=61) \
    .can_you_pay_healthcare_surcharge_extension("Yes", previous_question_id=59) \
    .clarify_question_62_terms() \
    .understand_travel_restrictions_extension("Yes, I understand", previous_question_id=60) \
    .run()

@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_eligible_switching_from_student_visa():
    await SkilledWorkerVisaScenario(
        short_description="Eligible: Switching from Student visa to Skilled Worker visa.",
        user_intro="I am currently on a Student visa in the UK and want to switch to a Skilled Worker visa.",
        user_should_be_eligible=True,
    ) \
    .clarify_question_1_terms() \
    .are_you_applying_for_the_first_time_extending_or_switching("Switching from another visa type while in the UK", previous_question_id=None) \
    .clarify_question_63_terms() \
    .are_you_on_visa_that_cannot_switch("No, I'm on a different visa type", previous_question_id=1) \
    .does_job_meet_eligibility_requirements("Yes", previous_question_id=63) \
    .clarify_question_65_terms() \
    .switching_to_care_worker_or_medium_skilled("No", previous_question_id=64) \
    .clarify_question_67_terms() \
    .can_you_prove_english_at_b2_for_switching("Yes", previous_question_id=65) \
    .can_you_pay_switching_fee("Yes", previous_question_id=67) \
    .can_you_pay_healthcare_surcharge_switching("Yes", previous_question_id=68) \
    .clarify_question_70_terms() \
    .been_in_uk_at_least_12_months("Yes (exempt from maintenance requirement)", previous_question_id=69) \
    .clarify_question_62_terms() \
    .understand_travel_restrictions_switching("Yes, I understand", previous_question_id=70) \
    .run()

@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_ineligible_extension_changed_employer():
    await SkilledWorkerVisaScenario(
        short_description="Ineligible for extension: Changed employer (must update visa instead).",
        user_intro="I am on a Skilled Worker visa but I changed employers.",
        user_should_be_eligible=False,
    ) \
    .clarify_question_1_terms() \
    .are_you_applying_for_the_first_time_extending_or_switching("Extending an existing Skilled Worker visa", previous_question_id=None) \
    .clarify_question_52_terms() \
    .do_you_have_same_job_as_previous_permission("Yes", previous_question_id=1) \
    .is_job_same_occupation_code("Yes", previous_question_id=52) \
    .still_with_same_employer("No", previous_question_id=53) \
    .run()

@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_ineligible_switching_from_visit_visa():
    await SkilledWorkerVisaScenario(
        short_description="Ineligible: Cannot switch from visit visa (must apply from abroad).",
        user_intro="I am on a visit visa and want to switch to a Skilled Worker visa.",
        user_should_be_eligible=False,
    ) \
    .clarify_question_1_terms() \
    .are_you_applying_for_the_first_time_extending_or_switching("Switching from another visa type while in the UK", previous_question_id=None) \
    .clarify_question_63_terms() \
    .are_you_on_visa_that_cannot_switch("Yes, I'm on one of those visas", previous_question_id=1) \
    .run()

@pytest.mark.agent_test
@pytest.mark.asyncio
async def test_eligible_medium_skilled_on_immigration_salary_list():
    await SkilledWorkerVisaScenario(
        short_description="Eligible: Medium skilled job on immigration salary list with sufficient salary.",
        user_intro="I am from Turkey, I have a medium skilled job offer on the immigration salary list paying £40,000 per year.",
        user_should_be_eligible=True,
    ) \
    .clarify_question_1_terms() \
    .are_you_applying_for_the_first_time_extending_or_switching("Applying for the first time from outside the UK", previous_question_id=None) \
    .clarify_question_2_terms() \
    .do_you_have_a_confirmed_job_offer("Yes", previous_question_id=1) \
    .clarify_question_3_terms() \
    .has_your_employer_been_approved_by_home_office("Yes", previous_question_id=2) \
    .clarify_question_4_terms() \
    .do_you_have_certificate_of_sponsorship("Yes", previous_question_id=3) \
    .clarify_question_5_terms() \
    .do_you_know_4_digit_occupation_code("Yes", previous_question_id=4) \
    .clarify_question_6_terms() \
    .is_occupation_code_listed_in_eligible_jobs("Yes", previous_question_id=5) \
    .clarify_question_7_terms() \
    .is_occupation_code_higher_or_medium_skilled("Medium skilled", previous_question_id=6) \
    .clarify_question_9_terms() \
    .is_job_on_immigration_salary_or_shortage_list("Yes", previous_question_id=7) \
    .clarify_question_10_terms() \
    .are_you_applying_for_care_worker_role("No", previous_question_id=9) \
    .clarify_question_12_terms() \
    .when_did_you_receive_cos("On or after 4 April 2024", previous_question_id=10) \
    .clarify_question_13_terms() \
    .what_is_your_annual_salary("£40,000", previous_question_id=12) \
    .clarify_question_14_terms() \
    .is_job_in_healthcare_or_education("No", previous_question_id=13) \
    .clarify_question_20_terms() \
    .what_is_standard_going_rate_for_occupation("£40,000", previous_question_id=14) \
    .is_salary_at_least_41700_and_going_rate("No", previous_question_id=20) \
    .is_salary_at_least_33400("Yes", previous_question_id=21) \
    .is_job_on_immigration_salary_list("Yes", previous_question_id=22) \
    .is_salary_at_least_standard_going_rate_for_isl_job("Yes", previous_question_id=23) \
    .clarify_question_42_terms() \
    .are_you_from_english_speaking_country("No", previous_question_id=24) \
    .are_you_healthcare_professional_with_english_assessment("No", previous_question_id=42) \
    .have_you_proved_english_in_previous_visa("No", previous_question_id=43) \
    .can_you_prove_english_knowledge("Yes", previous_question_id=44) \
    .which_method_to_prove_english("Approved SELT at level B2 or higher", previous_question_id=45) \
    .can_you_pass_selt_at_b2("Yes", previous_question_id=46) \
    .clarify_question_48_terms() \
    .can_you_pay_application_fee("Yes", previous_question_id=47) \
    .clarify_question_49_terms() \
    .can_you_pay_healthcare_surcharge("Yes", previous_question_id=48) \
    .clarify_question_50_terms() \
    .do_you_have_1270_in_bank_account("Yes", previous_question_id=49) \
    .run()
