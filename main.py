import mysql.connector
from datetime import datetime

# Small Pizza $15
# Medium Pizza $20
# Large Pizza $25

# Extras
# Pepperoni for small pizza $2
# Pepperoni for medium/large pizza $3
# Extra cheese $1

# Send welcome msg "Welcome to Python Pizza Deliveries"
# get size with variable named size, S,M,L
# ask for pepperoni add_pepperoni? Y/N
# ask for extra cheese extra_cheese Y/N

# output: Your final bill is $28

from credentials import host, user, password, database


prices = {
    'S': 15,
    'M': 20,
    'L': 25,
    'PS': 2,
    'PML': 3,
    'C': 1
}
final_bill = 0


def db_connect():
    # Establish a connection to the MySQL database
    fxn_connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )

    # Create a cursor object to interact with the database
    fxn_cursor = fxn_connection.cursor()
    return fxn_cursor, fxn_connection


def db_read():
    # Connect to DB
    cursor, connection = db_connect()
    try:
        # Execute SQL queries to read and write data

        # Reading data
        cursor.execute('SELECT * FROM orders')
        result_set = cursor.fetchall()
        for row in result_set:
            print(row)

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        # Close the cursor and the connection
        cursor.close()
        connection.close()
        print("Read DB successfully")


def db_write(size, extra_p, extra_c, amt, f_name):
    # Connect to DB
    cursor, connection = db_connect()

    try:
        # Execute SQL queries to write data

        insert_query = """INSERT INTO orders (
                        first_name, order_size, extra_pepperoni, extra_cheese, amount,
                        order_timestamp, created, points_gained) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        data_to_insert = (f_name, size, extra_p, extra_c, amt, datetime.now(), datetime.now(), amt*0.05)
        cursor.execute(insert_query, data_to_insert)
        connection.commit()  # Commit the changes

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        # Close the cursor and the connection
        cursor.close()
        connection.close()
        print("Saved all data to the DB successfully")


def get_greeting(first_name):
    from datetime import datetime

    # Get the current time
    current_time = datetime.now().time()

    # Define time ranges for different greetings
    morning_start = datetime.strptime("06:00:00", "%H:%M:%S").time()
    afternoon_start = datetime.strptime("12:00:00", "%H:%M:%S").time()
    evening_start = datetime.strptime("18:00:00", "%H:%M:%S").time()

    # Determine the greeting based on the current time
    if current_time < morning_start:
        greeting = "Good night"
    elif current_time < afternoon_start:
        greeting = "Good morning"
    elif current_time < evening_start:
        greeting = "Good afternoon"
    else:
        greeting = "Good evening"

    # welcome message
    print("-" * 80 + f"\n {greeting} {first_name}, Welcome to Python Pizza Deliveries \n" + "-" * 80)
    # return greeting


def request_pizza():
    global final_bill, prices

    db_read()

    size = input(f'\n What size of pizza do you want? S for Small, '
                 f'M for Medium, and L for Large >>> ').upper()
    if (size == 'S') or (size == 'M') or (size == 'L'):
        final_bill += prices[size]

        print("\n" + "-" * 8 + f"\n Extras \n" + "-" * 8)

        add_pepperoni = input("\nDo you want extra pepperoni? (Y/N) >>> ").upper()

        if add_pepperoni == "Y":
            pepperoni_size = input("\nWhat size of extra pepperoni do you want? S for Small,"
                                   " L for medium/Large >>> ").upper()
            if pepperoni_size == "S":
                final_bill += prices["PS"]
                extra_p = 'Small'
            elif pepperoni_size == "L":
                final_bill += prices["PML"]
                extra_p = 'Large'
            else:
                print("\nWrong input, extra pepperoni will be skipped\n")
                extra_p = 'No'
        else:
            print("Pepperoni have been skipped")
            extra_p = 'No'

        extra_cheese = input("\nDo you want extra cheese? (Y/N) >>>  ").upper()

        if extra_cheese == "Y":
            final_bill += prices["C"]
            extra_c = 'Yes'
        else:
            print("\nExtra cheese have been skipped")
            extra_c = 'No'

        print(f'\nYour final bill is ${final_bill}, thanks for your patronage!\n\n')
    else:
        print('\nWrong input, please try again!!!\n\n')

    db_write(size, extra_p, extra_c, final_bill, f_name)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    f_name = input("Please enter your first name: >>> ").title()
    get_greeting(f_name)

    pizza_count = input("How many pizzas do you want to order? >>> ")
    try:
        pizza_count = int(pizza_count)
        while pizza_count > 0:
            request_pizza()
            pizza_count -= 1
    except ValueError:
        print("Input is not a number, exiting the application.")

