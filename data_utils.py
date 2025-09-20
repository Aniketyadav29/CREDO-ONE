
import random
from Config import loan_data

def get_random_applicant():
    """
    Selects a random applicant's data from the loan_data list.
    """
    return random.choice(loan_data)
