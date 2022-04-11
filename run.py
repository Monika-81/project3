import gspread
from google.oauth2.service_account import Credentials
from prettytable import PrettyTable

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('buy_me')


def view_shopping_list():
    """
    Lets the user choose if they what to see both shopping
    lists as one or one of the separate list, either standard list or
    the list for extra supplies. A complete list contains values
    from both lists but only one heading.
    """

    while True:
        print(' -------------------------------------------------------')
        print('|       Welcome to your personal shopping list!         |')
        print(' -------------------------------------------------------')
        print('Would you like to view the complete shopping list?')
        print('Or one of your editable shopping lists?\n')
        print('Choose between:')
        print('Complete list (c) - a merger of the two lists below.')
        print('Standard list (s) - the regular groceries you stock up.')
        print('Extra list (e) - a list of additional supplies.\n')
        list_choice = input('Please choose a list: \n').lower()
        global shop_list

        if list_choice == 's':
            print('You chose the STANDARD shopping list.\n')
            shop_list = SHEET.worksheet('standard').get_values()
            list_prettytable(shop_list)
            return shop_list

        elif list_choice == 'e':
            print('You chose the EXTRA shopping list.\n')
            shop_list = SHEET.worksheet('extra').get_values()
            list_prettytable(shop_list)
            return shop_list

        elif list_choice == 'c':
            print('\nYou chose the COMPLETE shopping list.')
            print('This list is view only.\n')
            print('Choose another list if you would like to edit the list.\n')
            standard_list = SHEET.worksheet('standard').get_values()
            extra_list = SHEET.worksheet('extra').get_values()
         
            headings = [standard_list[0]]
            standard_list_values = standard_list[1:]
            extra_list_values = extra_list[1:]

            # sort list on location
            sort_list = standard_list_values + extra_list_values
            sorted_list = sorted(sort_list, key=lambda x: x[4])
            shop_list = headings + sorted_list
            list_prettytable(shop_list)

            print('Would you like to sort on items that needs to be bought?')
            sort_on_buy(sort_list, headings)
        else:
            print('Incorrect list choice, type "c", "e" or "s".')
            print('Please try again!\n')


def list_prettytable(shop_list):
    """
    Formats the list using PrettyTable, to make the
    lists easy to read and more visual appealing.
    """
    pt_ = PrettyTable()
    pt_.field_names = shop_list[0]
    for i in range(len(shop_list)-1):
        pt_.add_row(shop_list[i+1])
    print(pt_)


def sort_on_buy(sort_list, headings):
    """
    Gives the user the option to sort the list regarding
    if the item needs to be bought or not. Also gives the
    user the option to go back to main menu or quit.
    """
    while True:
        sort = input('Y/N?:\n').lower()
        if sort == 'y':
            sorted_list = sorted(sort_list, key=lambda x: x[2], reverse=True)
            shop_list = headings + sorted_list
            list_prettytable(shop_list)
            break
        elif sort == 'n':
            break
        else:
            print('Wrong input, try again.\n')

    print('Press M (m) to go back to the main menu')
    back = input('or any key to quit: \n').lower()
    if back == 'm':
        main()
    else:
        quit()


def edit_list():
    """
    Lets the user choose if they like to edit the list.
    """
    print('\nWould you like to edit this list?\n')
    edit = input('Y/N?:\n').lower()
    if edit == 'y':
        return
    elif edit == 'n':
        print('Going back to the main menu.\n')
        main()
    else:
        print('Wrong input, please try again.\n')
        edit_list()
        return


def edit_menu(shopping_list):
    """
    Displays an actions menu to let the user choose how to edit the list.
    """
    print('\nChoose an edit action:\n')
    print('     1. Check item')
    print('     2. Change quantity')
    print('     3. Change location')
    print('     4. Add an item')
    print('     5. Delete item')
    print('     6. Back to main menu\n')
    edit_action = input('Action number:\n')

    if validate_action(edit_action):
        print(f'You chose action {edit_action}. Is this correct?')
        validate_option = input('Y/N?\n').lower()
        if validate_option == 'y':
            edit_action_event(edit_action, shopping_list)
        elif validate_option == 'n':
            print()
            print('Please make new choice of action.\n')
            edit_menu(shopping_list)
        else:
            print()
            print('Wrong input, please try again.\n')
            edit_menu(shopping_list)
    else:
        edit_menu(shopping_list)


