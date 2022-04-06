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
    the list for extra supplies.
    """
    while True:
        print('Welcome to your personal shopping list!\n')
        print('Would you like to see a complete list?')
        print('Or part of your shopping list?')
        print('Choose between: Complete, Standard or Extra.\n')
        list_choice = input('Please choose a list: \n').lower()

        if list_choice == 'standard':
            print('You chose the standard shopping list.\n')
            shop_list = SHEET.worksheet('standard')
            data = shop_list.get_all_values()

        elif list_choice == 'extra':
            print('You chose the extra shopping list.\n')
            shop_list = SHEET.worksheet('extra')
            data = shop_list.get_all_values()

        elif list_choice == 'complete':
            print('You chose the complete shopping list.\n')
            standard_list = SHEET.worksheet('standard').get_all_values()
            extra_list = SHEET.worksheet('extra').get_all_values()

            headings = standard_list[0]
            standard_list_values = standard_list[1:]
            extra_list_values = extra_list[1:]

            data = headings + standard_list_values + extra_list_values

        else:
            print("Incorrect list choice. Please try again!\n")
            view_shoping_list()

        pprint(data)


view_shoping_list()