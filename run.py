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

def view_shopping_list():
    """
    Lets the user choose if they what to see both shopping
    lists as one or one separate list, either standard list or
    the list for extra supplies. A complete list contains values 
    from both lists but only one heading.
    """
    
    print('Welcome to your personal shopping list!\n')
    print('Would you like to see a complete list?')
    print('Or your editable shopping list?')
    print('Choose between: Complete, Standard or Extra.\n')
    list_choice = input('Please choose a list: \n').lower()

    if list_choice == 'standard':
        print('You chose the standard shopping list.\n')
        shop_list = SHEET.worksheet('standard').get_all_values()
        pprint(shop_list)

    elif list_choice == 'extra':
        print('You chose the extra shopping list.\n')
        shop_list = SHEET.worksheet('extra').get_all_values()
        pprint(shop_list)

    elif list_choice == 'complete':
        print('\nYou chose the complete shopping list.')
        print('At the moment this list is view only.')
        print('Choose another list if you like to edit the list.\n')
        standard_list = SHEET.worksheet('standard').get_all_values()
        extra_list = SHEET.worksheet('extra').get_all_values()

        headings = [standard_list[0]]
        standard_list_values = standard_list[1:]
        extra_list_values = extra_list[1:]

        shop_list = headings + standard_list_values + extra_list_values  ##add sort on location
        pprint(shop_list)
        main()

    else:
        print("Incorrect list choice. Please try again!\n")
        main()

    
    return shop_list
    

def check_bought_item():
    """
    Lets the user choose which item on the list to check as 
    bought or if it needs to be bought.
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
    
    return item_index
        

def validate_index(value):
    """
    Validates item index of chosen item as an integer.
    Or informs the user to input a number.
    """
    try:
        value = int(value)  ##add validation of column length in list, and max int lenght after list lenght
    except ValueError:
        print(f"Invalid data: {value} is not a whole number (no decimals). Please try again! \n")
        return False

    return True

def check_item_in_worksheet(check_item, shopping_list):
    """
    If the item the user chose to check is in the list,
    the function finds the item and changes the value in 
    google sheet to either yes or no (to buy or not to buy).
    """ 
    index_num = int(check_item)
    
    if shopping_list == SHEET.worksheet('standard').get_all_values():
        standard = SHEET.worksheet('standard').col_values(1)
        standard_col = SHEET.worksheet('standard').col_values(3) 
        
        if check_item in standard:
            update_value = standard_col[index_num]

            if update_value == 'yes':
                check_position = int(standard.index(check_item))
                SHEET.worksheet('standard').update_cell(check_position + 1, 3, 'no')
                print(f"Item number {check_item} has been set to No!")
            
            elif update_value == 'no':
                check_position = int(standard.index(check_item))
                SHEET.worksheet('standard').update_cell(check_position + 1, 3, 'yes')
                print(f"Item number {check_item} has been set to Yes!")
            
        else:
            print('Item value not in list, please pick another value.')

    elif shopping_list == SHEET.worksheet('extra').get_all_values():
        extra = SHEET.worksheet('extra').col_values(1)
        extra_col = SHEET.worksheet('extra').col_values(3) 
                
        if check_item in extra:
            update_value = (extra_col[index_num])
            print(update_value)

            if update_value == 'yes':
                check_position = int(extra.index(check_item))
                SHEET.worksheet('extra').update_cell(check_position + 1, 3, 'no')
                print(f"Item number {check_item} has been set to No!")
            
            elif update_value == 'no':
                check_position = int(extra.index(check_item))
                SHEET.worksheet('extra').update_cell(check_position + 1, 3, 'yes')
                print(f"Item number {check_item} has been set to Yes!")

        else:
            print('Item value not in list, please pick another value.')

    else:
        print('Not possible to check complete list atm')  ##complete list is merger of two lists


def main():
    """
    Run all program functions.
    """
    shopping_list = view_shopping_list()
    check_item = check_bought_item()
    check_item_in_worksheet(check_item, shopping_list)

main()