def validate_action(value):
    """
    Validates item index of chosen item as an integer.
    Or informs the user to input a number.
    """
    menu_range = range(1, 7)
    try:
        value = int(value)
        if value in menu_range:
            print()
        elif value > 6:
            print('You need to choose a number between 1 - 6.')
            print('Please try again!\n')
            return False

    except ValueError:
        print('You need to choose a number between 1 - 6. Please try again!\n')
        return False

    return True


def item_to_edit(shopping_list):
    """
    Lets the user choose which item on the list to edit, validates the input.
    """
    while True:
        print('\nChoose the number of the item you like to edit.\n')
        item_index = input('Item number:\n')
        if validate_int(item_index):
            print(f'(\nYou chose item no. {item_index}. Is that correct?')
            validate_item = input('Y/N? Or Q to go back.\n').lower()
            break

    # input validation        
    if validate_item == 'y':
        pass
    elif validate_item == 'n':
        print('Please choose another item number.')
        item_to_edit(shopping_list)
    elif validate_item == 'q':
        edit_menu(shopping_list)
    else:
        print('Wrong input, please try again.\n')
        item_to_edit(shopping_list)
    return item_index


def validate_int(value):
    """
    Validates item index of chosen item as an integer.
    Or informs the user to input a number.
    """
    try:
        value = int(value)
    except ValueError:
        print(f'Invalid data: {value} is not a whole number (no decimals).\n')
        print('Please try again!\n')
        return False
    return True


def edit_action_event(edit_action, shopping_list):
    """
    Identifies the action the user like to proceed with 
    and starts each action seperately.
    """
    if edit_action == '1':
        while True:
            print('\nWould you like to check all items on the list?')
            check_all = input('Y/N?:\n')
            if check_all == 'y':
                check_all_update(shopping_list)
                break
            elif check_all == 'n':
                edit_item = item_to_edit(shopping_list)
                check_item_in_list(edit_item, edit_action, shopping_list)
                break
            else:
                print('Wrong input, try again!')

    elif edit_action == '2':
        edit_item = item_to_edit(shopping_list)
        change_quantity(edit_item, shopping_list)

    elif edit_action == '3':
        edit_item = item_to_edit(shopping_list)
        change_location(edit_item, shopping_list)

    elif edit_action == '4':
        add_item(shopping_list)

    elif edit_action == '5':
        edit_item = item_to_edit(shopping_list)
        delete_item(edit_item, edit_action, shopping_list)

    elif edit_action == '6':
        main()

    else:
        print('Something went wrong, please restart the program.')
        quit()

    return


