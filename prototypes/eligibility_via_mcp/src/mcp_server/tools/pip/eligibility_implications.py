from mcp_server.models.eligibility_check_models import Implications

# NOTE: this could be implented instead by each of the implcated benefits creating their own tool, and taking
#       "pip" as input. The choice on whether to do this is more how the org wants to handle this. Arguably though,
#       implementing eligiblity implications in this way means there is reduced latency in finding an answer.
def check_pip_eligibility_implications() -> Implications:
    return Implications() \
        .add("Benefit Cap", "If you or your partner receive PIP, your household is completely exempt from the benefit cap (the limit on the total amount of benefits you can get)") \
        .add("Universal Credit", "While PIP doesn't automatically increase your UC standard allowance, it can unlock extra help. For example, if you claim for a disabled child who gets PIP, you can get the 'disabled child' addition.") \
        .add("Legacy Benefits", "If you are still on older benefits like Housing Benefit, Income Support, or Working Tax Credit, getting PIP can entitle you to extra 'disability premiums' which increase your overall payments.") \
        .add("Carer’s Allowance", "If you are awarded the daily living component of PIP, someone who cares for you for at least 35 hours a week may become eligible to claim Carer’s Allowance or the Carer Element of Universal Credit") \
        .add("Housing and Council Tax", "Receiving PIP often makes you eligible for a reduction in your local Council Tax bill. You have to apply for this directly through your local council.") \
        .add("Blue Badge", "You may automatically qualify for a Blue Badge for easier parking.") \
        .add("Vehicle Tax", "You can get a 50% discount on your road tax if you get the standard mobility rate, or a 100% exemption if you get the enhanced mobility rate.") \
        .add("Motability Scheme", "If you receive the enhanced mobility rate, you can use it to lease a new car, wheelchair-accessible vehicle, or mobility scooter through the Motability Scheme.") \
        .add("Public Transport", "You become eligible for a Disabled Persons Railcard (1/3 off train fares) and a free or discounted local bus pass.")