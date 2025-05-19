import sys
import os

# All commandline arguments that could be parsed for this program




class Arguments:

    def __init__(self):
        args = list()
        if len(sys.argv) > 1:
            # First argument is the script call, so parse from the second argument 
            for a in sys.argv[1:]:
                args.append(a)

        # default all arguments
        self.is_test = False
        self.display_help = False
        self.existing_assignment = ""
        self.unknown_args = list()
        self.parse_failures = list()

        # if no args, just default all arguments
        if len(args) == 0:
            return
        
        # There are args, parse them
        # The reasoning for the while loop is arguments with a specific number of input values
        # In those cases we can immediately parse booleans, paths etc. and increment i to skip it in the next pass
        i = 0
        while i < len(args):

            current_arg = args[i]

            match current_arg:
                case "--test" | "-t":
                    self.is_test = True
                case "--help" | "-h":
                    self.display_help = True
                case "--existing" | "-e":
                    if i + 1 < len(args):
                        i += 1 
                        if os.path.isfile(args[i]):
                            self.existing_assignment = args[i]
                        else:
                            self.parse_failures.append(f"{current_arg} expects a file as input, found argument {args[i]} is not a file")
                    else:
                        self.parse_failures.append(f"{current_arg} expects a path as input. E.G. --existing C:\\path\\to\\file.json")
                case _:
                    self.unknown_args.append(current_arg)

            i += 1
    
    def parse_success(self) -> bool:
        return len(self.unknown_args) == 0 and len(self.parse_failures) == 0
    
    def display_cli_help(self):

        # if help was not requested, but this is called then the user did something wrong
        # So display the unknown args
        if len(self.unknown_args) > 0 or len(self.parse_failures) > 0:
            print("There was an issue parsing the input arguments:")
            for unknown_arg in self.unknown_args:
                print(f"  Unknown Argument: \"{unknown_arg}\"")
            for parse_failure in self.parse_failures:
                print(f"  Parse Failure: {parse_failure}")
        
        print("Usage: py studance_lottery [-h|--help] [-t|--test]")
        print("Command explanation:")
        print("  [-h|--help]: Display this help dialog")
        print("  [-t|--test]: Use test data instead of the input data")
        print("  [-e|--existing <path>]: Use an existing assignment as input to assign extra members")