def check_item_in_list(edit_item, edit_action, shopping_list):
    """
    If the item the user chose to check is in the list,
    the function finds the item and changes the value in
    google sheet to either yes or no (to buy or not to buy).
    Restarts the action if the user likes to check another item.
    """
    index_num = int(edit_item)

    if shopping_list == SHEET.worksheet('standard').get_values():
        standard_sheet = SHEET.worksheet('standard')
        standard = SHEET.worksheet('standard').col_values(1)
        standard_col = SHEET.worksheet('standard').col_values(3)

        if edit_item in standard:
            update_value = standard_col[index_num]

            if update_value == 'yes':
                check_position = int(standard.index(edit_item))
                standard_sheet.update_cell(check_position + 1, 3, 'no')
                print(f'\nItem number {edit_item} has been set to No!\n')
                shop_list = SHEET.worksheet('standard').get_values()
                list_prettytable(shop_list)

                print('Would you like to check another item?')
                if again():
                    shopping_list = SHEET.worksheet('standard').get_values()
                    edit_item = item_to_edit(shopping_list)
                    check_item_in_list(edit_item, edit_action, shopping_list)

            elif update_value == 'no':
                check_position = int(standard.index(edit_item))
                standard_sheet.update_cell(check_position + 1, 3, 'yes')
                print(f'\nItem number {edit_item} has been set to Yes!?\n')
                shop_list = SHEET.worksheet('standard').get_values()
                list_prettytable(shop_list)

                print('Would you like to check another item?')
                if again():
                    shopping_list = SHEET.worksheet('standard').get_values()
                    edit_item = item_to_edit(shopping_list)
                    check_item_in_list(edit_item, edit_action, shopping_list)

        else:
            print('\nItem value not in list, please pick another value.\n')
            main()

    elif shopping_list == SHEET.worksheet('extra').get_values():
        extra_sheet = SHEET.worksheet('extra')
        extra = SHEET.worksheet('extra').col_values(1)
        extra_col = SHEET.worksheet('extra').col_values(3)

        if edit_item in extra:
            update_value = (extra_col[index_num])

            if update_value == 'yes':
                check_position = int(extra.index(edit_item))
                extra_sheet.update_cell(check_position + 1, 3, 'no')
                print(f'\nItem number {edit_item} has been set to No!\n')
                shop_list = SHEET.worksheet('extra').get_values()
                list_prettytable(shop_list)

                print('Would you like to check another item?')
                if again():
                    shopping_list = SHEET.worksheet('extra').get_values()
                    shop_list = SHEET.worksheet('extra').get_values()
                    edit_item = item_to_edit(shopping_list)
                    check_item_in_list(edit_item, edit_action, shopping_list)

            elif update_value == 'no':
                check_position = int(extra.index(edit_item))
                extra_sheet.update_cell(check_position + 1, 3, 'yes')
                print(f'\nItem number {edit_item} has been set to Yes!?\n')
                shop_list = SHEET.worksheet('extra').get_values()
                list_prettytable(shop_list)

                print('Would you like to check another item?')
                if again():
                    shopping_list = SHEET.worksheet('extra').get_values()
                    edit_item = item_to_edit(shopping_list)
                    check_item_in_list(edit_item, edit_action, shopping_list)
        else:
            print('\nItem value not in list, please choose another value.\n')
            main()

    else:
        print('Oops! Something went wrong, please try again!')
        main()


def check_all_update(shopping_list):
    """
    Lets the user check all items in list to either yes or no.
    """
    if shopping_list == SHEET.worksheet('standard').get_values():
        standard = SHEET.worksheet('standard').col_values(1)
        standard_col = SHEET.worksheet('standard').col_values(3)

        print('\nCheck as YES (y) or NO (n)?:\n')
        check_type = input('Y/N?\n').lower()
        if check_type == 'y':
            for i in range(len(standard)):
                i = int(i)
                standard_col[i] = 0 + 1
                SHEET.worksheet('standard').update_cell(i + 1, 3, "yes")

            SHEET.worksheet('standard').update_cell(1, 3, 'Buy-Me')
            shop_list = SHEET.worksheet('standard').get_values()
            list_prettytable(shop_list)
            print('All items checked as Yes, going back to main menu.')

        elif check_type == 'n':
            for i in range(len(standard)):
                i = int(i)
                standard_col[i] = 0 + 1
                SHEET.worksheet('standard').update_cell(i + 1, 3, "no")

            SHEET.worksheet('standard').update_cell(1, 3, 'Buy-Me')
            shop_list = SHEET.worksheet('standard').get_values()
            list_prettytable(shop_list)
            print('All items checked as No, going back to main menu.')
        else:
            print('Wrong input, try again!')
            check_all_update(shopping_list)

    elif shopping_list == SHEET.worksheet('extra').get_values():
        extra = SHEET.worksheet('extra').col_values(1)
        extra_col = SHEET.worksheet('extra').col_values(3)

        print('\nCheck as YES (y) or NO (n)?:\n')
        check_type = input('Y/N?\n').lower()
        if check_type == 'y':
            for i in range(len(extra)):
                i = int(i)
                extra_col[i] = 0 + 1
                SHEET.worksheet('extra').update_cell(i + 1, 3, "yes")

            SHEET.worksheet('extra').update_cell(1, 3, 'Buy-Me')
            shop_list = SHEET.worksheet('extra').get_values()
            list_prettytable(shop_list)
            print('All items checked as Yes, going back to main menu.')

        elif check_type == 'n':
            for i in range(len(extra)):
                i = int(i)
                extra_col[i] = 0 + 1
                SHEET.worksheet('extra').update_cell(i + 1, 3, "no")

            SHEET.worksheet('extra').update_cell(1, 3, 'Buy-Me')
            shop_list = SHEET.worksheet('extra').get_values()
            list_prettytable(shop_list)
            print('All items checked as No, going back to main menu.')
        else:
            print('Wrong input, try again!')
            check_all_update(shopping_list)

    else:
        print('Oops! Something went wrong, please try again!')
    main()


