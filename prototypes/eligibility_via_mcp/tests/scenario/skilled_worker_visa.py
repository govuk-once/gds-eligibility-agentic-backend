from tests.scenario.base import BaseScenario

class SkilledWorkerVisaScenario(BaseScenario):

    def _get_eligibility_name(self) -> str:
        return "Skilled Worker Visa"

    def clarify_question_1_terms(self) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append("What is meant by 'Skilled Worker visa'?")
        self.judge_criteria.append("The agent should offer the following definition for 'Skilled Worker visa': A visa that allows you to come to or stay in the UK to do an eligible job with an approved employer. It replaced the Tier 2 (General) work visa.")
        return self

    def are_you_applying_for_the_first_time_extending_or_switching(self, answer: str, previous_question_id: int | None = None) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append(answer)
        
        expected_question = "Are you applying for a Skilled Worker visa for the first time, extending an existing Skilled Worker visa, or switching from another visa type?"
        if previous_question_id:
            self.judge_criteria.append(f"After Question {previous_question_id} was answered, the agent must ask '{expected_question}'. The user answered '{answer}'.")
        else:
            self.judge_criteria.append(f"The agent must start the assessment by asking '{expected_question}'. The user answered '{answer}'.")
            
        return self

    def clarify_question_2_terms(self) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append("What is meant by 'confirmed job offer'?")
        self.judge_criteria.append("The agent should offer the following definition for 'confirmed job offer': A formal offer of employment from a UK employer that meets the Skilled Worker visa requirements, confirmed by a certificate of sponsorship.")
        return self

    def do_you_have_a_confirmed_job_offer(self, answer: str, previous_question_id: int | None = None) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append(answer)
        
        expected_question = "Do you have a confirmed job offer from a UK employer before applying for your visa?"
        if previous_question_id:
            self.judge_criteria.append(f"After Question {previous_question_id} was answered, the agent must ask '{expected_question}'. The user answered '{answer}'.")
        else:
            self.judge_criteria.append(f"The agent must start the assessment by asking '{expected_question}'. The user answered '{answer}'.")
            
        return self

    def clarify_question_3_terms(self) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append("What is meant by 'licensed sponsor'?")
        self.judge_criteria.append("The agent should offer the following definition for 'licensed sponsor': An employer registered with the UK Home Office who has been granted permission to sponsor skilled workers. You can view the list of approved UK employers on the GOV.UK website.")
        return self

    def has_your_employer_been_approved_by_home_office(self, answer: str, previous_question_id: int | None = None) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append(answer)
        
        expected_question = "Has your employer been approved by the Home Office as a licensed sponsor?"
        if previous_question_id:
            self.judge_criteria.append(f"After Question {previous_question_id} was answered, the agent must ask '{expected_question}'. The user answered '{answer}'.")
        else:
            self.judge_criteria.append(f"The agent must start the assessment by asking '{expected_question}'. The user answered '{answer}'.")
            
        return self

    def clarify_question_4_terms(self) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append("What is meant by 'certificate of sponsorship'?")
        self.judge_criteria.append("The agent should offer the following definition for 'certificate of sponsorship': An electronic record (not a physical document) issued by your employer with a unique reference number. It contains information about your job role and personal details. You must apply for your visa within 3 months of receiving it.")
        return self

    def do_you_have_certificate_of_sponsorship(self, answer: str, previous_question_id: int | None = None) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append(answer)
        
        expected_question = "Do you have a certificate of sponsorship (CoS) from your employer with information about the role you've been offered in the UK?"
        if previous_question_id:
            self.judge_criteria.append(f"After Question {previous_question_id} was answered, the agent must ask '{expected_question}'. The user answered '{answer}'.")
        else:
            self.judge_criteria.append(f"The agent must start the assessment by asking '{expected_question}'. The user answered '{answer}'.")
            
        return self

    def clarify_question_5_terms(self) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append("What is meant by 'occupation code'?")
        self.judge_criteria.append("The agent should offer the following definition for 'occupation code': A 4-digit code from the UK Standard Occupational Classification (SOC) system that identifies your specific job type. Different occupation codes have different eligibility requirements and going rates.")
        return self

    def do_you_know_4_digit_occupation_code(self, answer: str, previous_question_id: int | None = None) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append(answer)
        
        expected_question = "Do you know the 4-digit occupation code for your job?"
        if previous_question_id:
            self.judge_criteria.append(f"After Question {previous_question_id} was answered, the agent must ask '{expected_question}'. The user answered '{answer}'.")
        else:
            self.judge_criteria.append(f"The agent must start the assessment by asking '{expected_question}'. The user answered '{answer}'.")
            
        return self

    def clarify_question_6_terms(self) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append("What is meant by 'eligible occupations'?")
        self.judge_criteria.append("The agent should offer the following definition for 'eligible occupations': Jobs that are at RQF level 3 or above (equivalent to A level) with specific occupation codes listed in the UK's immigration rules. The table is sorted by occupation code on GOV.UK.")
        return self

    def is_occupation_code_listed_in_eligible_jobs(self, answer: str, previous_question_id: int | None = None) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append(answer)
        
        expected_question = "Is your occupation code listed in the table of eligible jobs for the Skilled Worker visa?"
        if previous_question_id:
            self.judge_criteria.append(f"After Question {previous_question_id} was answered, the agent must ask '{expected_question}'. The user answered '{answer}'.")
        else:
            self.judge_criteria.append(f"The agent must start the assessment by asking '{expected_question}'. The user answered '{answer}'.")
            
        return self

    def clarify_question_7_terms(self) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append("What is meant by 'higher skilled vs medium skilled'?")
        self.judge_criteria.append("The agent should offer the following definition for 'higher skilled vs medium skilled': Higher skilled jobs can apply directly for a Skilled Worker visa. Medium skilled jobs can only apply if the job is also on the immigration salary list or temporary shortage list.")
        return self

    def is_occupation_code_higher_or_medium_skilled(self, answer: str, previous_question_id: int | None = None) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append(answer)
        
        expected_question = "Is your occupation code listed as 'higher skilled' or 'medium skilled'?"
        if previous_question_id:
            self.judge_criteria.append(f"After Question {previous_question_id} was answered, the agent must ask '{expected_question}'. The user answered '{answer}'.")
        else:
            self.judge_criteria.append(f"The agent must start the assessment by asking '{expected_question}'. The user answered '{answer}'.")
            
        return self

    def for_higher_skilled_jobs_continue(self, answer: str, previous_question_id: int | None = None) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append(answer)
        
        expected_question = "For higher skilled jobs: You are eligible to proceed with your application. Continue to salary checks."
        if previous_question_id:
            self.judge_criteria.append(f"After Question {previous_question_id} was answered, the agent must ask '{expected_question}'. The user answered '{answer}'.")
        else:
            self.judge_criteria.append(f"The agent must start the assessment by asking '{expected_question}'. The user answered '{answer}'.")
            
        return self

    def clarify_question_9_terms(self) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append("What is meant by 'immigration salary list'?")
        self.judge_criteria.append("The agent should offer the following definition for 'immigration salary list': A list of skilled jobs which have lower salary requirements (minimum £33,400) and lower visa application fees. Check if your job is on this list on GOV.UK.")
        return self

    def clarify_question_9_terms_temporary_shortage(self) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append("What is meant by 'temporary shortage list'?")
        self.judge_criteria.append("The agent should offer the following definition for 'temporary shortage list': A list of occupations where there is a shortage of workers in the UK, making them eligible for the Skilled Worker visa even if medium skilled.")
        return self

    def is_job_on_immigration_salary_or_shortage_list(self, answer: str, previous_question_id: int | None = None) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append(answer)
        
        expected_question = "For medium skilled jobs: Is your job on either the immigration salary list OR the temporary shortage list?"
        if previous_question_id:
            self.judge_criteria.append(f"After Question {previous_question_id} was answered, the agent must ask '{expected_question}'. The user answered '{answer}'.")
        else:
            self.judge_criteria.append(f"The agent must start the assessment by asking '{expected_question}'. The user answered '{answer}'.")
            
        return self

    def clarify_question_10_terms(self) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append("What is meant by 'care worker codes'?")
        self.judge_criteria.append("The agent should offer the following definition for 'care worker codes': Care workers have occupation code 6135, senior care workers have code 6136. These roles have specific registration requirements in England.")
        return self

    def are_you_applying_for_care_worker_role(self, answer: str, previous_question_id: int | None = None) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append(answer)
        
        expected_question = "Are you applying for a role as a care worker (code 6135) or senior care worker (code 6136) in England?"
        if previous_question_id:
            self.judge_criteria.append(f"After Question {previous_question_id} was answered, the agent must ask '{expected_question}'. The user answered '{answer}'.")
        else:
            self.judge_criteria.append(f"The agent must start the assessment by asking '{expected_question}'. The user answered '{answer}'.")
            
        return self

    def clarify_question_11_terms(self) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append("What is meant by 'Care Quality Commission'?")
        self.judge_criteria.append("The agent should offer the following definition for 'Care Quality Commission': The independent regulator of health and adult social care services in England. Care worker employers must be registered with the CQC.")
        return self

    def is_employer_registered_with_cqc(self, answer: str, previous_question_id: int | None = None) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append(answer)
        
        expected_question = "Is your employer registered with the Care Quality Commission?"
        if previous_question_id:
            self.judge_criteria.append(f"After Question {previous_question_id} was answered, the agent must ask '{expected_question}'. The user answered '{answer}'.")
        else:
            self.judge_criteria.append(f"The agent must start the assessment by asking '{expected_question}'. The user answered '{answer}'.")
            
        return self

    def clarify_question_12_terms(self) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append("What is meant by 'CoS date significance'?")
        self.judge_criteria.append("The agent should offer the following definition for 'CoS date significance': The date you received your certificate of sponsorship determines which salary rules apply. Different thresholds apply for CoS received before vs. on or after 4 April 2024.")
        return self

    def when_did_you_receive_cos(self, answer: str, previous_question_id: int | None = None) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append(answer)
        
        expected_question = "When did you (or will you) receive your certificate of sponsorship?"
        if previous_question_id:
            self.judge_criteria.append(f"After Question {previous_question_id} was answered, the agent must ask '{expected_question}'. The user answered '{answer}'.")
        else:
            self.judge_criteria.append(f"The agent must start the assessment by asking '{expected_question}'. The user answered '{answer}'.")
            
        return self

    def clarify_question_13_terms(self) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append("What is meant by 'annual salary'?")
        self.judge_criteria.append("The agent should offer the following definition for 'annual salary': The gross annual salary (before tax) that your employer will pay you for the sponsored role, as stated on your certificate of sponsorship. This must meet minimum thresholds.")
        return self

    def what_is_your_annual_salary(self, answer: str, previous_question_id: int | None = None) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append(answer)
        
        expected_question = "What is your annual salary for the job offer (in GBP)?"
        if previous_question_id:
            self.judge_criteria.append(f"After Question {previous_question_id} was answered, the agent must ask '{expected_question}'. The user answered '{answer}'.")
        else:
            self.judge_criteria.append(f"The agent must start the assessment by asking '{expected_question}'. The user answered '{answer}'.")
            
        return self

    def clarify_question_14_terms(self) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append("What is meant by 'healthcare and education jobs'?")
        self.judge_criteria.append("The agent should offer the following definition for 'healthcare and education jobs': Some healthcare and education jobs have going rates based on national pay scales (e.g., NHS pay bands), with a minimum of £25,000 instead of £41,700.")
        return self

    def is_job_in_healthcare_or_education(self, answer: str, previous_question_id: int | None = None) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append(answer)
        
        expected_question = "Is your job in healthcare or education with national pay scale rates?"
        if previous_question_id:
            self.judge_criteria.append(f"After Question {previous_question_id} was answered, the agent must ask '{expected_question}'. The user answered '{answer}'.")
        else:
            self.judge_criteria.append(f"The agent must start the assessment by asking '{expected_question}'. The user answered '{answer}'.")
            
        return self

    def clarify_question_15_terms(self) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append("What is meant by 'eligible healthcare and education jobs list'?")
        self.judge_criteria.append("The agent should offer the following definition for 'eligible healthcare and education jobs list': A specific list of healthcare and education roles with national pay scale rates. Check the GOV.UK page 'If you work in healthcare or education' to see if your job is included.")
        return self

    def does_job_appear_on_healthcare_education_list(self, answer: str, previous_question_id: int | None = None) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append(answer)
        
        expected_question = "Does your healthcare or education job appear on the list of eligible healthcare and education jobs with national pay scales?"
        if previous_question_id:
            self.judge_criteria.append(f"After Question {previous_question_id} was answered, the agent must ask '{expected_question}'. The user answered '{answer}'.")
        else:
            self.judge_criteria.append(f"The agent must start the assessment by asking '{expected_question}'. The user answered '{answer}'.")
            
        return self

    def clarify_question_16_terms(self) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append("What is meant by 'national pay scale going rate'?")
        self.judge_criteria.append("The agent should offer the following definition for 'national pay scale going rate': For eligible healthcare/education jobs, the going rate is based on NHS pay bands or teaching/education leadership pay scales, which vary by role and UK region.")
        return self

    def what_is_national_pay_scale_going_rate(self, answer: str, previous_question_id: int | None = None) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append(answer)
        
        expected_question = "What is the going rate for your job based on the national pay scale (NHS pay band or teaching role)?"
        if previous_question_id:
            self.judge_criteria.append(f"After Question {previous_question_id} was answered, the agent must ask '{expected_question}'. The user answered '{answer}'.")
        else:
            self.judge_criteria.append(f"The agent must start the assessment by asking '{expected_question}'. The user answered '{answer}'.")
            
        return self

    def is_salary_at_least_25000(self, answer: str, previous_question_id: int | None = None) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append(answer)
        
        expected_question = "Is your annual salary at least £25,000?"
        if previous_question_id:
            self.judge_criteria.append(f"After Question {previous_question_id} was answered, the agent must ask '{expected_question}'. The user answered '{answer}'.")
        else:
            self.judge_criteria.append(f"The agent must start the assessment by asking '{expected_question}'. The user answered '{answer}'.")
            
        return self

    def is_salary_at_least_national_pay_scale_going_rate_q18(self, answer: str, previous_question_id: int | None = None) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append(answer)
        
        expected_question = "Is your annual salary at least the national pay scale going rate for your specific job?"
        if previous_question_id:
            self.judge_criteria.append(f"After Question {previous_question_id} was answered, the agent must ask '{expected_question}'. The user answered '{answer}'.")
        else:
            self.judge_criteria.append(f"The agent must start the assessment by asking '{expected_question}'. The user answered '{answer}'.")
            
        return self

    def is_salary_at_least_national_pay_scale_going_rate_q19(self, answer: str, previous_question_id: int | None = None) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append(answer)
        
        expected_question = "Is your annual salary at least the national pay scale going rate for your specific job?"
        if previous_question_id:
            self.judge_criteria.append(f"After Question {previous_question_id} was answered, the agent must ask '{expected_question}'. The user answered '{answer}'.")
        else:
            self.judge_criteria.append(f"The agent must start the assessment by asking '{expected_question}'. The user answered '{answer}'.")
            
        return self

    def clarify_question_20_terms(self) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append("What is meant by 'going rate'?")
        self.judge_criteria.append("The agent should offer the following definition for 'going rate': The minimum salary level set for your specific occupation code. Each code has its own going rate listed in the going rates table on GOV.UK. You must be paid at least £41,700 OR the going rate, whichever is higher.")
        return self

    def what_is_standard_going_rate_for_occupation(self, answer: str, previous_question_id: int | None = None) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append(answer)
        
        expected_question = "What is the standard going rate for your occupation code (from the going rates table)?"
        if previous_question_id:
            self.judge_criteria.append(f"After Question {previous_question_id} was answered, the agent must ask '{expected_question}'. The user answered '{answer}'.")
        else:
            self.judge_criteria.append(f"The agent must start the assessment by asking '{expected_question}'. The user answered '{answer}'.")
            
        return self

    def is_salary_at_least_41700_and_going_rate(self, answer: str, previous_question_id: int | None = None) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append(answer)
        
        expected_question = "Is your annual salary at least £41,700 AND at least the going rate for your occupation, whichever is higher?"
        if previous_question_id:
            self.judge_criteria.append(f"After Question {previous_question_id} was answered, the agent must ask '{expected_question}'. The user answered '{answer}'.")
        else:
            self.judge_criteria.append(f"The agent must start the assessment by asking '{expected_question}'. The user answered '{answer}'.")
            
        return self

    def is_salary_at_least_33400(self, answer: str, previous_question_id: int | None = None) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append(answer)
        
        expected_question = "Is your annual salary at least £33,400?"
        if previous_question_id:
            self.judge_criteria.append(f"After Question {previous_question_id} was answered, the agent must ask '{expected_question}'. The user answered '{answer}'.")
        else:
            self.judge_criteria.append(f"The agent must start the assessment by asking '{expected_question}'. The user answered '{answer}'.")
            
        return self

    def is_job_on_immigration_salary_list(self, answer: str, previous_question_id: int | None = None) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append(answer)
        
        expected_question = "Is your job on the immigration salary list?"
        if previous_question_id:
            self.judge_criteria.append(f"After Question {previous_question_id} was answered, the agent must ask '{expected_question}'. The user answered '{answer}'.")
        else:
            self.judge_criteria.append(f"The agent must start the assessment by asking '{expected_question}'. The user answered '{answer}'.")
            
        return self

    def is_salary_at_least_standard_going_rate_for_isl_job(self, answer: str, previous_question_id: int | None = None) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append(answer)
        
        expected_question = "For immigration salary list jobs: Is your salary at least the standard going rate for your job (even though the minimum is £33,400)?"
        if previous_question_id:
            self.judge_criteria.append(f"After Question {previous_question_id} was answered, the agent must ask '{expected_question}'. The user answered '{answer}'.")
        else:
            self.judge_criteria.append(f"The agent must start the assessment by asking '{expected_question}'. The user answered '{answer}'.")
            
        return self

    def are_you_under_26(self, answer: str, previous_question_id: int | None = None) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append(answer)
        
        expected_question = "Are you under 26 years old on the date you apply?"
        if previous_question_id:
            self.judge_criteria.append(f"After Question {previous_question_id} was answered, the agent must ask '{expected_question}'. The user answered '{answer}'.")
        else:
            self.judge_criteria.append(f"The agent must start the assessment by asking '{expected_question}'. The user answered '{answer}'.")
            
        return self

    def is_salary_70_percent_going_rate_under_26(self, answer: str, previous_question_id: int | None = None) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append(answer)
        
        expected_question = "For under 26: Is your salary at least 70% of the standard going rate for your job?"
        if previous_question_id:
            self.judge_criteria.append(f"After Question {previous_question_id} was answered, the agent must ask '{expected_question}'. The user answered '{answer}'.")
        else:
            self.judge_criteria.append(f"The agent must start the assessment by asking '{expected_question}'. The user answered '{answer}'.")
            
        return self

    def clarify_question_27_terms(self) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append("What is meant by 'Student visa holder eligibility'?")
        self.judge_criteria.append("The agent should offer the following definition for 'Student visa holder eligibility': You can get a reduced salary threshold (70% of going rate) if you're currently on a Student visa studying at bachelor's level or above, or held one in the last 2 years with Student/visit visa as most recent.")
        return self

    def are_you_current_or_recent_student_visa_holder(self, answer: str, previous_question_id: int | None = None) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append(answer)
        
        expected_question = "Are you currently in the UK on a Student visa studying at bachelor's degree level or above, OR have you been in the last 2 years with a Student or visit visa as your most recent visa?"
        if previous_question_id:
            self.judge_criteria.append(f"After Question {previous_question_id} was answered, the agent must ask '{expected_question}'. The user answered '{answer}'.")
        else:
            self.judge_criteria.append(f"The agent must start the assessment by asking '{expected_question}'. The user answered '{answer}'.")
            
        return self

    def is_salary_70_percent_going_rate_student(self, answer: str, previous_question_id: int | None = None) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append(answer)
        
        expected_question = "For current/recent students: Is your salary at least 70% of the standard going rate for your job?"
        if previous_question_id:
            self.judge_criteria.append(f"After Question {previous_question_id} was answered, the agent must ask '{expected_question}'. The user answered '{answer}'.")
        else:
            self.judge_criteria.append(f"The agent must start the assessment by asking '{expected_question}'. The user answered '{answer}'.")
            
        return self

    def clarify_question_29_terms(self) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append("What is meant by 'Graduate visa holder eligibility'?")
        self.judge_criteria.append("The agent should offer the following definition for 'Graduate visa holder eligibility': You can get a reduced salary threshold (70% of going rate) if you're currently on a Graduate visa, or held one in the last 2 years with Graduate/visit visa as most recent.")
        return self

    def are_you_current_or_recent_graduate_visa_holder(self, answer: str, previous_question_id: int | None = None) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append(answer)
        
        expected_question = "Are you currently in the UK on a Graduate visa, OR have you been in the last 2 years with a Graduate or visit visa as your most recent visa?"
        if previous_question_id:
            self.judge_criteria.append(f"After Question {previous_question_id} was answered, the agent must ask '{expected_question}'. The user answered '{answer}'.")
        else:
            self.judge_criteria.append(f"The agent must start the assessment by asking '{expected_question}'. The user answered '{answer}'.")
            
        return self

    def is_salary_70_percent_going_rate_graduate(self, answer: str, previous_question_id: int | None = None) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append(answer)
        
        expected_question = "For current/recent graduate visa holders: Is your salary at least 70% of the standard going rate for your job?"
        if previous_question_id:
            self.judge_criteria.append(f"After Question {previous_question_id} was answered, the agent must ask '{expected_question}'. The user answered '{answer}'.")
        else:
            self.judge_criteria.append(f"The agent must start the assessment by asking '{expected_question}'. The user answered '{answer}'.")
            
        return self

    def clarify_question_31_terms(self) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append("What is meant by 'UK regulated profession'?")
        self.judge_criteria.append("The agent should offer the following definition for 'UK regulated profession': A profession that requires specific qualifications or registration to practice legally in the UK, such as doctors, lawyers, architects, or engineers.")
        return self

    def working_towards_uk_regulated_profession(self, answer: str, previous_question_id: int | None = None) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append(answer)
        
        expected_question = "Will you be working towards a recognised qualification in a UK regulated profession?"
        if previous_question_id:
            self.judge_criteria.append(f"After Question {previous_question_id} was answered, the agent must ask '{expected_question}'. The user answered '{answer}'.")
        else:
            self.judge_criteria.append(f"The agent must start the assessment by asking '{expected_question}'. The user answered '{answer}'.")
            
        return self

    def is_salary_70_percent_going_rate_regulated_profession(self, answer: str, previous_question_id: int | None = None) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append(answer)
        
        expected_question = "For regulated profession training: Is your salary at least 70% of the standard going rate for your job?"
        if previous_question_id:
            self.judge_criteria.append(f"After Question {previous_question_id} was answered, the agent must ask '{expected_question}'. The user answered '{answer}'.")
        else:
            self.judge_criteria.append(f"The agent must start the assessment by asking '{expected_question}'. The user answered '{answer}'.")
            
        return self

    def clarify_question_33_terms(self) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append("What is meant by 'chartered status'?")
        self.judge_criteria.append("The agent should offer the following definition for 'chartered status': Professional recognition awarded by a chartered body (like the Royal Institution of Chartered Surveyors) showing you meet the highest standards in your profession.")
        return self

    def working_towards_chartered_status(self, answer: str, previous_question_id: int | None = None) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append(answer)
        
        expected_question = "Will you be working towards full registration or chartered status in the job you're being sponsored for?"
        if previous_question_id:
            self.judge_criteria.append(f"After Question {previous_question_id} was answered, the agent must ask '{expected_question}'. The user answered '{answer}'.")
        else:
            self.judge_criteria.append(f"The agent must start the assessment by asking '{expected_question}'. The user answered '{answer}'.")
            
        return self

    def is_salary_70_percent_going_rate_chartered_status(self, answer: str, previous_question_id: int | None = None) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append(answer)
        
        expected_question = "For registration/chartered status training: Is your salary at least 70% of the standard going rate for your job?"
        if previous_question_id:
            self.judge_criteria.append(f"After Question {previous_question_id} was answered, the agent must ask '{expected_question}'. The user answered '{answer}'.")
        else:
            self.judge_criteria.append(f"The agent must start the assessment by asking '{expected_question}'. The user answered '{answer}'.")
            
        return self

    def clarify_question_35_terms(self) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append("What is meant by 'PhD level qualification'?")
        self.judge_criteria.append("The agent should offer the following definition for 'PhD level qualification': A UK PhD or equivalent doctorate-level overseas qualification (you'll need to apply through Ecctis to check overseas equivalency) that is relevant to the job you'll be doing in the UK.")
        return self

    def do_you_have_phd_relevant_to_job(self, answer: str, previous_question_id: int | None = None) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append(answer)
        
        expected_question = "Do you have a PhD level qualification that's relevant to your job?"
        if previous_question_id:
            self.judge_criteria.append(f"After Question {previous_question_id} was answered, the agent must ask '{expected_question}'. The user answered '{answer}'.")
        else:
            self.judge_criteria.append(f"The agent must start the assessment by asking '{expected_question}'. The user answered '{answer}'.")
            
        return self

    def clarify_question_36_terms(self) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append("What is meant by 'STEM PhD'?")
        self.judge_criteria.append("The agent should offer the following definition for 'STEM PhD': A PhD in Science, Technology, Engineering, or Mathematics. STEM PhD holders can be paid 80% of the going rate (minimum £33,400), while non-STEM PhD holders need 90% (minimum £37,500).")
        return self

    def is_phd_in_stem_subject(self, answer: str, previous_question_id: int | None = None) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append(answer)
        
        expected_question = "Is your PhD in a STEM subject (science, technology, engineering, or maths)?"
        if previous_question_id:
            self.judge_criteria.append(f"After Question {previous_question_id} was answered, the agent must ask '{expected_question}'. The user answered '{answer}'.")
        else:
            self.judge_criteria.append(f"The agent must start the assessment by asking '{expected_question}'. The user answered '{answer}'.")
            
        return self

    def is_salary_80_percent_going_rate_stem_phd(self, answer: str, previous_question_id: int | None = None) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append(answer)
        
        expected_question = "For STEM PhD holders: Is your salary at least 80% of the standard going rate for your job, and at least £33,400?"
        if previous_question_id:
            self.judge_criteria.append(f"After Question {previous_question_id} was answered, the agent must ask '{expected_question}'. The user answered '{answer}'.")
        else:
            self.judge_criteria.append(f"The agent must start the assessment by asking '{expected_question}'. The user answered '{answer}'.")
            
        return self

    def is_salary_90_percent_going_rate_non_stem_phd(self, answer: str, previous_question_id: int | None = None) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append(answer)
        
        expected_question = "For non-STEM PhD holders: Is your salary at least 90% of the standard going rate for your job, and at least £37,500?"
        if previous_question_id:
            self.judge_criteria.append(f"After Question {previous_question_id} was answered, the agent must ask '{expected_question}'. The user answered '{answer}'.")
        else:
            self.judge_criteria.append(f"The agent must start the assessment by asking '{expected_question}'. The user answered '{answer}'.")
            
        return self

    def clarify_question_39_terms(self) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append("What is meant by 'postdoctoral position codes'?")
        self.judge_criteria.append("The agent should offer the following definition for 'postdoctoral position codes': Specific occupation codes for postdoctoral science/higher education roles: 2111 (chemical scientists), 2112 (biological scientists), 2113 (biochemists/biomedical scientists), 2114 (physical scientists), 2115 (social/humanities scientists), 2119 (natural/social science professionals), 2162 (other researchers), 2311 (higher education teaching professionals).")
        return self

    def working_in_postdoctoral_position(self, answer: str, previous_question_id: int | None = None) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append(answer)
        
        expected_question = "Will you be working in a postdoctoral position in science or higher education (occupation codes 2111, 2112, 2113, 2114, 2115, 2119, 2162, or 2311)?"
        if previous_question_id:
            self.judge_criteria.append(f"After Question {previous_question_id} was answered, the agent must ask '{expected_question}'. The user answered '{answer}'.")
        else:
            self.judge_criteria.append(f"The agent must start the assessment by asking '{expected_question}'. The user answered '{answer}'.")
            
        return self

    def is_salary_70_percent_going_rate_postdoc(self, answer: str, previous_question_id: int | None = None) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append(answer)
        
        expected_question = "For postdoctoral positions: Is your salary at least 70% of the standard going rate for your job?"
        if previous_question_id:
            self.judge_criteria.append(f"After Question {previous_question_id} was answered, the agent must ask '{expected_question}'. The user answered '{answer}'.")
        else:
            self.judge_criteria.append(f"The agent must start the assessment by asking '{expected_question}'. The user answered '{answer}'.")
            
        return self

    def clarify_question_41_terms(self) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append("What is meant by '4-year limit for 70% salary routes'?")
        self.judge_criteria.append("The agent should offer the following definition for '4-year limit for 70% salary routes': If you qualify for a visa using the 70% salary threshold (under 26, student/graduate, professional training, or postdoctoral position), your total UK stay cannot exceed 4 years, including any time on a Graduate visa.")
        return self

    def understand_4_year_limit(self, answer: str, previous_question_id: int | None = None) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append(answer)
        
        expected_question = "Note: If you qualified under certain 70% salary routes, your total stay in the UK cannot be more than 4 years (including any time on a Graduate visa). Do you understand this limitation?"
        if previous_question_id:
            self.judge_criteria.append(f"After Question {previous_question_id} was answered, the agent must ask '{expected_question}'. The user answered '{answer}'.")
        else:
            self.judge_criteria.append(f"The agent must start the assessment by asking '{expected_question}'. The user answered '{answer}'.")
            
        return self

    def clarify_question_42_terms(self) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append("What is meant by 'English-speaking countries'?")
        self.judge_criteria.append("The agent should offer the following definition for 'English-speaking countries': Nationals of these countries are exempt from proving English: Antigua and Barbuda, Australia, Bahamas, Barbados, Belize, British overseas territories, Canada, Dominica, Grenada, Guyana, Jamaica, Malta, New Zealand, St Kitts and Nevis, St Lucia, St Vincent and the Grenadines, Trinidad and Tobago, USA.")
        return self

    def are_you_from_english_speaking_country(self, answer: str, previous_question_id: int | None = None) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append(answer)
        
        expected_question = "Are you a national of one of the following majority English-speaking countries: Antigua and Barbuda, Australia, the Bahamas, Barbados, Belize, British overseas territories, Canada, Dominica, Grenada, Guyana, Jamaica, Malta, New Zealand, St Kitts and Nevis, St Lucia, St Vincent and the Grenadines, Trinidad and Tobago, or USA?"
        if previous_question_id:
            self.judge_criteria.append(f"After Question {previous_question_id} was answered, the agent must ask '{expected_question}'. The user answered '{answer}'.")
        else:
            self.judge_criteria.append(f"The agent must start the assessment by asking '{expected_question}'. The user answered '{answer}'.")
            
        return self

    def clarify_question_43_terms(self) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append("What is meant by 'regulated professional body English assessment'?")
        self.judge_criteria.append("The agent should offer the following definition for 'regulated professional body English assessment': Doctors, dentists, nurses, midwives, and vets who have passed English assessments accepted by their professional bodies (GMC, GDC, NMC, RCVS) are exempt from additional English proof.")
        return self

    def are_you_healthcare_professional_with_english_assessment(self, answer: str, previous_question_id: int | None = None) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append(answer)
        
        expected_question = "Are you a doctor, dentist, nurse, midwife, or vet who has already passed an English language assessment accepted by the relevant regulated professional body?"
        if previous_question_id:
            self.judge_criteria.append(f"After Question {previous_question_id} was answered, the agent must ask '{expected_question}'. The user answered '{answer}'.")
        else:
            self.judge_criteria.append(f"The agent must start the assessment by asking '{expected_question}'. The user answered '{answer}'.")
            
        return self

    def have_you_proved_english_in_previous_visa(self, answer: str, previous_question_id: int | None = None) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append(answer)
        
        expected_question = "Have you already proved your knowledge of English in a previous successful visa application?"
        if previous_question_id:
            self.judge_criteria.append(f"After Question {previous_question_id} was answered, the agent must ask '{expected_question}'. The user answered '{answer}'.")
        else:
            self.judge_criteria.append(f"The agent must start the assessment by asking '{expected_question}'. The user answered '{answer}'.")
            
        return self

    def can_you_prove_english_knowledge(self, answer: str, previous_question_id: int | None = None) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append(answer)
        
        expected_question = "Can you prove your knowledge of English in one of the following ways: UK school qualification (GCSE, A Level, Scottish qualifications), degree from UK institution taught in English, degree from non-UK institution taught in English with Ecctis assessment, or passing an approved SELT at level B2?"
        if previous_question_id:
            self.judge_criteria.append(f"After Question {previous_question_id} was answered, the agent must ask '{expected_question}'. The user answered '{answer}'.")
        else:
            self.judge_criteria.append(f"The agent must start the assessment by asking '{expected_question}'. The user answered '{answer}'.")
            
        return self

    def clarify_question_46_terms_uk_school(self) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append("What is meant by 'UK school qualification for English'?")
        self.judge_criteria.append("The agent should offer the following definition for 'UK school qualification for English': GCSE, A Level, Scottish National Qualification level 4 or 5, or Scottish Higher/Advanced Higher in English - must have begun the qualification when under 18.")
        return self

    def clarify_question_46_terms_ecctis(self) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append("What is meant by 'Ecctis'?")
        self.judge_criteria.append("The agent should offer the following definition for 'Ecctis': The UK agency that assesses overseas qualifications. If your degree was taught in English but awarded outside the UK, Ecctis can confirm it's equivalent to a UK bachelor's degree or higher.")
        return self

    def which_method_to_prove_english(self, answer: str, previous_question_id: int | None = None) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append(answer)
        
        expected_question = "Which method will you use to prove your English knowledge?"
        if previous_question_id:
            self.judge_criteria.append(f"After Question {previous_question_id} was answered, the agent must ask '{expected_question}'. The user answered '{answer}'.")
        else:
            self.judge_criteria.append(f"The agent must start the assessment by asking '{expected_question}'. The user answered '{answer}'.")
            
        return self

    def clarify_question_47_terms_selt(self) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append("What is meant by 'SELT'?")
        self.judge_criteria.append("The agent should offer the following definition for 'SELT': Secure English Language Test from an approved provider. For new Skilled Worker visa applications, you need level B2 on the CEFR scale.")
        return self

    def clarify_question_47_terms_cefr(self) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append("What is meant by 'CEFR scale'?")
        self.judge_criteria.append("The agent should offer the following definition for 'CEFR scale': Common European Framework of Reference for Languages - a standardized measure of language ability. B2 is upper intermediate level.")
        return self

    def can_you_pass_selt_at_b2(self, answer: str, previous_question_id: int | None = None) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append(answer)
        
        expected_question = "Can you pass a Secure English Language Test (SELT) at level B2 on the CEFR scale, proving you can read, write, speak and understand English?"
        if previous_question_id:
            self.judge_criteria.append(f"After Question {previous_question_id} was answered, the agent must ask '{expected_question}'. The user answered '{answer}'.")
        else:
            self.judge_criteria.append(f"The agent must start the assessment by asking '{expected_question}'. The user answered '{answer}'.")
            
        return self

    def clarify_question_48_terms(self) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append("What is meant by 'application fee structure'?")
        self.judge_criteria.append("The agent should offer the following definition for 'application fee structure': Fees vary by visa length and whether your job is on the immigration salary list. Outside UK: £769/£1,519 (standard) or £590/£1,160 (ISL). Inside UK: £885/£1,751 (standard) or £590/£1,160 (ISL).")
        return self

    def can_you_pay_application_fee(self, answer: str, previous_question_id: int | None = None) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append(answer)
        
        expected_question = "Can you pay the visa application fee (ranging from £590 to £1,519 depending on your circumstances and visa length)?"
        if previous_question_id:
            self.judge_criteria.append(f"After Question {previous_question_id} was answered, the agent must ask '{expected_question}'. The user answered '{answer}'.")
        else:
            self.judge_criteria.append(f"The agent must start the assessment by asking '{expected_question}'. The user answered '{answer}'.")
            
        return self

    def clarify_question_49_terms(self) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append("What is meant by 'healthcare surcharge'?")
        self.judge_criteria.append("The agent should offer the following definition for 'healthcare surcharge': Also called the Immigration Health Surcharge (IHS), this is usually £1,035 per year. You pay upfront for the full duration of your visa. Some healthcare workers may be exempt.")
        return self

    def can_you_pay_healthcare_surcharge(self, answer: str, previous_question_id: int | None = None) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append(answer)
        
        expected_question = "Can you pay the healthcare surcharge (usually £1,035 per year for the full duration of your visa)?"
        if previous_question_id:
            self.judge_criteria.append(f"After Question {previous_question_id} was answered, the agent must ask '{expected_question}'. The user answered '{answer}'.")
        else:
            self.judge_criteria.append(f"The agent must start the assessment by asking '{expected_question}'. The user answered '{answer}'.")
            
        return self

    def clarify_question_50_terms(self) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append("What is meant by 'maintenance funds'?")
        self.judge_criteria.append("The agent should offer the following definition for 'maintenance funds': Money to support yourself when you arrive in the UK. Must be at least £1,270, available for 28 consecutive days, with day 28 within 31 days of applying.")
        return self

    def do_you_have_1270_in_bank_account(self, answer: str, previous_question_id: int | None = None) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append(answer)
        
        expected_question = "Do you have at least £1,270 in your bank account that has been available for at least 28 consecutive days (with day 28 within 31 days of applying)?"
        if previous_question_id:
            self.judge_criteria.append(f"After Question {previous_question_id} was answered, the agent must ask '{expected_question}'. The user answered '{answer}'.")
        else:
            self.judge_criteria.append(f"The agent must start the assessment by asking '{expected_question}'. The user answered '{answer}'.")
            
        return self

    def clarify_question_51_terms(self) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append("What is meant by 'employer certifies maintenance'?")
        self.judge_criteria.append("The agent should offer the following definition for 'employer certifies maintenance': Your employer can confirm on your certificate of sponsorship that they will cover your costs during your first month in the UK, up to £1,270. Check the 'sponsor certifies maintenance' section under 'Additional data' on your CoS.")
        return self

    def can_employer_certify_maintenance(self, answer: str, previous_question_id: int | None = None) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append(answer)
        
        expected_question = "Can your employer certify maintenance on your certificate of sponsorship, confirming they can cover your costs during your first month in the UK up to £1,270?"
        if previous_question_id:
            self.judge_criteria.append(f"After Question {previous_question_id} was answered, the agent must ask '{expected_question}'. The user answered '{answer}'.")
        else:
            self.judge_criteria.append(f"The agent must start the assessment by asking '{expected_question}'. The user answered '{answer}'.")
            
        return self

    def clarify_question_52_terms(self) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append("What is meant by 'extending vs updating'?")
        self.judge_criteria.append("The agent should offer the following definition for 'extending vs updating': Extending = same job, employer, and occupation code. Updating = changed job, employer, or occupation code. Different application processes apply.")
        return self

    def do_you_have_same_job_as_previous_permission(self, answer: str, previous_question_id: int | None = None) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append(answer)
        
        expected_question = "Do you have the same job as when you were given your previous permission to enter or stay in the UK?"
        if previous_question_id:
            self.judge_criteria.append(f"After Question {previous_question_id} was answered, the agent must ask '{expected_question}'. The user answered '{answer}'.")
        else:
            self.judge_criteria.append(f"The agent must start the assessment by asking '{expected_question}'. The user answered '{answer}'.")
            
        return self

    def is_job_same_occupation_code(self, answer: str, previous_question_id: int | None = None) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append(answer)
        
        expected_question = "Is your job in the same occupation code as when you were given your previous permission?"
        if previous_question_id:
            self.judge_criteria.append(f"After Question {previous_question_id} was answered, the agent must ask '{expected_question}'. The user answered '{answer}'.")
        else:
            self.judge_criteria.append(f"The agent must start the assessment by asking '{expected_question}'. The user answered '{answer}'.")
            
        return self

    def still_with_same_employer(self, answer: str, previous_question_id: int | None = None) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append(answer)
        
        expected_question = "Are you still working for the employer who gave you your current certificate of sponsorship?"
        if previous_question_id:
            self.judge_criteria.append(f"After Question {previous_question_id} was answered, the agent must ask '{expected_question}'. The user answered '{answer}'.")
        else:
            self.judge_criteria.append(f"The agent must start the assessment by asking '{expected_question}'. The user answered '{answer}'.")
            
        return self

    def clarify_question_55_terms(self) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append("What is meant by 'medium skilled extension deadline'?")
        self.judge_criteria.append("The agent should offer the following definition for 'medium skilled extension deadline': From 22 July 2025 onwards, new medium skilled job applications are not eligible for Skilled Worker visas. Only those who got their first CoS before this date can extend.")
        return self

    def did_you_get_first_cos_before_july_2025(self, answer: str, previous_question_id: int | None = None) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append(answer)
        
        expected_question = "If your occupation code is 'medium skilled', did you get your first certificate of sponsorship before 22 July 2025?"
        if previous_question_id:
            self.judge_criteria.append(f"After Question {previous_question_id} was answered, the agent must ask '{expected_question}'. The user answered '{answer}'.")
        else:
            self.judge_criteria.append(f"The agent must start the assessment by asking '{expected_question}'. The user answered '{answer}'.")
            
        return self

    def have_you_continually_held_skilled_worker_visas(self, answer: str, previous_question_id: int | None = None) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append(answer)
        
        expected_question = "Have you continually held one or more Skilled Worker visas since you got your first certificate of sponsorship?"
        if previous_question_id:
            self.judge_criteria.append(f"After Question {previous_question_id} was answered, the agent must ask '{expected_question}'. The user answered '{answer}'.")
        else:
            self.judge_criteria.append(f"The agent must start the assessment by asking '{expected_question}'. The user answered '{answer}'.")
            
        return self

    def when_did_you_receive_first_cos(self, answer: str, previous_question_id: int | None = None) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append(answer)
        
        expected_question = "When did you receive your first certificate of sponsorship?"
        if previous_question_id:
            self.judge_criteria.append(f"After Question {previous_question_id} was answered, the agent must ask '{expected_question}'. The user answered '{answer}'.")
        else:
            self.judge_criteria.append(f"The agent must start the assessment by asking '{expected_question}'. The user answered '{answer}'.")
            
        return self

    def clarify_question_58_terms(self) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append("What is meant by 'pre-April 2024 salary rules'?")
        self.judge_criteria.append("The agent should offer the following definition for 'pre-April 2024 salary rules': If you got your first CoS before 4 April 2024, you may meet lower salary thresholds, and your salary may include guaranteed allowances like London weighting.")
        return self

    def meeting_lower_salary_requirements_pre_april_2024(self, answer: str, previous_question_id: int | None = None) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append(answer)
        
        expected_question = "For CoS before 4 April 2024: Are you meeting the lower salary requirements applicable to your original CoS date?"
        if previous_question_id:
            self.judge_criteria.append(f"After Question {previous_question_id} was answered, the agent must ask '{expected_question}'. The user answered '{answer}'.")
        else:
            self.judge_criteria.append(f"The agent must start the assessment by asking '{expected_question}'. The user answered '{answer}'.")
            
        return self

    def can_you_pay_extension_fee(self, answer: str, previous_question_id: int | None = None) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append(answer)
        
        expected_question = "Can you pay the extension application fee (£885 for up to 3 years, £1,751 for more than 3 years)?"
        if previous_question_id:
            self.judge_criteria.append(f"After Question {previous_question_id} was answered, the agent must ask '{expected_question}'. The user answered '{answer}'.")
        else:
            self.judge_criteria.append(f"The agent must start the assessment by asking '{expected_question}'. The user answered '{answer}'.")
            
        return self

    def can_you_pay_healthcare_surcharge_extension(self, answer: str, previous_question_id: int | None = None) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append(answer)
        
        expected_question = "Can you pay the healthcare surcharge for the extension period?"
        if previous_question_id:
            self.judge_criteria.append(f"After Question {previous_question_id} was answered, the agent must ask '{expected_question}'. The user answered '{answer}'.")
        else:
            self.judge_criteria.append(f"The agent must start the assessment by asking '{expected_question}'. The user answered '{answer}'.")
            
        return self

    def clarify_question_61_terms(self) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append("What is meant by 'proving English again'?")
        self.judge_criteria.append("The agent should offer the following definition for 'proving English again': If you already proved English in a previous visa application, you don't need to prove it again when extending. If extending from before 8 January 2026, you only need level B1, not B2.")
        return self

    def have_you_already_proved_english_for_extension(self, answer: str, previous_question_id: int | None = None) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append(answer)
        
        expected_question = "Have you already proved your knowledge of English in your previous visa application?"
        if previous_question_id:
            self.judge_criteria.append(f"After Question {previous_question_id} was answered, the agent must ask '{expected_question}'. The user answered '{answer}'.")
        else:
            self.judge_criteria.append(f"The agent must start the assessment by asking '{expected_question}'. The user answered '{answer}'.")
            
        return self

    def clarify_question_62_terms(self) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append("What is meant by 'travel restrictions during processing'?")
        self.judge_criteria.append("The agent should offer the following definition for 'travel restrictions during processing': If you're extending or switching your visa from inside the UK, you must not travel outside the UK, Ireland, Channel Islands, or Isle of Man until you receive a decision. Your application will be withdrawn if you do.")
        return self

    def understand_travel_restrictions_extension(self, answer: str, previous_question_id: int | None = None) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append(answer)
        
        expected_question = "Do you understand you must not travel outside the UK, Ireland, Channel Islands, or Isle of Man until you get a decision?"
        if previous_question_id:
            self.judge_criteria.append(f"After Question {previous_question_id} was answered, the agent must ask '{expected_question}'. The user answered '{answer}'.")
        else:
            self.judge_criteria.append(f"The agent must start the assessment by asking '{expected_question}'. The user answered '{answer}'.")
            
        return self

    def clarify_question_63_terms(self) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append("What is meant by 'visas that cannot switch'?")
        self.judge_criteria.append("The agent should offer the following definition for 'visas that cannot switch': These visa types cannot switch to Skilled Worker visa from inside the UK: visit, short-term student, Parent of a Child Student, seasonal worker, domestic worker in a private household, immigration bail, or permission outside immigration rules.")
        return self

    def are_you_on_visa_that_cannot_switch(self, answer: str, previous_question_id: int | None = None) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append(answer)
        
        expected_question = "Are you currently in the UK on one of the following visa types that CANNOT switch: visit visa, short-term student visa, Parent of a Child Student visa, seasonal worker visa, domestic worker in a private household visa, immigration bail, or permission outside immigration rules?"
        if previous_question_id:
            self.judge_criteria.append(f"After Question {previous_question_id} was answered, the agent must ask '{expected_question}'. The user answered '{answer}'.")
        else:
            self.judge_criteria.append(f"The agent must start the assessment by asking '{expected_question}'. The user answered '{answer}'.")
            
        return self

    def does_job_meet_eligibility_requirements(self, answer: str, previous_question_id: int | None = None) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append(answer)
        
        expected_question = "Does your job meet the eligibility requirements for a Skilled Worker visa (approved employer, eligible occupation, salary thresholds)?"
        if previous_question_id:
            self.judge_criteria.append(f"After Question {previous_question_id} was answered, the agent must ask '{expected_question}'. The user answered '{answer}'.")
        else:
            self.judge_criteria.append(f"The agent must start the assessment by asking '{expected_question}'. The user answered '{answer}'.")
            
        return self

    def clarify_question_65_terms(self) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append("What is meant by 'dependant restrictions for medium skilled/care workers'?")
        self.judge_criteria.append("The agent should offer the following definition for 'dependant restrictions for medium skilled/care workers': If you switch to work as a care worker, senior care worker, or in a medium skilled job, your partner and children cannot switch to this visa as your dependants.")
        return self

    def switching_to_care_worker_or_medium_skilled(self, answer: str, previous_question_id: int | None = None) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append(answer)
        
        expected_question = "Are you switching to work as a care worker, senior care worker, or in a medium skilled job?"
        if previous_question_id:
            self.judge_criteria.append(f"After Question {previous_question_id} was answered, the agent must ask '{expected_question}'. The user answered '{answer}'.")
        else:
            self.judge_criteria.append(f"The agent must start the assessment by asking '{expected_question}'. The user answered '{answer}'.")
            
        return self

    def understand_dependant_restrictions(self, answer: str, previous_question_id: int | None = None) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append(answer)
        
        expected_question = "Important: If switching to care worker/senior care worker/medium skilled job, your partner and children CANNOT switch as your dependants. Do you understand this?"
        if previous_question_id:
            self.judge_criteria.append(f"After Question {previous_question_id} was answered, the agent must ask '{expected_question}'. The user answered '{answer}'.")
        else:
            self.judge_criteria.append(f"The agent must start the assessment by asking '{expected_question}'. The user answered '{answer}'.")
            
        return self

    def clarify_question_67_terms(self) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append("What is meant by 'B2 English for switching'?")
        self.judge_criteria.append("The agent should offer the following definition for 'B2 English for switching': Switching from another visa requires level B2 English (upper intermediate). This is higher than the B1 requirement for extending an existing Skilled Worker visa.")
        return self

    def can_you_prove_english_at_b2_for_switching(self, answer: str, previous_question_id: int | None = None) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append(answer)
        
        expected_question = "Can you prove your knowledge of English at level B2 (since you're switching, not extending)?"
        if previous_question_id:
            self.judge_criteria.append(f"After Question {previous_question_id} was answered, the agent must ask '{expected_question}'. The user answered '{answer}'.")
        else:
            self.judge_criteria.append(f"The agent must start the assessment by asking '{expected_question}'. The user answered '{answer}'.")
            
        return self

    def can_you_pay_switching_fee(self, answer: str, previous_question_id: int | None = None) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append(answer)
        
        expected_question = "Can you pay the switching application fee (£885 for up to 3 years, £1,751 for more than 3 years)?"
        if previous_question_id:
            self.judge_criteria.append(f"After Question {previous_question_id} was answered, the agent must ask '{expected_question}'. The user answered '{answer}'.")
        else:
            self.judge_criteria.append(f"The agent must start the assessment by asking '{expected_question}'. The user answered '{answer}'.")
            
        return self

    def can_you_pay_healthcare_surcharge_switching(self, answer: str, previous_question_id: int | None = None) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append(answer)
        
        expected_question = "Can you pay the healthcare surcharge for your visa period?"
        if previous_question_id:
            self.judge_criteria.append(f"After Question {previous_question_id} was answered, the agent must ask '{expected_question}'. The user answered '{answer}'.")
        else:
            self.judge_criteria.append(f"The agent must start the assessment by asking '{expected_question}'. The user answered '{answer}'.")
            
        return self

    def clarify_question_70_terms(self) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append("What is meant by '12-month exemption'?")
        self.judge_criteria.append("The agent should offer the following definition for '12-month exemption': If you've been in the UK with a valid visa for at least 12 months, you don't need to prove you have £1,270 maintenance funds when switching visas.")
        return self

    def been_in_uk_at_least_12_months(self, answer: str, previous_question_id: int | None = None) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append(answer)
        
        expected_question = "Have you been in the UK for at least 12 months with a valid visa?"
        if previous_question_id:
            self.judge_criteria.append(f"After Question {previous_question_id} was answered, the agent must ask '{expected_question}'. The user answered '{answer}'.")
        else:
            self.judge_criteria.append(f"The agent must start the assessment by asking '{expected_question}'. The user answered '{answer}'.")
            
        return self

    def have_1270_or_employer_certify_switching(self, answer: str, previous_question_id: int | None = None) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append(answer)
        
        expected_question = "Do you have at least £1,270 in your bank account (available for 28 consecutive days, day 28 within 31 days of applying), OR can your employer certify maintenance?"
        if previous_question_id:
            self.judge_criteria.append(f"After Question {previous_question_id} was answered, the agent must ask '{expected_question}'. The user answered '{answer}'.")
        else:
            self.judge_criteria.append(f"The agent must start the assessment by asking '{expected_question}'. The user answered '{answer}'.")
            
        return self

    def understand_travel_restrictions_switching(self, answer: str, previous_question_id: int | None = None) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append(answer)
        
        expected_question = "Do you understand you must not travel outside the UK, Ireland, Channel Islands, or Isle of Man until you get a decision?"
        if previous_question_id:
            self.judge_criteria.append(f"After Question {previous_question_id} was answered, the agent must ask '{expected_question}'. The user answered '{answer}'.")
        else:
            self.judge_criteria.append(f"The agent must start the assessment by asking '{expected_question}'. The user answered '{answer}'.")
            
        return self

    def what_is_salary_for_pre_april_2024_cos(self, answer: str, previous_question_id: int | None = None) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append(answer)
        
        expected_question = "For certificates of sponsorship received before 4 April 2024: What is your annual salary?"
        if previous_question_id:
            self.judge_criteria.append(f"After Question {previous_question_id} was answered, the agent must ask '{expected_question}'. The user answered '{answer}'.")
        else:
            self.judge_criteria.append(f"The agent must start the assessment by asking '{expected_question}'. The user answered '{answer}'.")
            
        return self

    def does_salary_meet_pre_april_2024_requirements(self, answer: str, previous_question_id: int | None = None) -> 'SkilledWorkerVisaScenario':
        self.user_inputs.append(answer)
        
        expected_question = "Does your salary (potentially including guaranteed allowances like London weighting) meet the lower salary requirements applicable to pre-4 April 2024 CoS dates?"
        if previous_question_id:
            self.judge_criteria.append(f"After Question {previous_question_id} was answered, the agent must ask '{expected_question}'. The user answered '{answer}'.")
        else:
            self.judge_criteria.append(f"The agent must start the assessment by asking '{expected_question}'. The user answered '{answer}'.")
            
        return self
