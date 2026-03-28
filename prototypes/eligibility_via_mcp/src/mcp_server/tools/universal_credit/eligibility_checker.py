from mcp_server.models.eligibility_check_models import Decision, NextQuestion, Question

QUESTIONS = {
    1: "Do you live in the UK?",
    2: "Are you aged 16 or 17?",
    3: "Are you aged 18 or over but under State Pension age?",
    4: "Do you have £16,000 or less in money, savings and investments?",
    5: "Are you an EU, EEA or Swiss citizen?",
    6: "Do you have settled or pre-settled status under the EU Settlement Scheme?",
    7: "Do you live with a partner?",
    8: "Is your partner eligible for Universal Credit?",
    9: "Has either you or your partner reached State Pension age?",
    10: "Have both you and your partner reached State Pension age?",
    11: "Are you currently getting Pension Credit?",
    12: "Are you in full-time education or training?",
    13: "Do you live with a partner who is eligible for Universal Credit?",
    14: "Are you responsible for a child (either as a single person or as a couple)?",
    15: "Have you reached State Pension age and live with a partner who is below State Pension age?",
    16: "Have you received a Migration Notice letter telling you to move to Universal Credit?",
    17: "Are you 21 or under, studying any qualification up to A level or equivalent, and do not have parental support?",
    18: "Are you studying part-time?",
    19: "Is your course one for which no student loan or finance is available?",
    20: "Do you have a disability or health condition?",
    21: "Were you assessed as having limited capability for work by a Work Capability Assessment before starting your course?",
    22: "Are you entitled to Personal Independence Payment (PIP), Disability Living Allowance (DLA), Attendance Allowance, Armed Forces Independence Payment, Adult Disability Payment (ADP) in Scotland, Child Disability Payment (CDP) in Scotland, Pension Age Disability Payment (PADP) in Scotland, or Scottish Adult Disability Living Allowance (SADLA) in Scotland?",
    23: "Do you have a health condition or disability with medical evidence for it, such as a fit note?",
    24: "Are you caring for someone who gets a health or disability-related benefit?",
    25: "Has a medical professional said you are nearing the end of life?",
    26: "Are you pregnant and expecting your baby in the next 11 weeks?",
    27: "Have you had a baby in the last 15 weeks?",
    28: "Do you have parental support (for example, do you live with your parents or are you under local authority care)?",
    29: "Are you in the armed forces and stationed abroad?"
}