def change_quantity(edit_item, shopping_list):
    """
    Ask for user input of quantity and checks for valid input.
    """
    quantity = input('\nInput new quantity value:\n')
    if validate_int(quantity):
        print(f'\nDo you like to update the quantity to {quantity}?')
        validate_item = input('Y/N? Or Q to choose another action.\n').lower()
        if validate_item == 'y':
            update_quantity(edit_item, quantity, shopping_list)
        elif validate_item == 'n':
            print('Please choose a new quantity number.\n')
            change_quantity(edit_item, shopping_list)
        elif validate_item == 'q':
            edit_menu(shopping_list)
            return
        else:
            print('Wrong input, please try again.\n')
            change_quantity(edit_item, shopping_list)
    else:
        print('Please insert a whole numeric number.')
        change_quantity(edit_item, shopping_list)


def update_quantity(edit_item, quantity, shopping_list):
    """
    If the item the user chose to change quantity of an item,
    the function finds the item and changes the value in
    google sheet to either after user input new quantity value.
    Restarts the action if the user likes to edit another item.
    """
    if shopping_list == SHEET.worksheet('standard').get_values():
        standard = SHEET.worksheet('standard').col_values(1)

        if edit_item in standard:
            position = int(standard.index(edit_item))
            SHEET.worksheet('standard').update_cell(position + 1, 4, quantity)
            print(f'The quantatity has been set to {quantity}.\n')
            shop_list = SHEET.worksheet('standard').get_values()
            list_prettytable(shop_list)

            print('Would you like to change quantity on another item?')
            if again():
                shopping_list = SHEET.worksheet('standard').get_values()
                edit_item = item_to_edit(shopping_list)
                change_quantity(edit_item, shopping_list)

        else:
            print('\nItem value not in list, please pick another value.\n')
            item_to_edit(shopping_list)

    elif shopping_list == SHEET.worksheet('extra').get_values():
        extra = SHEET.worksheet('extra').col_values(1)

        if edit_item in extra:
            position = int(extra.index(edit_item))
            SHEET.worksheet('extra').update_cell(position + 1, 4, quantity)
            print(f'The quantatity has been set to {quantity}.\n')
            shop_list = SHEET.worksheet('extra').get_values()
            list_prettytable(shop_list)

            print('Would you like to change quantity on another item?')
            if again():
                shopping_list = SHEET.worksheet('extra').get_values()
                edit_item = item_to_edit(shopping_list)
                change_quantity(edit_item, shopping_list)
        else:
            print('\nItem value not in list, please pick another value.\n')
            item_to_edit(shopping_list)

    else:
        print('Oops! Something went wrong, please try again!')
        main()


def change_location(edit_item, shopping_list):
    """
    Ask for user input new location and checks for valid input.
    """
    while True:
        print('\nLocation in store (examples): "Bakery", "Beverages", "Bulk",')
        print(' "Dairy", "Deli", "Floral", "Household", "Meat",')
        print(' "Personal", "Snacks", "Vegetables" \n')
        location = input('Input new location: \n').capitalize()

        if location.isalpha():  # input validation
            break
        else:
            print('Input needs to be alphabetic. Try again.\n')

    print(f'\nDo you like to update the location to {location}?')
    validate = input('Y/N? Or Q to choose another action.\n').lower()
    if validate == 'y':
        update_location(edit_item, location, shopping_list)
    elif validate == 'n':
        print('Please choose another location.\n')
        change_location(edit_item, shopping_list)
    elif validate == 'q':
        edit_menu(shopping_list)
        return
    else:
        print('Please use alphabetic figures and no spaces.')
        change_location(edit_item, shopping_list)


