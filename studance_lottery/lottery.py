from studancer import Studancer
from dance_classes import DanceClass
import random

# Struct for easier passing of lottery variables
class LotteryArgs:
    def __init__(
        self,
        assignment : dict[str, list[Studancer]],
        dance_classes : dict[str, DanceClass],
        dancers : set[Studancer]
    ):
        self.assignment = assignment
        self.dance_classes = dance_classes
        self.dancers = dancers

# Tries to assign the current preference of a dancer to a specific dance class
def _try_assign_dancer_to_preference(
    dancer : Studancer, 
    preference_pass : int, 
    args : LotteryArgs,
    unassigned_dancers : set[Studancer],
    assigned_dancers : set[Studancer]):

    # Get limits of the chosen dance class
    chosen_class = dancer.chosen_classes[preference_pass]
    num_dancers_in_class = len(args.assignment[chosen_class])
    max_dancers_in_class = args.dance_classes[chosen_class].max_dancers

    if num_dancers_in_class < max_dancers_in_class:
        # This dancer did not exceed the limit, so assign this dancer to their chosen dance class
        # So add them to the assignment
        args.assignment[chosen_class].append(dancer)

        dancer.num_assignments += 1
        # check if dancer is fully assigned, if so put them on the assigned set
        if dancer.num_assignments >= dancer.max_assignments:
            assigned_dancers.add(dancer)
            unassigned_dancers.remove(dancer)

# Tries to assign all dancers to their preferences
def _try_assign_dancers_to_preferences(
    dancers_to_assign : list[Studancer],
    preference_pass : int, 
    args : LotteryArgs,
    unassigned_dancers : set[Studancer],
    assigned_dancers : set[Studancer]
):
    # try and assign all dancers in group
    for dancer in dancers_to_assign:
        _try_assign_dancer_to_preference(
            dancer,
            preference_pass,
            args,
            unassigned_dancers,
            assigned_dancers
        )

# Assigns a priority group given by a priority function
def _assign_priority_group(
    priority_function,
    args : LotteryArgs
):
    # The question right now is what would be the order:
    # 1. We first assign everyone their first preference for every group, then second for every group, etc.
    #    This practically places the last group first preference in front of the first group second preference
    # 2. We assign first preference within the group, then second preference within the group then third etc.
    #    This places teh first preference of anyone above the second preference of anyone
    # 3. We shuffle all participants within the group, then assign the best preference per person
    #    In this case the shuffle determines who has a higher chance of being elected
    #    This has an issue when following the advice of the teacher, as that being the second choice suddenly 
    #    should be at a higher priority than someone who is not following the advice

    # For now assign every priority group, within each choice list first pick the choices that align with 
    # Teachers suggestions

    # In the future, Studance might allow more than 3 (or variable) suggestions, so just check whether we reached the
    # End of all lists for now

    # initially we start with the top preferences with everyone unassigned
    unassigned_dancers = set([x for x in args.dancers if priority_function(x)])
    preference_pass = 0
    assigned_dancers = set()

    # Continue until everyone is assigned, or we reach the end of the preference list
    while len(unassigned_dancers) > 0:

        # Find the people that are following the advice of their teachers
        dancers_with_preferences = [x for x in unassigned_dancers if preference_pass < len(x.chosen_classes)]

        # Stop if we reached the end of all preference lists
        if len(dancers_with_preferences) <= 0:
            break

        # Split dancers up into following advice, and not following advice
        dancers_following_advice = [x for x in dancers_with_preferences if x.chosen_classes[preference_pass] in x.advised_classes]
        dancers_not_following_advice = [x for x in dancers_with_preferences if x.chosen_classes[preference_pass] not in x.advised_classes]

        # Shuffle the dancers to determine order
        random.shuffle(dancers_following_advice)
        random.shuffle(dancers_not_following_advice)

        # First handle the dancers following the advise
        _try_assign_dancers_to_preferences(
            dancers_following_advice,
            preference_pass,
            args,
            unassigned_dancers,
            assigned_dancers
        )

        # Then handle the dancers not following the advise
        _try_assign_dancers_to_preferences(
            dancers_not_following_advice,
            preference_pass,
            args,
            unassigned_dancers,
            assigned_dancers
        )

        # Move to next preference in list
        preference_pass += 1
    
    # Remove assigned dancers from list as those do not require any more processing
    for dancer in assigned_dancers:
        args.dancers.remove(dancer)
    