def get_next_question_for_universal_credit_eligibility_check(next_question: int) -> Question:
    if QUESTIONS.get(next_question) is None:
        raise ValueError(f"Question index {next_question} not recognised")
    
    question = Question.new(QUESTIONS[next_question])
    
    match next_question:
        case 1:
            return question \
                .add_answer_and_outcome("Yes", NextQuestion.new(2)) \
                .add_answer_and_outcome("No", Decision.new(False, "You must live in the UK to be eligible for Universal Credit."))
        
        case 2:
            return question \
                .add_answer_and_outcome("Yes", NextQuestion.new(23)) \
                .add_answer_and_outcome("No", NextQuestion.new(3))
        
        case 3:
            return question \
                .add_answer_and_outcome("Yes", NextQuestion.new(4)) \
                .add_answer_and_outcome("No", Decision.new(False, "You must be aged 18 or over but under State Pension age to be eligible for Universal Credit (unless you're 16-17 and meet specific criteria).")) \
                .add_to_glossary("State Pension age", "The age at which you can start claiming your State Pension. This varies depending on when you were born.")
        
        case 4:
            return question \
                .add_answer_and_outcome("Yes", NextQuestion.new(5)) \
                .add_answer_and_outcome("No", Decision.new(False, "You must have £16,000 or less in money, savings and investments to be eligible for Universal Credit."))
        
        case 5:
            return question \
                .add_answer_and_outcome("Yes", NextQuestion.new(6)) \
                .add_answer_and_outcome("No", NextQuestion.new(7)) \
                .add_to_glossary("EU", "European Union - a political and economic union of member states located primarily in Europe.") \
                .add_to_glossary("EEA", "European Economic Area - includes EU countries and also Iceland, Liechtenstein and Norway.")
        
        case 6:
            return question \
                .add_answer_and_outcome("Yes", NextQuestion.new(7)) \
                .add_answer_and_outcome("No", Decision.new(False, "As an EU, EEA or Swiss citizen, you and your family might need settled or pre-settled status under the EU Settlement Scheme to get Universal Credit.")) \
                .add_to_glossary("EU Settlement Scheme", "A scheme that allows EU, EEA and Swiss citizens and their family members to continue living in the UK after Brexit. It grants either settled or pre-settled status.")
        
        case 7:
            return question \
                .add_answer_and_outcome("Yes", NextQuestion.new(9)) \
                .add_answer_and_outcome("No", NextQuestion.new(12))
        
        case 8:
            return question \
                .add_answer_and_outcome("Yes", Decision.new(True, "You are eligible for Universal Credit. You and your partner will need to make a joint claim for your household. How much you can get will depend on your partner's income and savings, as well as your own.")) \
                .add_answer_and_outcome("No", Decision.new(True, "You are eligible for Universal Credit. You and your partner will need to make a joint claim for your household, even if your partner is not eligible. How much you can get will depend on your partner's income and savings, as well as your own."))
        
        case 9:
            return question \
                .add_answer_and_outcome("Yes", NextQuestion.new(10)) \
                .add_answer_and_outcome("No", NextQuestion.new(8))
        
        case 10:
            return question \
                .add_answer_and_outcome("Yes", Decision.new(False, "Your Universal Credit claim will stop when you both reach State Pension age. You should explore Pension Credit instead.")) \
                .add_answer_and_outcome("No", NextQuestion.new(11))
        
        case 11:
            return question \
                .add_answer_and_outcome("Yes", Decision.new(True, "You can still claim Universal Credit as a couple, but your Pension Credit will stop if you or your partner make a claim for Universal Credit. You'll usually be better off staying on Pension Credit. You should check using a benefits calculator before proceeding.")) \
                .add_answer_and_outcome("No", NextQuestion.new(8)) \
                .add_to_glossary("Pension Credit", "A means-tested benefit for people over State Pension age who are on a low income. It tops up your weekly income to a guaranteed minimum level.")
        
        case 12:
            return question \
                .add_answer_and_outcome("Yes", NextQuestion.new(13)) \
                .add_answer_and_outcome("No", NextQuestion.new(20))
        
        case 13:
            return question \
                .add_answer_and_outcome("Yes", Decision.new(True, "You can claim Universal Credit while in full-time education because you live with a partner who is eligible for Universal Credit.")) \
                .add_answer_and_outcome("No", NextQuestion.new(14))
        
        case 14:
            return question \
                .add_answer_and_outcome("Yes", Decision.new(True, "You can claim Universal Credit while in full-time education because you are responsible for a child.")) \
                .add_answer_and_outcome("No", NextQuestion.new(15))
        
        case 15:
            return question \
                .add_answer_and_outcome("Yes", Decision.new(True, "You can claim Universal Credit while in full-time education because you have reached State Pension age and live with a partner who is below State Pension age.")) \
                .add_answer_and_outcome("No", NextQuestion.new(16))
        
        case 16:
            return question \
                .add_answer_and_outcome("Yes", Decision.new(True, "You can claim Universal Credit while in full-time education because you have received a Migration Notice letter telling you to move to Universal Credit.")) \
                .add_answer_and_outcome("No", NextQuestion.new(17)) \
                .add_to_glossary("Migration Notice letter", "A letter sent to people on certain legacy benefits telling them to move to Universal Credit by a specific date.")
        
        case 17:
            return question \
                .add_answer_and_outcome("Yes", Decision.new(True, "You can claim Universal Credit because you are 21 or under, studying any qualification up to A level or equivalent, and do not have parental support.")) \
                .add_answer_and_outcome("No", NextQuestion.new(18))
        
        case 18:
            return question \
                .add_answer_and_outcome("Yes", Decision.new(True, "You may be able to claim Universal Credit while studying part-time.")) \
                .add_answer_and_outcome("No", NextQuestion.new(19))
        
        case 19:
            return question \
                .add_answer_and_outcome("Yes", Decision.new(True, "You may be able to claim Universal Credit because your course is one for which no student loan or finance is available.")) \
                .add_answer_and_outcome("No", NextQuestion.new(21))
        
        case 20:
            return question \
                .add_answer_and_outcome("Yes", NextQuestion.new(29)) \
                .add_answer_and_outcome("No", NextQuestion.new(29))
        
        case 21:
            return question \
                .add_answer_and_outcome("Yes", NextQuestion.new(22)) \
                .add_answer_and_outcome("No", Decision.new(False, "You cannot claim Universal Credit while in full-time education unless you meet one of the specific exemptions.")) \
                .add_to_glossary("Work Capability Assessment", "An assessment used to determine whether your health condition or disability limits your ability to work. It decides if you have limited capability for work or limited capability for work-related activity.")
        
        case 22:
            return question \
                .add_answer_and_outcome("Yes", Decision.new(True, "You can claim Universal Credit while in full-time education because you were assessed as having limited capability for work before starting your course and are entitled to a qualifying disability-related benefit.")) \
                .add_answer_and_outcome("No", Decision.new(False, "To claim Universal Credit while in full-time education based on a disability, you must have been assessed as having limited capability for work AND be entitled to one of the qualifying disability-related benefits.")) \
                .add_to_glossary("Personal Independence Payment (PIP)", "A benefit for people aged 16 to State Pension age who have long-term ill-health or disability and need help with daily living activities or mobility.") \
                .add_to_glossary("Disability Living Allowance (DLA)", "A benefit to help with the extra costs of looking after a child under 16 with disabilities. Adults who were getting DLA before April 2013 may still receive it.") \
                .add_to_glossary("Attendance Allowance", "A benefit for people over State Pension age who need help with personal care or supervision because of illness or disability.") \
                .add_to_glossary("Armed Forces Independence Payment", "A tax-free payment for service personnel and veterans who have been seriously injured as a result of military service.") \
                .add_to_glossary("Adult Disability Payment (ADP)", "A Scottish benefit replacing PIP in Scotland for people aged 16 to State Pension age with a disability or long-term health condition.") \
                .add_to_glossary("Child Disability Payment (CDP)", "A Scottish benefit replacing DLA for children in Scotland under 18 with a disability or long-term health condition.") \
                .add_to_glossary("Pension Age Disability Payment (PADP)", "A Scottish benefit replacing Attendance Allowance in Scotland for people over State Pension age.") \
                .add_to_glossary("Scottish Adult Disability Living Allowance (SADLA)", "A transitional disability benefit in Scotland for those previously receiving DLA.")
        
        case 23:
            return question \
                .add_answer_and_outcome("Yes", Decision.new(True, "You can claim Universal Credit at age 16 or 17 because you have a health condition or disability with medical evidence for it.")) \
                .add_answer_and_outcome("No", NextQuestion.new(24)) \
                .add_to_glossary("fit note", "A statement from a doctor or medical professional that provides evidence of your health condition. Previously known as a sick note.")
        
        case 24:
            return question \
                .add_answer_and_outcome("Yes", Decision.new(True, "You can claim Universal Credit at age 16 or 17 because you are caring for someone who gets a health or disability-related benefit.")) \
                .add_answer_and_outcome("No", NextQuestion.new(25))
        
        case 25:
            return question \
                .add_answer_and_outcome("Yes", Decision.new(True, "You can claim Universal Credit at age 16 or 17 because a medical professional has said you are nearing the end of life.")) \
                .add_answer_and_outcome("No", NextQuestion.new(14)) \
                .add_to_glossary("nearing the end of life", "A clinical assessment that someone is likely to die within the next 12 months. This can provide access to fast-tracked benefits and support.")
        
        case 26:
            return question \
                .add_answer_and_outcome("Yes", Decision.new(True, "You can claim Universal Credit at age 16 or 17 because you are pregnant and expecting your baby in the next 11 weeks.")) \
                .add_answer_and_outcome("No", NextQuestion.new(27))
        
        case 27:
            return question \
                .add_answer_and_outcome("Yes", Decision.new(True, "You can claim Universal Credit at age 16 or 17 because you have had a baby in the last 15 weeks.")) \
                .add_answer_and_outcome("No", NextQuestion.new(28))
        
        case 28:
            return question \
                .add_answer_and_outcome("Yes", Decision.new(False, "You cannot claim Universal Credit at age 16 or 17 if you have parental support (for example, if you live with your parents or are under local authority care) and do not meet any of the other specific criteria.")) \
                .add_answer_and_outcome("No", Decision.new(True, "You can claim Universal Credit at age 16 or 17 because you do not have parental support.")) \
                .add_to_glossary("local authority care", "When a child or young person is looked after by their local council, either in foster care, a children's home, or other accommodation provided by the council.")
        
        case 29:
            return question \
                .add_answer_and_outcome("Yes", Decision.new(True, "You are eligible for Universal Credit. As you are in the armed forces and stationed abroad, you will need to use a specific address when you apply.")) \
                .add_answer_and_outcome("No", Decision.new(True, "You are eligible for Universal Credit. You may be able to get extra money if you have a health condition that affects your ability to work."))
        
        case _:
            raise ValueError(f"Question index {next_question} not recognised")
