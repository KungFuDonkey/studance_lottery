
from cli_args import Arguments
from dance_classes import load_dance_classes, load_existing_assignment, export_assignment
from studancer import load_dancers
from lottery import assign_dancers


def main():
    args = Arguments()

    print("=== STUdance Class Lottery Script ===")
    print()

    # Check if arguments should be displayed in the console
    if not args.parse_success() or args.display_help:
        args.display_cli_help()
        return

    print("---------- Loading dancers ----------")
    dancers = load_dancers(args.is_test)
    print("Finished loading dancers")
    print()

    existing_assignment = dict()
    dance_class_dict = dict()

    print("------- Loading dance classes -------")
    dance_classes = load_dance_classes()

    # Pre initialize assignment list
    for dance_class in dance_classes:
        existing_assignment[dance_class.name] = list()

    # Make a dictionary to faster search properties of dance classes
    for dance_class in dance_classes:
        dance_class_dict[dance_class.name] = dance_class

    print("Finished loading dance classes")
    print()

    if args.existing_assignment != "":
        print("---- Loading existing assignment ----")
        print(args.existing_assignment)
        existing_assignment = load_existing_assignment(args.existing_assignment)
        print("Finished loading assignment")
        print()

    print("------ Assigning dance classes ------")
    class_assignment = assign_dancers(existing_assignment, set(dancers), dance_class_dict)
    print("Finished assigning dance classes")
    print()


    print("------ Exporting dance classes ------")
    export_assignment(class_assignment, args.is_test)
    print("Finished assigning dance classes")
    print()




if __name__ == "__main__":
    main()