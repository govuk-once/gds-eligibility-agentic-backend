from mcp_server.models.eligibility_check_models import Decision, NextQuestion, Question

def get_next_question_for_pip_eligibility_check(next_question: int) -> Question:
    match next_question:
        case 1:
            return Question.new("How old are you?") \
                .add_answer_and_outcome("68+", Decision.new(False, "You usually cannot make a new claim for PIP and should look at 'Attendance Allowance' instead.")) \
                .add_answer_and_outcome("18 to 67", NextQuestion.new(2)) \
                .add_answer_and_outcome("17 or under", Decision.new(False, "Too young, unfortunately!"))
        case 2:
            return Question.new("Do you live in England or Wales?") \
                .add_answer_and_outcome("Yes", NextQuestion.new(3)) \
                .add_answer_and_outcome("No", Decision.new(False, "If you live in Scotland, you can apply for 'Adulut Disability Payment' instead.")
            )
        case 3:
            return Question.new("Have you lived in the UK for at least 2 of the last 3 years?") \
                .add_answer_and_outcome("Yes", NextQuestion.new(4)) \
                .add_answer_and_outcome("No", Decision.new(False))
        case 4:
            return Question.new("Have you had a health condition for at least 3 months, and do you expect it to continue for at least another 9 months. Alternatively, are you not expected to live more than 12 months?") \
                .add_answer_and_outcome("Yes", NextQuestion.new(5)) \
                .add_answer_and_outcome("No", Decision.new(False))
        case 5: 
            return Question.new("""
                Do you need help, or struggle, with any of the following for over half of any given day?
                - Preparing & Eating
                - Hygiene
                - Dressing
                - Managing Health
                - Communication
                - Socializing
                - Finances
                - Planning a Journey
                - Moving Around"
            """) \
            .add_answer_and_outcome("Yes", NextQuestion.new(6)) \
            .add_answer_and_outcome("No", Decision.new(False)) \
            .add_to_glossary("needing help", "Only being able to do a task by using an aid (like a grab rail, a walking stick, or a dossette box for pills) counts.") \
            .add_to_glossary("Preparing & Eating", "cooking a simple meal, cutting up food, or being reminded to eat") \
            .add_to_glossary("Hygiene", "washing, bathing, or using the toilet") \
            .add_to_glossary("Dressing", "putting on or taking off clothes") \
            .add_to_glossary("Managing Health", "managing medication, monitoring a health condition, or using medical equipment") \
            .add_to_glossary("Communication", "speaking to others, hearing/understanding what is being said, or reading basic information") \
            .add_to_glossary("Socializing", "difficulty being around other people, or interacting with them") \
            .add_to_glossary("Finances", "managing money or making decisions about spending") \
            .add_to_glossary("Planning a Journey", "planning or following a route because of a mental health condition, sensory impairment, or learning disability e.g., getting overwhelmed or lost") \
            .add_to_glossary("Moving Around", "physical difficulty walking? e.g., you are only able to walk a short distance (20 or 50 meters), before needing to stop")
            
        case 6: 
            return Question.new("""
                With respect to the tasks discussed, do any of the following apply?
                - Safety
                - Time
                - Frequency
                - Standard
            """) \
            .add_answer_and_outcome("Yes", Decision.new(True)) \
            .add_answer_and_outcome("No", Decision.new(False)) \
            .add_to_glossary("Safety", "you can't do the task without putting yourself or others at risk") \
            .add_to_glossary("Time", "it takes you much longer (more than twice as long) than it would take a person without your condition") \
            .add_to_glossary("Frequency", "you can't do it as often as you need to throughout the day") \
            .add_to_glossary("Standard", "you can't do it to an acceptable standard")
        case _:
            raise ValueError("Next question index not recognised")