def update_location(edit_item, location, shopping_list):
    """
    If the item the user chose to change location of an item,
    the function finds the item and changes the value in
    google sheet to either after user input new location value.
    Restarts the action if the user likes to edit another item.
    """
    if shopping_list == SHEET.worksheet('standard').get_values():
        standard = SHEET.worksheet('standard').col_values(1)

        if edit_item in standard:

            position = int(standard.index(edit_item))
            SHEET.worksheet('standard').update_cell(position + 1, 5, location)
            print(f'\nThe new location has been set to {location}.\n')
            shop_list = SHEET.worksheet('standard').get_values()
            list_prettytable(shop_list)

            print('Would you like to change the location of another item?')
            if again():
                shopping_list = SHEET.worksheet('standard').get_values()
                edit_item = item_to_edit(shopping_list)
                change_location(edit_item, shopping_list)
        else:
            print('\nItem value not in list, please pick another value.\n')
            item_to_edit(shopping_list)

    elif shopping_list == SHEET.worksheet('extra').get_values():
        extra = SHEET.worksheet('extra').col_values(1)

        if edit_item in extra:

            position = int(extra.index(edit_item))
            SHEET.worksheet('extra').update_cell(position + 1, 5, location)
            print(f'The location has been set to {location}.\n')
            shop_list = SHEET.worksheet('extra').get_values()
            list_prettytable(shop_list)

            print('Would you like to change the location of another item?')
            if again():
                shopping_list = SHEET.worksheet('extra').get_values()
                edit_item = item_to_edit(shopping_list)
                change_location(edit_item, shopping_list)
        else:
            print('\nItem value not in list, please pick another value.\n')
            item_to_edit(shopping_list)

    else:
        print('Oops! Something went wrong, please try again!')
        main()


def add_item(shopping_list):
    """
    Asks the user what values they like to pass to the new item.
    Validates the values and asks the user to verify that they want
    to add input values as a new row on chosen list.
    """
    while True:
        print('\nYou wish to add an item to the list.\n')
        item = input('Name of item:\n').capitalize()

        if item.isalpha():  # input validation
            break
        else:
            print('Input needs to be alphabetic. Try again.\n')

    while True:
        quantity = input('Quantity: \n')

        try:  # input validation
            quantity = int(quantity)
            if quantity in range(1, 100):
                break
            else:
                print('Max quantity is 100. Please try again.\n')

        except ValueError:
            print(f'{quantity} is not a whole number (no decimals).')
            print('Please try again!\n')

    while True:
        print('\nLocation in store (examples): "Bakery", "Beverages", "Bulk",')
        print(' "Dairy", "Deli", "Floral", "Household", "Meat",')
        print(' "Personal", "Snacks", "Vegetables" \n')
        location = input('Location in store: \n').capitalize()

        if location.isalpha():  # input validation
            break
        else:
            print('Input needs to be alphabetic. Try again.\n')

    print(f'\nDo you wish to add {item}, qty of {quantity} at {location}?')
    
    # Adds the new row
    add_acceptance = input('Y/N? Or Q to choose another action:\n')
    if add_acceptance == 'y':
        if shopping_list == SHEET.worksheet('standard').get_values():
            standard = SHEET.worksheet('standard').col_values(1)

            new_index = (int(standard[-1]) + 1)
            add_row = [new_index] + [item] + ['yes'] + [quantity] + [location]
            SHEET.worksheet('standard').append_row(add_row)
            print('\nNew item added to list.\n')
            shop_list = SHEET.worksheet('standard').get_values()
            list_prettytable(shop_list)

            print('Would you like to add another item?')
            if again():
                shopping_list = SHEET.worksheet('standard').get_values()
                add_item(shopping_list)

        elif shopping_list == SHEET.worksheet('extra').get_values():
            extra = SHEET.worksheet('extra').col_values(1)

            new_index = (int(extra[-1]) + 1)
            add_row = [new_index] + [item] + ['yes'] + [quantity] + [location]
            SHEET.worksheet('extra').append_row(add_row)
            print('\nNew item added to list.\n')
            shop_list = SHEET.worksheet('extra').get_values()
            list_prettytable(shop_list)

            print('Would you like to add another item?')
            if again():
                shopping_list = SHEET.worksheet('extra').get_values()
                add_item(shopping_list)

        else:
            print('Oops! Something went wrong, please try again!')
        return

    elif add_acceptance == 'n':
        print('Going back to add new item...\n')
        add_item(shopping_list)

    elif add_acceptance == 'q':
        edit_menu(shopping_list)

    else:
        print('Wrong input, please try again.\n')
        add_item(shopping_list)
    return


