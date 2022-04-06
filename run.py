import gspread
from google.oauth2.service_account import Credentials

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
        print('or part of your shopping list?')
        print('Choose between: Complete, Standard or Extra.\n')
        list_choice = input('Please choose a list: \n').lower()

        if list_choice == 'standard':
            print('You chose the standard shopping list.')
            shop_list = SHEET.worksheet('standard')
            data = shop_list.get_all_values()

            print(data)


view_shoping_list()