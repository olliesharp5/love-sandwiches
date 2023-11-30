import gspread
from google.oauth2.service_account import Credentials
#enables the use of pprint
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')


def get_sales_data():
    """
    Get sales figures input from the user.
    Run a while loop to collect a valid string of data from the user
    via the terminal, which must be a string of 6 numbers separated
    by commas. The loop will repeatedly request data, until it is valid.
    """
    while True:
        print("Please enter sales data from the last market.")
        print("Data should be six numbers, separated by commas.")
        print("Example: 10,20,30,40,50,60\n")

        data_str = input("Enter your data here: ")

        sales_data = data_str.split(",")

        if validate_data(sales_data):
            print("Data is valid!")
            break
    
    return sales_data


def validate_data(values):
    """
    Inside the try, converts all string values into integers.
    Raises ValueError if strings cannot be converted into int,
    or if there aren't exactly 6 values.
    """
    try:
        # list comprehention to change each value in our values list into an integer
        [int(value) for value in values]
        # checks if the length equals 6
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values required, you privided {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False
    #returns true if the value has passed the validator check 
    return True 


def update_sales_worksheet(data):
    """
    Update sales worksheet, add new row with the list data provided.
    """
    #provides response to user that data has been sent to worksheet
    print("Updating sales worksheet...\n")
    #acesses the sales worksheet  by using the SHEET variable called at top of code and the gspread worksheet() method, "sales" refers to the name of the worksheet(tab) in the actual document
    sales_worksheet = SHEET.worksheet("sales")
    #uses the gspread append method to add a new row to the worksheet
    sales_worksheet.append_row(data)
    print("Sales worksheet updated successfully.\n")


def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and calculate the surplus for each item type.

    The surplus is defined as the sales figure subtracted from the stock:
    - Positive surplus indicates waste
    - Negative surplus indicates extra made when stock was sold out.
    """
    print("Calculating surplus data...\n")
    #obtains values in the stock sheet using gspread methods worksheet() and get_all_values()
    stock = SHEET.worksheet("stock").get_all_values()
    #variable to obtain the last row in the stock data, uses slice method [-1 ] to always obtian the final row in the sheet
    stock_row = stock[-1]
    print(stock_row)



def main():
    """
    Run all program functions
    """
    data = get_sales_data()
    #list comprehention to convert string values into integers 
    sales_data = [int(num) for num in data]
    update_sales_worksheet(sales_data)
    calculate_surplus_data(sales_data)

#prints an initial message before the data needs to be inputted by the user
print("Welcome to Love Sandwiches Data Automation")
#important to note you can’t call a function above where it is defined in the file
main()