from mcp_server.models.eligibility_check_models import Decision, NextQuestion, Question

QUESTIONS = {
    1: "Are you applying for a Skilled Worker visa for the first time, extending an existing Skilled Worker visa, or switching from another visa type?",
    2: "Do you have a confirmed job offer from a UK employer before applying for your visa?",
    3: "Has your employer been approved by the Home Office as a licensed sponsor?",
    4: "Do you have a certificate of sponsorship (CoS) from your employer with information about the role you've been offered in the UK?",
    5: "Do you know the 4-digit occupation code for your job?",
    6: "Is your occupation code listed in the table of eligible jobs for the Skilled Worker visa?",
    7: "Is your occupation code listed as 'higher skilled' or 'medium skilled'?",
    8: "For higher skilled jobs: You are eligible to proceed with your application. Continue to salary checks.",
    9: "For medium skilled jobs: Is your job on either the immigration salary list OR the temporary shortage list?",
    10: "Are you applying for a role as a care worker (code 6135) or senior care worker (code 6136) in England?",
    11: "Is your employer registered with the Care Quality Commission?",
    12: "When did you (or will you) receive your certificate of sponsorship?",
    13: "What is your annual salary for the job offer (in GBP)?",
    14: "Is your job in healthcare or education with national pay scale rates?",
    15: "Does your healthcare or education job appear on the list of eligible healthcare and education jobs with national pay scales?",
    16: "What is the going rate for your job based on the national pay scale (NHS pay band or teaching role)?",
    17: "Is your annual salary at least £25,000?",
    18: "Is your annual salary at least the national pay scale going rate for your specific job?",
    19: "Is your annual salary at least the national pay scale going rate for your specific job?",
    20: "What is the standard going rate for your occupation code (from the going rates table)?",
    21: "Is your annual salary at least £41,700 AND at least the going rate for your occupation, whichever is higher?",
    22: "Is your annual salary at least £33,400?",
    23: "Is your job on the immigration salary list?",
    24: "For immigration salary list jobs: Is your salary at least the standard going rate for your job (even though the minimum is £33,400)?",
    25: "Are you under 26 years old on the date you apply?",
    26: "For under 26: Is your salary at least 70% of the standard going rate for your job?",
    27: "Are you currently in the UK on a Student visa studying at bachelor's degree level or above, OR have you been in the last 2 years with a Student or visit visa as your most recent visa?",
    28: "For current/recent students: Is your salary at least 70% of the standard going rate for your job?",
    29: "Are you currently in the UK on a Graduate visa, OR have you been in the last 2 years with a Graduate or visit visa as your most recent visa?",
    30: "For current/recent graduate visa holders: Is your salary at least 70% of the standard going rate for your job?",
    31: "Will you be working towards a recognised qualification in a UK regulated profession?",
    32: "For regulated profession training: Is your salary at least 70% of the standard going rate for your job?",
    33: "Will you be working towards full registration or chartered status in the job you're being sponsored for?",
    34: "For registration/chartered status training: Is your salary at least 70% of the standard going rate for your job?",
    35: "Do you have a PhD level qualification that's relevant to your job?",
    36: "Is your PhD in a STEM subject (science, technology, engineering, or maths)?",
    37: "For STEM PhD holders: Is your salary at least 80% of the standard going rate for your job, and at least £33,400?",
    38: "For non-STEM PhD holders: Is your salary at least 90% of the standard going rate for your job, and at least £37,500?",
    39: "Will you be working in a postdoctoral position in science or higher education (occupation codes 2111, 2112, 2113, 2114, 2115, 2119, 2162, or 2311)?",
    40: "For postdoctoral positions: Is your salary at least 70% of the standard going rate for your job?",
    41: "Note: If you qualified under certain 70% salary routes, your total stay in the UK cannot be more than 4 years (including any time on a Graduate visa). Do you understand this limitation?",
    42: "Are you a national of one of the following majority English-speaking countries: Antigua and Barbuda, Australia, the Bahamas, Barbados, Belize, British overseas territories, Canada, Dominica, Grenada, Guyana, Jamaica, Malta, New Zealand, St Kitts and Nevis, St Lucia, St Vincent and the Grenadines, Trinidad and Tobago, or USA?",
    43: "Are you a doctor, dentist, nurse, midwife, or vet who has already passed an English language assessment accepted by the relevant regulated professional body?",
    44: "Have you already proved your knowledge of English in a previous successful visa application?",
    45: "Can you prove your knowledge of English in one of the following ways: UK school qualification (GCSE, A Level, Scottish qualifications), degree from UK institution taught in English, degree from non-UK institution taught in English with Ecctis assessment, or passing an approved SELT at level B2?",
    46: "Which method will you use to prove your English knowledge?",
    47: "Can you pass a Secure English Language Test (SELT) at level B2 on the CEFR scale, proving you can read, write, speak and understand English?",
    48: "Can you pay the visa application fee (ranging from £590 to £1,519 depending on your circumstances and visa length)?",
    49: "Can you pay the healthcare surcharge (usually £1,035 per year for the full duration of your visa)?",
    50: "Do you have at least £1,270 in your bank account that has been available for at least 28 consecutive days (with day 28 within 31 days of applying)?",
    51: "Can your employer certify maintenance on your certificate of sponsorship, confirming they can cover your costs during your first month in the UK up to £1,270?",
    52: "Do you have the same job as when you were given your previous permission to enter or stay in the UK?",
    53: "Is your job in the same occupation code as when you were given your previous permission?",
    54: "Are you still working for the employer who gave you your current certificate of sponsorship?",
    55: "If your occupation code is 'medium skilled', did you get your first certificate of sponsorship before 22 July 2025?",
    56: "Have you continually held one or more Skilled Worker visas since you got your first certificate of sponsorship?",
    57: "When did you receive your first certificate of sponsorship?",
    58: "For CoS before 4 April 2024: Are you meeting the lower salary requirements applicable to your original CoS date?",
    59: "Can you pay the extension application fee (£885 for up to 3 years, £1,751 for more than 3 years)?",
    60: "Can you pay the healthcare surcharge for the extension period?",
    61: "Have you already proved your knowledge of English in your previous visa application?",
    62: "Do you understand you must not travel outside the UK, Ireland, Channel Islands, or Isle of Man until you get a decision?",
    63: "Are you currently in the UK on one of the following visa types that CANNOT switch: visit visa, short-term student visa, Parent of a Child Student visa, seasonal worker visa, domestic worker in a private household visa, immigration bail, or permission outside immigration rules?",
    64: "Does your job meet the eligibility requirements for a Skilled Worker visa (approved employer, eligible occupation, salary thresholds)?",
    65: "Are you switching to work as a care worker, senior care worker, or in a medium skilled job?",
    66: "Important: If switching to care worker/senior care worker/medium skilled job, your partner and children CANNOT switch as your dependants. Do you understand this?",
    67: "Can you prove your knowledge of English at level B2 (since you're switching, not extending)?",
    68: "Can you pay the switching application fee (£885 for up to 3 years, £1,751 for more than 3 years)?",
    69: "Can you pay the healthcare surcharge for your visa period?",
    70: "Have you been in the UK for at least 12 months with a valid visa?",
    71: "Do you have at least £1,270 in your bank account (available for 28 consecutive days, day 28 within 31 days of applying), OR can your employer certify maintenance?",
    72: "Do you understand you must not travel outside the UK, Ireland, Channel Islands, or Isle of Man until you get a decision?",
    73: "For certificates of sponsorship received before 4 April 2024: What is your annual salary?",
    74: "Does your salary (potentially including guaranteed allowances like London weighting) meet the lower salary requirements applicable to pre-4 April 2024 CoS dates?",
}

