import sys
from src.apartments import apartment

def get_commands_and_arguments(text):
    arguments = []
    splited_text = text.split(' ')
    command_name = splited_text[0]

    if command_name != 'BILL':
        arguments = splited_text[1:]

    return command_name, arguments


def main():
    input_file = sys.argv[1]

    with open(input_file) as fp:
        Lines = fp.readlines()

        for line in Lines:
            command_name, arguments = get_commands_and_arguments(line)

            if command_name == 'ALLOT_WATER':
                apartment_object = apartment(int(arguments[0]), arguments[1])
            elif command_name == 'ADD_GUESTS':
                apartment_object.add_guests(int(arguments[0]))
            else:
                apartment_object.calculate_billings()

    total_water_consumption = apartment_object.total_water_consumption
    bill = apartment_object.total_bill
    print(total_water_consumption, bill)


if __name__ == "__main__":
    main()
