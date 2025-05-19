import random

# Describes a single person, and all attributes required for the lottery of assigning the person
# within a dance group in Studance
class Studancer:

    def __init__(
        self,
        name : str,                                # Name of the person requesting membership
        is_board : bool,                           # Whether this person is within the board of studance
        is_damn : bool,                            # Whether this person is a DAMN member
        is_student : bool,                         # Whether this person is following a study
        has_a_gap_year : bool,                     # Whether this person currently has a gap year
        is_new_member : bool,                      # Whether this person is new to studance
        is_non_female : bool,                      # Whether this person has a non female gender
        was_non_dancing_member_last_year : bool,   # Whether this person had a non-dancing membership last year
        was_unrolled_last_year : bool,             # Whether this person requested a membership last year, but was unrolled
        half_year_membership : bool,               # Whether the requested membership is a half year membership
        advised_classes : list[str],               # The advised classes of the member from their teacher last year
        chosen_classes : list[str],                # A list of classes the member wants to join, ordered by priority
        index          : int                       # Index of dancer, as a key to differentiate similar names and data
    ):
        self.name = name 
        self.is_board = is_board
        self.is_damn = is_damn
        self.is_student = is_student
        self.has_a_gap_year = has_a_gap_year
        self.is_new_member = is_new_member
        self.is_non_female = is_non_female
        self.was_non_dancing_member_last_year = was_non_dancing_member_last_year
        self.was_unrolled_last_year = was_unrolled_last_year
        self.half_year_membership = half_year_membership
        self.advised_classes = [x.lower().strip() for x in advised_classes] # sanitize data
        self.chosen_classes = [x.lower().strip() for x in chosen_classes]   # sanitize data
        self.dancer_index = index
        self.max_assignments = 2 if is_board else 1                         # number of classes this person can be assigned to
        self.num_assignments = 0                                            # number of classes this dancer was assigned to
    

    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.name

def _load_from_input_file() -> list[Studancer]:
    return []

def _test_data() -> list[Studancer]:
    print("NOTE: loading test data")
    return [
        Studancer(
            name = "Robin", 
            is_board=True,
            is_damn=True,
            is_student=True,
            has_a_gap_year=False,
            is_new_member=False,
            is_non_female=True,
            was_non_dancing_member_last_year=False,
            was_unrolled_last_year=False,
            half_year_membership=False,
            advised_classes=["Modern 3", "Klassiek"],
            chosen_classes=["Modern 3", "Klassiek", "HipHop 3"],
            index=0
        ),
        Studancer(
            name = "Lisa", 
            is_board=True,
            is_damn=True,
            is_student=True,
            has_a_gap_year=False,
            is_new_member=False,
            is_non_female=True,
            was_non_dancing_member_last_year=False,
            was_unrolled_last_year=False,
            half_year_membership=False,
            advised_classes=["modern 3", "hiphop 3"],
            chosen_classes=["HipHop 3", "Street 3", "HipHop 1"],
            index=1
        ),
        Studancer(
            name = "Milou", 
            is_board=False,
            is_damn=True,
            is_student=False,
            has_a_gap_year=False,
            is_new_member=False,
            is_non_female=True,
            was_non_dancing_member_last_year=False,
            was_unrolled_last_year=False,
            half_year_membership=False,
            advised_classes=["street 2"],
            chosen_classes=["Klassiek", "Modern 3", "Modern 2"],
            index=2
        ),
        Studancer(
            name = "Sietze", 
            is_board=False,
            is_damn=False,
            is_student=False,
            has_a_gap_year=False,
            is_new_member=False,
            is_non_female=True,
            was_non_dancing_member_last_year=False,
            was_unrolled_last_year=False,
            half_year_membership=False,
            advised_classes=["street 2"],
            chosen_classes=["street 2", "street 3", "HipHop 2"],
            index=3
        ),
    ]

def load_dancers(is_test : bool) -> list[Studancer]:
    data = None
    if is_test:
        data = _test_data()
    else:
        data = _load_from_input_file()
    
    print (f"Loaded {len(data)} dancers")
    return data