def delete_item(edit_item, edit_action, shopping_list):
    """
    Deletes the item the user chooses from the current list.
    """
    while True:
        if shopping_list == SHEET.worksheet('standard').get_values():
            standard = SHEET.worksheet('standard').col_values(1)
            index_num = int(edit_item)

            if edit_item in standard:
                delete_row = (shopping_list[index_num])
                print(f'\nAre you sure you want to delete row {delete_row}')
                verify_delete = input('Y/N?:\n')

                if verify_delete == 'y':
                    SHEET.worksheet('standard').delete_rows((index_num) + 1)

                    # Updates item index to correct index number
                    standard = SHEET.worksheet('standard').col_values(1)
                    for i in range(len(standard)):
                        i = int(i)
                        standard[i] = 0 + 1
                        SHEET.worksheet('standard').update_cell(i + 1, 1, i)

                    SHEET.worksheet('standard').update_cell(1, 1, 'Index')
                    print('Row deleted\n')
                    shop_list = SHEET.worksheet('standard').get_values()
                    list_prettytable(shop_list)

                    print('Would you like to delete another item?')
                    if again():
                        shopping_list = SHEET.worksheet('standard').get_values()
                        edit_item = item_to_edit(shopping_list)
                        edit_action_event(edit_action, shopping_list)

                elif verify_delete == 'n':
                    print('\nItem not deleted. Please choice a new action.\n')
                    main()
                    break

                else:
                    print('Please try again. Choose yes (y) or no (n).')
                    return False

        elif shopping_list == SHEET.worksheet('extra').get_values():
            extra = SHEET.worksheet('extra').col_values(1)
            index_num = int(edit_item)

            if edit_item in extra:
                delete_row = (shopping_list[index_num])
                print(f'\nAre you sure you want to delete row {delete_row}')
                verify_delete = input('Y/N?:\n')

                if verify_delete == 'y':
                    SHEET.worksheet('extra').delete_rows((index_num) + 1)

                    # Updates item index to correct index number
                    extra = SHEET.worksheet('extra').col_values(1)
                    for i in range(len(extra)):
                        i = int(i)
                        extra[i] = 0 + 1
                        SHEET.worksheet('extra').update_cell(i + 1, 1, i)

                    SHEET.worksheet('extra').update_cell(1, 1, 'Index')
                    print('Row deleted\n')
                    shop_list = SHEET.worksheet('extra').get_values()
                    list_prettytable(shop_list)

                    print('Would you like to delete another item?')
                    if again():
                        shopping_list = SHEET.worksheet('extra').get_values()
                        edit_item = item_to_edit(shopping_list)
                        edit_action_event(edit_action, shopping_list)

                elif verify_delete == 'n':
                    print('\nItem not deleted. Please choice a new action.\n')
                    main()
                    break

                else:
                    print('Please try again. Choose yes (y) or no (n).')
                    return False
        else:
            print('Oops! Something went wrong, please try again!')
            main()
    return


def again():
    """
    Ask the user if they like to redo the last action.
    """
    action_again = input('Y/N?\n')
    if action_again == 'y':
        return True
    elif action_again == 'n':
        print('Going back to main menu.\n')
        main()
    else:
        print('Invalid input')
        main()


def main():
    """
    Run all program functions.
    """
    shopping_list = view_shopping_list()
    edit_list()
    edit_menu(shopping_list)


main()
