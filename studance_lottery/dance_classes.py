import os
from studancer import Studancer

class DanceClass:

    def __init__(
        self,
        name : str,         # Name of this dance class
        max_dancers : int   # The maximum number of dancers that can be in this dance class
    ):
        self.name = name
        self.max_dancers = max_dancers

def load_dance_classes() -> list[DanceClass]:

    # Find path in the current work directory
    file_path = os.path.join(os.getcwd(), "dance_classes.txt")

    # If the file does not exist, create one and notify the user of the correct location
    if not os.path.exists(file_path):

        print("Error: did not find the dance_classes.txt file")
        print(f"       A dance_classes file will be created at the correct location: {file_path}")

        f = open(file_path, "w")

        # Apparently spacing in multiline python strings works like this, its ugly, but gets the job done
        f.write(
            """
# Write out the different classes like <class name> <max people in class> 
# E.G. Mixles 30
# So A class named Mixles with a maximum of 30 people

Modern 1 30
Modern 2 30
Modern 3 30

Street 1 30
Street 2 30
Street 3 30

Mixles 30

Klassiek 30

Hiphop 1 30
Hiphop 2 30
Hiphop 3 30

Jazz 1 30
Jazz 2 30
Jazz 3 30

Feminine jazz/modern 30
Feminine hiphop 30

            """
        )
        f.close()
        # Yeah, we could continue with the newly produced file, but I do not want to give a board member
        # A false sense of hope that the program ran correctly 
        exit(-1)
    
    f = open(file_path, "r")

    classes = list()

    for line in f.readlines():
        # I don't want to deal with spacing and capital letter mismatches
        sanitized_line = line.lower().strip()

        # Can't really have empty classes or comments
        if sanitized_line != "" and not sanitized_line.startswith("#"):

            sections = sanitized_line.split(' ')

            name = ' '.join(sections[:-1]).strip()
            max_dancers = int(sections[-1])

            classes.append(DanceClass(name, max_dancers))

    f.close()

    print (f"Loaded {len(classes)} dance classes")
    
    return classes


def load_existing_assignment(assignment_path) -> dict[str, list[Studancer]]:
    pass

def export_assignment(assignment: dict[str, list[Studancer]], export_to_terminal : bool):

    if export_to_terminal:
        for class_name, students in assignment.items():
            capitalized_class_name = class_name[0].upper() + class_name[1:]
            print(f"{capitalized_class_name}: {str(students)}")
        
        return