def get_next_question_for_skilled_worker_visa_eligibility_check(next_question: int) -> Question:
    if QUESTIONS.get(next_question) is None:
        raise ValueError(f"Question index {next_question} not recognised")
    
    question = Question.new(QUESTIONS[next_question])
    
    match next_question:
        case 1:
            return question \
                .add_answer_and_outcome("Applying for the first time from outside the UK", NextQuestion.new(2)) \
                .add_answer_and_outcome("Extending an existing Skilled Worker visa", NextQuestion.new(52)) \
                .add_answer_and_outcome("Switching from another visa type while in the UK", NextQuestion.new(63)) \
                .add_to_glossary("Skilled Worker visa", "A visa that allows you to come to or stay in the UK to do an eligible job with an approved employer. It replaced the Tier 2 (General) work visa.")
        
        case 2:
            return question \
                .add_answer_and_outcome("Yes", NextQuestion.new(3)) \
                .add_answer_and_outcome("No", Decision.new(False, "You must have a confirmed job offer before you apply for your visa.")) \
                .add_to_glossary("confirmed job offer", "A formal offer of employment from a UK employer that meets the Skilled Worker visa requirements, confirmed by a certificate of sponsorship.")
        
        case 3:
            return question \
                .add_answer_and_outcome("Yes", NextQuestion.new(4)) \
                .add_answer_and_outcome("No", Decision.new(False, "Your employer must be approved by the Home Office as a licensed sponsor. They can apply for a sponsor licence if eligible, which costs £574 for small businesses/charities or £1,579 for medium/large organisations and takes around 8 weeks to process.")) \
                .add_to_glossary("licensed sponsor", "An employer registered with the UK Home Office who has been granted permission to sponsor skilled workers. You can view the list of approved UK employers on the GOV.UK website.")
        
        case 4:
            return question \
                .add_answer_and_outcome("Yes", NextQuestion.new(5)) \
                .add_answer_and_outcome("No", Decision.new(False, "You must have a certificate of sponsorship (CoS) from your employer. This is provided by your employer once they verify you meet the eligibility requirements.")) \
                .add_to_glossary("certificate of sponsorship", "An electronic record (not a physical document) issued by your employer with a unique reference number. It contains information about your job role and personal details. You must apply for your visa within 3 months of receiving it.")
        
        case 5:
            return question \
                .add_answer_and_outcome("Yes", NextQuestion.new(6)) \
                .add_answer_and_outcome("No", Decision.new(False, "You need to know your 4-digit occupation code. Ask your employer for it, or search for your job in the CASCOT occupation coding tool on GOV.UK.")) \
                .add_to_glossary("occupation code", "A 4-digit code from the UK Standard Occupational Classification (SOC) system that identifies your specific job type. Different occupation codes have different eligibility requirements and going rates.")
        
        case 6:
            return question \
                .add_answer_and_outcome("Yes", NextQuestion.new(7)) \
                .add_answer_and_outcome("No", Decision.new(False, "Your job must be on the list of eligible occupations for the Skilled Worker visa. Check the table of eligible jobs on GOV.UK using your occupation code.")) \
                .add_to_glossary("eligible occupations", "Jobs that are at RQF level 3 or above (equivalent to A level) with specific occupation codes listed in the UK's immigration rules. The table is sorted by occupation code on GOV.UK.")
        
        case 7:
            return question \
                .add_answer_and_outcome("Higher skilled", NextQuestion.new(8)) \
                .add_answer_and_outcome("Medium skilled", NextQuestion.new(9)) \
                .add_to_glossary("higher skilled vs medium skilled", "Higher skilled jobs can apply directly for a Skilled Worker visa. Medium skilled jobs can only apply if the job is also on the immigration salary list or temporary shortage list.")
        
        case 8:
            return question \
                .add_answer_and_outcome("Continue", NextQuestion.new(10))
        
        case 9:
            return question \
                .add_answer_and_outcome("Yes", NextQuestion.new(10)) \
                .add_answer_and_outcome("No", Decision.new(False, "Medium skilled jobs must be on either the immigration salary list OR the temporary shortage list to be eligible for a Skilled Worker visa.")) \
                .add_to_glossary("immigration salary list", "A list of skilled jobs which have lower salary requirements (minimum £33,400) and lower visa application fees. Check if your job is on this list on GOV.UK.") \
                .add_to_glossary("temporary shortage list", "A list of occupations where there is a shortage of workers in the UK, making them eligible for the Skilled Worker visa even if medium skilled.")
        
        case 10:
            return question \
                .add_answer_and_outcome("Yes", NextQuestion.new(11)) \
                .add_answer_and_outcome("No", NextQuestion.new(12)) \
                .add_to_glossary("care worker codes", "Care workers have occupation code 6135, senior care workers have code 6136. These roles have specific registration requirements in England.")
        
        case 11:
            return question \
                .add_answer_and_outcome("Yes", NextQuestion.new(12)) \
                .add_answer_and_outcome("No", Decision.new(False, "Care workers (code 6135) and senior care workers (code 6136) in England must have an employer registered with the Care Quality Commission (CQC). Check if your employer is registered on the CQC website.")) \
                .add_to_glossary("Care Quality Commission", "The independent regulator of health and adult social care services in England. Care worker employers must be registered with the CQC.")
        
        case 12:
            return question \
                .add_answer_and_outcome("On or after 4 April 2024", NextQuestion.new(13)) \
                .add_answer_and_outcome("Before 4 April 2024", NextQuestion.new(73)) \
                .add_to_glossary("CoS date significance", "The date you received your certificate of sponsorship determines which salary rules apply. Different thresholds apply for CoS received before vs. on or after 4 April 2024.")
        
        case 13:
            return question \
                .add_answer_and_outcome("Provide amount", NextQuestion.new(14)) \
                .add_to_glossary("annual salary", "The gross annual salary (before tax) that your employer will pay you for the sponsored role, as stated on your certificate of sponsorship. This must meet minimum thresholds.")
        
        case 14:
            return question \
                .add_answer_and_outcome("Yes", NextQuestion.new(15)) \
                .add_answer_and_outcome("No", NextQuestion.new(20)) \
                .add_to_glossary("healthcare and education jobs", "Some healthcare and education jobs have going rates based on national pay scales (e.g., NHS pay bands), with a minimum of £25,000 instead of £41,700.")
        
        case 15:
            return question \
                .add_answer_and_outcome("Yes", NextQuestion.new(16)) \
                .add_answer_and_outcome("No", NextQuestion.new(20)) \
                .add_to_glossary("eligible healthcare and education jobs list", "A specific list of healthcare and education roles with national pay scale rates. Check the GOV.UK page 'If you work in healthcare or education' to see if your job is included.")
        
        case 16:
            return question \
                .add_answer_and_outcome("Provide going rate", NextQuestion.new(17)) \
                .add_to_glossary("national pay scale going rate", "For eligible healthcare/education jobs, the going rate is based on NHS pay bands or teaching/education leadership pay scales, which vary by role and UK region.")
        
        case 17:
            return question \
                .add_answer_and_outcome("Yes", NextQuestion.new(19)) \
                .add_answer_and_outcome("No", NextQuestion.new(18))
        
        case 18:
            return question \
                .add_answer_and_outcome("Yes", Decision.new(False, "Your salary must be at least £25,000 AND at least the national pay scale going rate for your job.")) \
                .add_answer_and_outcome("No", Decision.new(False, "Your salary must be at least £25,000 AND at least the national pay scale going rate for your job."))
        
        case 19:
            return question \
                .add_answer_and_outcome("Yes", NextQuestion.new(42)) \
                .add_answer_and_outcome("No", Decision.new(False, "Your salary must be at least the national pay scale going rate for your specific healthcare or education job."))
        
        case 20:
            return question \
                .add_answer_and_outcome("Provide going rate", NextQuestion.new(21)) \
                .add_to_glossary("going rate", "The minimum salary level set for your specific occupation code. Each code has its own going rate listed in the going rates table on GOV.UK. You must be paid at least £41,700 OR the going rate, whichever is higher.")
        
        case 21:
            return question \
                .add_answer_and_outcome("Yes", NextQuestion.new(42)) \
                .add_answer_and_outcome("No", NextQuestion.new(22))
        
        case 22:
            return question \
                .add_answer_and_outcome("Yes", NextQuestion.new(23)) \
                .add_answer_and_outcome("No", Decision.new(False, "Your salary is below the minimum threshold of £33,400, which is the absolute minimum even for reduced salary categories. You are not eligible for a Skilled Worker visa."))
        
        case 23:
            return question \
                .add_answer_and_outcome("Yes", NextQuestion.new(24)) \
                .add_answer_and_outcome("No", NextQuestion.new(25))
        
        case 24:
            return question \
                .add_answer_and_outcome("Yes", NextQuestion.new(42)) \
                .add_answer_and_outcome("No", Decision.new(False, "Even though your job is on the immigration salary list with a minimum of £33,400, you must still be paid at least the standard going rate for your occupation."))
        
        case 25:
            return question \
                .add_answer_and_outcome("Yes", NextQuestion.new(26)) \
                .add_answer_and_outcome("No", NextQuestion.new(27))
        
        case 26:
            return question \
                .add_answer_and_outcome("Yes", NextQuestion.new(41)) \
                .add_answer_and_outcome("No", Decision.new(False, "If you are under 26, your salary must be at least 70% of the standard going rate for your job, and at least £33,400."))
        
        case 27:
            return question \
                .add_answer_and_outcome("Yes", NextQuestion.new(28)) \
                .add_answer_and_outcome("No", NextQuestion.new(29)) \
                .add_to_glossary("Student visa holder eligibility", "You can get a reduced salary threshold (70% of going rate) if you're currently on a Student visa studying at bachelor's level or above, or held one in the last 2 years with Student/visit visa as most recent.")
        
        case 28:
            return question \
                .add_answer_and_outcome("Yes", NextQuestion.new(41)) \
                .add_answer_and_outcome("No", Decision.new(False, "As a current or recent Student visa holder, your salary must be at least 70% of the standard going rate for your job, and at least £33,400."))
        
        case 29:
            return question \
                .add_answer_and_outcome("Yes", NextQuestion.new(30)) \
                .add_answer_and_outcome("No", NextQuestion.new(31)) \
                .add_to_glossary("Graduate visa holder eligibility", "You can get a reduced salary threshold (70% of going rate) if you're currently on a Graduate visa, or held one in the last 2 years with Graduate/visit visa as most recent.")
        
        case 30:
            return question \
                .add_answer_and_outcome("Yes", NextQuestion.new(41)) \
                .add_answer_and_outcome("No", Decision.new(False, "As a current or recent Graduate visa holder, your salary must be at least 70% of the standard going rate for your job, and at least £33,400."))
        
        case 31:
            return question \
                .add_answer_and_outcome("Yes", NextQuestion.new(32)) \
                .add_answer_and_outcome("No", NextQuestion.new(33)) \
                .add_to_glossary("UK regulated profession", "A profession that requires specific qualifications or registration to practice legally in the UK, such as doctors, lawyers, architects, or engineers.")
        
        case 32:
            return question \
                .add_answer_and_outcome("Yes", NextQuestion.new(41)) \
                .add_answer_and_outcome("No", Decision.new(False, "If working towards a recognised qualification in a UK regulated profession, your salary must be at least 70% of the standard going rate, and at least £33,400."))
        
        case 33:
            return question \
                .add_answer_and_outcome("Yes", NextQuestion.new(34)) \
                .add_answer_and_outcome("No", NextQuestion.new(35)) \
                .add_to_glossary("chartered status", "Professional recognition awarded by a chartered body (like the Royal Institution of Chartered Surveyors) showing you meet the highest standards in your profession.")
        
        case 34:
            return question \
                .add_answer_and_outcome("Yes", NextQuestion.new(41)) \
                .add_answer_and_outcome("No", Decision.new(False, "If working towards full registration or chartered status in your sponsored job, your salary must be at least 70% of the standard going rate, and at least £33,400."))
        
        case 35:
            return question \
                .add_answer_and_outcome("Yes", NextQuestion.new(36)) \
                .add_answer_and_outcome("No", NextQuestion.new(39)) \
                .add_to_glossary("PhD level qualification", "A UK PhD or equivalent doctorate-level overseas qualification (you'll need to apply through Ecctis to check overseas equivalency) that is relevant to the job you'll be doing in the UK.")
        
        case 36:
            return question \
                .add_answer_and_outcome("Yes (STEM PhD)", NextQuestion.new(37)) \
                .add_answer_and_outcome("No (non-STEM PhD)", NextQuestion.new(38)) \
                .add_to_glossary("STEM PhD", "A PhD in Science, Technology, Engineering, or Mathematics. STEM PhD holders can be paid 80% of the going rate (minimum £33,400), while non-STEM PhD holders need 90% (minimum £37,500).")
        
        case 37:
            return question \
                .add_answer_and_outcome("Yes", NextQuestion.new(42)) \
                .add_answer_and_outcome("No", Decision.new(False, "STEM PhD holders must earn at least 80% of the standard going rate for their job, and at least £33,400."))
        
        case 38:
            return question \
                .add_answer_and_outcome("Yes", NextQuestion.new(42)) \
                .add_answer_and_outcome("No", Decision.new(False, "Non-STEM PhD holders must earn at least 90% of the standard going rate for their job, and at least £37,500."))
        
        case 39:
            return question \
                .add_answer_and_outcome("Yes", NextQuestion.new(40)) \
                .add_answer_and_outcome("No", Decision.new(False, "You do not meet any of the criteria for reduced salary thresholds. Your salary must be at least £41,700 AND the standard going rate for your job, whichever is higher.")) \
                .add_to_glossary("postdoctoral position codes", "Specific occupation codes for postdoctoral science/higher education roles: 2111 (chemical scientists), 2112 (biological scientists), 2113 (biochemists/biomedical scientists), 2114 (physical scientists), 2115 (social/humanities scientists), 2119 (natural/social science professionals), 2162 (other researchers), 2311 (higher education teaching professionals).")
        
        case 40:
            return question \
                .add_answer_and_outcome("Yes", NextQuestion.new(41)) \
                .add_answer_and_outcome("No", Decision.new(False, "Postdoctoral positions in the eligible science/higher education roles must earn at least 70% of the standard going rate and at least £33,400."))
        
        case 41:
            return question \
                .add_answer_and_outcome("Yes, I understand", NextQuestion.new(42)) \
                .add_answer_and_outcome("Tell me more", NextQuestion.new(42)) \
                .add_to_glossary("4-year limit for 70% salary routes", "If you qualify for a visa using the 70% salary threshold (under 26, student/graduate, professional training, or postdoctoral position), your total UK stay cannot exceed 4 years, including any time on a Graduate visa.")
        
        case 42:
            return question \
                .add_answer_and_outcome("Yes", NextQuestion.new(48)) \
                .add_answer_and_outcome("No", NextQuestion.new(43)) \
                .add_to_glossary("English-speaking countries", "Nationals of these countries are exempt from proving English: Antigua and Barbuda, Australia, Bahamas, Barbados, Belize, British overseas territories, Canada, Dominica, Grenada, Guyana, Jamaica, Malta, New Zealand, St Kitts and Nevis, St Lucia, St Vincent and the Grenadines, Trinidad and Tobago, USA.")
        
        case 43:
            return question \
                .add_answer_and_outcome("Yes", NextQuestion.new(48)) \
                .add_answer_and_outcome("No", NextQuestion.new(44)) \
                .add_to_glossary("regulated professional body English assessment", "Doctors, dentists, nurses, midwives, and vets who have passed English assessments accepted by their professional bodies (GMC, GDC, NMC, RCVS) are exempt from additional English proof.")
        
        case 44:
            return question \
                .add_answer_and_outcome("Yes", NextQuestion.new(48)) \
                .add_answer_and_outcome("No", NextQuestion.new(45))
        
        case 45:
            return question \
                .add_answer_and_outcome("Yes", NextQuestion.new(46)) \
                .add_answer_and_outcome("No", Decision.new(False, "You must prove your knowledge of English to be eligible for a Skilled Worker visa."))
        
        case 46:
            return question \
                .add_answer_and_outcome("UK school qualification (GCSE, A Level, Scottish qualifications started before age 18)", NextQuestion.new(48)) \
                .add_answer_and_outcome("Degree from UK institution taught in English", NextQuestion.new(48)) \
                .add_answer_and_outcome("Degree from non-UK institution taught in English with Ecctis confirmation", NextQuestion.new(48)) \
                .add_answer_and_outcome("Approved SELT at level B2 or higher", NextQuestion.new(47)) \
                .add_to_glossary("UK school qualification for English", "GCSE, A Level, Scottish National Qualification level 4 or 5, or Scottish Higher/Advanced Higher in English - must have begun the qualification when under 18.") \
                .add_to_glossary("Ecctis", "The UK agency that assesses overseas qualifications. If your degree was taught in English but awarded outside the UK, Ecctis can confirm it's equivalent to a UK bachelor's degree or higher.")
        
        case 47:
            return question \
                .add_answer_and_outcome("Yes", NextQuestion.new(48)) \
                .add_answer_and_outcome("No", Decision.new(False, "You must pass a Secure English Language Test (SELT) at level B2 on the Common European Framework of Reference for Languages (CEFR) scale, proving you can read, write, speak and understand English.")) \
                .add_to_glossary("SELT", "Secure English Language Test from an approved provider. For new Skilled Worker visa applications, you need level B2 on the CEFR scale.") \
                .add_to_glossary("CEFR scale", "Common European Framework of Reference for Languages - a standardized measure of language ability. B2 is upper intermediate level.")
        
        case 48:
            return question \
                .add_answer_and_outcome("Yes", NextQuestion.new(49)) \
                .add_answer_and_outcome("No", Decision.new(False, "You must pay the visa application fee. For new applications from outside the UK, standard fees are £769 (up to 3 years) or £1,519 (more than 3 years). Immigration salary list jobs have reduced fees of £590 or £1,160.")) \
                .add_to_glossary("application fee structure", "Fees vary by visa length and whether your job is on the immigration salary list. Outside UK: £769/£1,519 (standard) or £590/£1,160 (ISL). Inside UK: £885/£1,751 (standard) or £590/£1,160 (ISL).")
        
        case 49:
            return question \
                .add_answer_and_outcome("Yes", NextQuestion.new(50)) \
                .add_answer_and_outcome("No", Decision.new(False, "You must pay the healthcare surcharge (Immigration Health Surcharge/IHS) for each year of your stay. This is usually £1,035 per year and gives you access to the UK's National Health Service (NHS).")) \
                .add_to_glossary("healthcare surcharge", "Also called the Immigration Health Surcharge (IHS), this is usually £1,035 per year. You pay upfront for the full duration of your visa. Some healthcare workers may be exempt.")
        
        case 50:
            return question \
                .add_answer_and_outcome("Yes", Decision.new(True, "You meet all the requirements for a Skilled Worker visa. You can apply online up to 3 months before your job start date. Your application will typically be decided within 3 weeks (outside UK) or 8 weeks (inside UK).")) \
                .add_answer_and_outcome("No", NextQuestion.new(51)) \
                .add_to_glossary("maintenance funds", "Money to support yourself when you arrive in the UK. Must be at least £1,270, available for 28 consecutive days, with day 28 within 31 days of applying.")
        
        case 51:
            return question \
                .add_answer_and_outcome("Yes", Decision.new(True, "You meet all the requirements for a Skilled Worker visa. Your employer will certify maintenance on your certificate of sponsorship. You can apply online up to 3 months before your job start date.")) \
                .add_answer_and_outcome("No", Decision.new(False, "You must prove you have at least £1,270 available to support yourself in the UK, either in your bank account (available for 28 consecutive days) OR certified by your employer on your certificate of sponsorship.")) \
                .add_to_glossary("employer certifies maintenance", "Your employer can confirm on your certificate of sponsorship that they will cover your costs during your first month in the UK, up to £1,270. Check the 'sponsor certifies maintenance' section under 'Additional data' on your CoS.")
        
        case 52:
            return question \
                .add_answer_and_outcome("Yes", NextQuestion.new(53)) \
                .add_answer_and_outcome("No", Decision.new(False, "You cannot extend your visa if you've changed jobs. You must apply to update your visa instead if you have a new job or employer.")) \
                .add_to_glossary("extending vs updating", "Extending = same job, employer, and occupation code. Updating = changed job, employer, or occupation code. Different application processes apply.")
        
        case 53:
            return question \
                .add_answer_and_outcome("Yes", NextQuestion.new(54)) \
                .add_answer_and_outcome("No", Decision.new(False, "You cannot extend your visa if your job is in a different occupation code. You must apply to update your visa instead."))
        
        case 54:
            return question \
                .add_answer_and_outcome("Yes", NextQuestion.new(55)) \
                .add_answer_and_outcome("No", Decision.new(False, "You cannot extend your visa if you've changed employers. You must apply to update your visa instead."))
        
        case 55:
            return question \
                .add_answer_and_outcome("Not applicable (higher skilled job)", NextQuestion.new(57)) \
                .add_answer_and_outcome("Yes (got CoS before 22 July 2025)", NextQuestion.new(56)) \
                .add_answer_and_outcome("No (got CoS on or after 22 July 2025)", Decision.new(False, "Medium skilled jobs can only be extended if you got your first certificate of sponsorship before 22 July 2025.")) \
                .add_to_glossary("medium skilled extension deadline", "From 22 July 2025 onwards, new medium skilled job applications are not eligible for Skilled Worker visas. Only those who got their first CoS before this date can extend.")
        
        case 56:
            return question \
                .add_answer_and_outcome("Yes", NextQuestion.new(57)) \
                .add_answer_and_outcome("No", Decision.new(False, "Medium skilled job extensions require that you have continually held one or more Skilled Worker visas since you got your first certificate of sponsorship."))
        
        case 57:
            return question \
                .add_answer_and_outcome("On or after 4 April 2024", NextQuestion.new(21)) \
                .add_answer_and_outcome("Before 4 April 2024", NextQuestion.new(58))
        
        case 58:
            return question \
                .add_answer_and_outcome("Yes", NextQuestion.new(59)) \
                .add_answer_and_outcome("No", Decision.new(False, "You must meet the salary requirements that were in place when you received your first certificate of sponsorship. These may include allowances like London weighting if guaranteed for the length of your stay.")) \
                .add_to_glossary("pre-April 2024 salary rules", "If you got your first CoS before 4 April 2024, you may meet lower salary thresholds, and your salary may include guaranteed allowances like London weighting.")
        
        case 59:
            return question \
                .add_answer_and_outcome("Yes", NextQuestion.new(60)) \
                .add_answer_and_outcome("No", Decision.new(False, "You must pay the extension application fee. For extensions, fees are £885 (up to 3 years) or £1,751 (more than 3 years), or reduced fees if your job is on the immigration salary list."))
        
        case 60:
            return question \
                .add_answer_and_outcome("Yes", NextQuestion.new(61)) \
                .add_answer_and_outcome("No", Decision.new(False, "You must pay the healthcare surcharge for the extension period."))
        
        case 61:
            return question \
                .add_answer_and_outcome("Yes", NextQuestion.new(62)) \
                .add_answer_and_outcome("No", NextQuestion.new(45)) \
                .add_to_glossary("proving English again", "If you already proved English in a previous visa application, you don't need to prove it again when extending. If extending from before 8 January 2026, you only need level B1, not B2.")
        
        case 62:
            return question \
                .add_answer_and_outcome("Yes, I understand", Decision.new(True, "You are eligible to extend your Skilled Worker visa. Apply online before your current visa expires. You'll get a decision within 8 weeks. Do not travel outside the UK, Ireland, Channel Islands, or Isle of Man until you receive your decision.")) \
                .add_answer_and_outcome("No, tell me more", Decision.new(True, "You are eligible to extend your Skilled Worker visa. IMPORTANT: You must not travel outside the UK, Ireland, Channel Islands, or Isle of Man until you get a decision, or your application will be withdrawn. Apply online before your current visa expires.")) \
                .add_to_glossary("travel restrictions during processing", "If you're extending or switching your visa from inside the UK, you must not travel outside the UK, Ireland, Channel Islands, or Isle of Man until you receive a decision. Your application will be withdrawn if you do.")
        
        case 63:
            return question \
                .add_answer_and_outcome("Yes, I'm on one of those visas", Decision.new(False, "You cannot switch to a Skilled Worker visa from: visit visa, short-term student visa, Parent of a Child Student visa, seasonal worker visa, domestic worker in a private household visa, immigration bail, or permission outside immigration rules. You must leave the UK and apply for a Skilled Worker visa from abroad.")) \
                .add_answer_and_outcome("No, I'm on a different visa type", NextQuestion.new(64)) \
                .add_to_glossary("visas that cannot switch", "These visa types cannot switch to Skilled Worker visa from inside the UK: visit, short-term student, Parent of a Child Student, seasonal worker, domestic worker in a private household, immigration bail, or permission outside immigration rules.")
        
        case 64:
            return question \
                .add_answer_and_outcome("Yes", NextQuestion.new(65)) \
                .add_answer_and_outcome("No", Decision.new(False, "Your job must meet all eligibility requirements for a Skilled Worker visa: approved employer, certificate of sponsorship, eligible occupation, and salary thresholds."))
        
        case 65:
            return question \
                .add_answer_and_outcome("Yes", NextQuestion.new(66)) \
                .add_answer_and_outcome("No", NextQuestion.new(67)) \
                .add_to_glossary("dependant restrictions for medium skilled/care workers", "If you switch to work as a care worker, senior care worker, or in a medium skilled job, your partner and children cannot switch to this visa as your dependants.")
        
        case 66:
            return question \
                .add_answer_and_outcome("Yes, I understand", NextQuestion.new(67)) \
                .add_answer_and_outcome("Tell me more", NextQuestion.new(67))
        
        case 67:
            return question \
                .add_answer_and_outcome("Yes", NextQuestion.new(68)) \
                .add_answer_and_outcome("No", Decision.new(False, "When switching to a Skilled Worker visa (not extending), you must prove your English knowledge at level B2 on the CEFR scale.")) \
                .add_to_glossary("B2 English for switching", "Switching from another visa requires level B2 English (upper intermediate). This is higher than the B1 requirement for extending an existing Skilled Worker visa.")
        
        case 68:
            return question \
                .add_answer_and_outcome("Yes", NextQuestion.new(69)) \
                .add_answer_and_outcome("No", Decision.new(False, "You must pay the switching application fee. Fees are £885 (up to 3 years) or £1,751 (more than 3 years), or reduced fees if your job is on the immigration salary list."))
        
        case 69:
            return question \
                .add_answer_and_outcome("Yes", NextQuestion.new(70)) \
                .add_answer_and_outcome("No", Decision.new(False, "You must pay the healthcare surcharge for your visa period."))
        
        case 70:
            return question \
                .add_answer_and_outcome("Yes (exempt from maintenance requirement)", NextQuestion.new(72)) \
                .add_answer_and_outcome("No (less than 12 months in UK)", NextQuestion.new(71)) \
                .add_to_glossary("12-month exemption", "If you've been in the UK with a valid visa for at least 12 months, you don't need to prove you have £1,270 maintenance funds when switching visas.")
        
        case 71:
            return question \
                .add_answer_and_outcome("Yes", NextQuestion.new(72)) \
                .add_answer_and_outcome("No", Decision.new(False, "Since you've been in the UK for less than 12 months, you must prove you have at least £1,270 available (in your bank account for 28 consecutive days, with day 28 within 31 days of applying) OR your employer can certify maintenance."))
        
        case 72:
            return question \
                .add_answer_and_outcome("Yes, I understand", Decision.new(True, "You are eligible to switch to a Skilled Worker visa. Apply online before your current visa expires. You'll get a decision within 8 weeks. Do not travel outside the UK, Ireland, Channel Islands, or Isle of Man until you receive your decision.")) \
                .add_answer_and_outcome("No, tell me more", Decision.new(True, "You are eligible to switch to a Skilled Worker visa. IMPORTANT: You must not travel outside the UK, Ireland, Channel Islands, or Isle of Man until you get a decision, or your application will be withdrawn. Apply online before your current visa expires."))
        
        case 73:
            return question \
                .add_answer_and_outcome("Provide amount", NextQuestion.new(74))
        
        case 74:
            return question \
                .add_answer_and_outcome("Yes", NextQuestion.new(42)) \
                .add_answer_and_outcome("No", Decision.new(False, "You must meet the salary requirements that were in place when you received your certificate of sponsorship before 4 April 2024. Check the specific thresholds applicable to your CoS date."))

        case _:
            raise ValueError(f"Question index {next_question} not recognised")
