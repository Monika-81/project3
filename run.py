import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('buy_me')

def view_shoping_list():
    """
    Lets the user choose if they what to see both shopping
    lists as one or one separate list, either standard list or
    the list for extra supplies. A complete list contains values 
    from both lists but only one heading.
    """
    
    print('Welcome to your personal shopping list!\n')
    print('Would you like to see a complete list?')
    print('Or part of your shopping list?')
    print('Choose between: Complete, Standard or Extra.\n')
    list_choice = input('Please choose a list: \n').lower()

    if list_choice == 'standard':
        print('You chose the standard shopping list.\n')
        shop_list = SHEET.worksheet('standard').get_all_values()

    elif list_choice == 'extra':
        print('You chose the extra shopping list.\n')
        shop_list = SHEET.worksheet('extra').get_all_values()

    elif list_choice == 'complete':
        print('You chose the complete shopping list.\n')
        standard_list = SHEET.worksheet('standard').get_all_values()
        extra_list = SHEET.worksheet('extra').get_all_values()

        headings = standard_list[0]
        standard_list_values = standard_list[1:]
        extra_list_values = extra_list[1:]

        shop_list = headings + standard_list_values + extra_list_values

    else:
        print("Incorrect list choice. Please try again!\n")
        main()

    pprint(shop_list)
    return shop_list
    

def check_bought_item():
    """
    Lets the user check of items already bought on the list.
    """
    while True:
        print('\nWould you like to check of an item?\n')
        check_item = input('Y/N?\n').lower()

        if check_item == 'y':
            print('Choose the number of the item you like to check.\n')
            item_index = input('Item number:')
            
            if validate_index(item_index):
                print('Valid input.')
                break

        elif check_item == 'n':
            print('Going back to the main menu.\n')
            main()

        else:
            print('Wrong input, please try again.\n')   
            check_bought_item() 
        

def validate_index(value):
    """
    Validates item index as an integer.
    """
    try:
        index_value = int(value)
    except ValueError:
        print(f"Invalid data: {value} is not a whole number (no decimals). Please try again! \n")
        return False

    return True


def main():
    """
    Run all program functions.
    """
    view_shoping_list()
    check_bought_item()
    
    

main()