def assign_dancers(
    existing_assignment : dict[str, list[Studancer]],
    dancers : set[Studancer],
    dance_classes : dict[str, DanceClass]
) -> dict[str, list[Studancer]]:
    
    # Args for most functions in this file
    args = LotteryArgs(
        assignment=existing_assignment,
        dancers=dancers,
        dance_classes=dance_classes
    )

    # Remove previously assigned dancers
    # MUST ensure that dancers in the existing assignment map to dancers in the set
    # Should be ensured in load_existing_assignment()
    for assignment_list in args.assignment.values():
        for dancer in assignment_list:
            dancers.remove(dancer)

    # First group to assign are the board members
    # These are special, as only two of them are allowed in each class
    # That is some complex logic for this special case
    # Therefore, board members should solve this issue by setting the class 
    # they should be in as the first class, until I revisit this and make the decision automatic
    def is_board(x : Studancer):
        return x.is_board
    _assign_priority_group(is_board, args)

    # Second group is the DAMN group, as they need to have a standard dance lesson next to DAMN
    def is_damn(x : Studancer):
        return x.is_damn
    _assign_priority_group(is_damn, args)

    # Third group are existing Student members
    def is_existing_student(x : Studancer):
        return all([
            not x.is_new_member,
            x.is_student,
            not x.has_a_gap_year,
            not x.half_year_membership
        ]) 
    _assign_priority_group(is_existing_student, args)

    # Fourth group are non-dancing students from last year
    def is_non_dancer(x : Studancer):
        return all([
            x.is_student,
            not x.has_a_gap_year,
            x.was_non_dancing_member_last_year,
            not x.half_year_membership
        ])
    _assign_priority_group(is_non_dancer, args)

    # Fifth group are students that were not rolled in last year (must be new?)
    def is_unrolled(x : Studancer):
        return all([
            x.is_student,
            not x.has_a_gap_year,
            x.was_unrolled_last_year,
            not x.half_year_membership
        ])
    _assign_priority_group(is_unrolled, args)

    # Sixth group are new non female students
    def is_non_female(x : Studancer):
        return all([
            x.is_student,
            not x.has_a_gap_year,
            x.is_non_female,
            not x.half_year_membership,
            x.is_new_member
        ])
    _assign_priority_group(is_non_female, args)

    # Seventh group are new female students
    def is_female(x : Studancer):
        return all([
            x.is_student,
            not x.has_a_gap_year,
            not x.is_non_female,
            not x.half_year_membership,
            x.is_new_member
        ])
    _assign_priority_group(is_female, args)

    # Eight group are new half year students
    def is_new_half_year(x : Studancer):
        return all([
            x.is_student,
            not x.has_a_gap_year,
            x.half_year_membership,
            x.is_new_member
        ])
    _assign_priority_group(is_new_half_year, args)

    # Ninth group are gap year students
    def is_gap_year_student(x : Studancer):
        return all([
            x.is_student,
            x.has_a_gap_year,
            not x.half_year_membership,
            x.is_new_member
        ])
    _assign_priority_group(is_gap_year_student, args)

    # Tenth group are half year gap year students
    def is_half_gap_year_student(x : Studancer):
        return all([
            x.is_student,
            x.has_a_gap_year,
            x.half_year_membership,
            x.is_new_member
        ])
    _assign_priority_group(is_half_gap_year_student, args)

    # Eleventh group are non-studying members
    def is_non_studying_member(x : Studancer):
        return all([
            not x.is_student,
            not x.half_year_membership
        ])
    _assign_priority_group(is_non_studying_member, args)

    # Twelfth group are half year non-studying members
    def is_half_non_studying_member(x : Studancer):
        return all([
            not x.is_student,
            x.half_year_membership
        ])
    _assign_priority_group(is_half_non_studying_member, args)

    # Write out remaining unassigned dancers to special list
    if "unassigned" not in args.assignment:
        args.assignment["unassigned"] = list()
    for dancer in args.dancers:
        args.assignment["unassigned"].append(dancer)

    return args.assignment







