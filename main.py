from prettytable import PrettyTable
from datetime import datetime
import mysql.connector as server
import random
import sys

mycon = server.connect(
    host="localhost", 
    user="root", 
    passwd="", 
    database="hotel")

if mycon.is_connected():
    print("Successfully connected to MySQL database.")
else:
    print("Not connected.")

cursor = mycon.cursor(buffered=True)
#print(cursor.execute("SHOW TABLES"))

cursor.execute('''
    CREATE TABLE IF NOT EXISTS record (
        customer_id INT NOT NULL,
        name VARCHAR(50) NOT NULL,
        address VARCHAR(50) NOT NULL,
        phno INT(15) NOT NULL,
        checkin date NOT NULL,
        checkout date NOT NULL,
        room_price FLOAT DEFAULT 0,
        room_type VARCHAR(50),
        room_no INT NOT NULL UNIQUE,
        food_price FLOAT DEFAULT 0,
        ttpay FLOAT DEFAULT 0,
        PRIMARY KEY(customer_id)
    )
''')

# Colors
MAGENTA = "\033[0;35m"
BRIGHT_MAGENTA = "\033[0;95m"
DARKCYAN = '\033[36m'
GREEN = "\033[0;32m"
BRIGHT_GREEN = "\033[0;92m"
YELLOW = '\033[93m'
RED = '\033[91m'

# Styles.
BOLD = '\033[1m'
UNDERLINE = '\033[4m'
END = '\033[0m'


print(BRIGHT_MAGENTA + BOLD + UNDERLINE +
      "\n\n\t\t\t𖣔  Welcome to Glorious Riverfront Hotel! 𖣔")
print(BOLD + "\t\t\t\tMarjan Island, Saudi Arabia.\n" + END)

def validate_date(date):
    try:
        datetime.strptime(date, '%Y-%m-%d')
        return 0
    except ValueError:
        return 1


# Main house function.
def Menu():

    print(GREEN + "\n\t\t 1. Rooms Info\n")
    print("\t\t 2. Booking\n")
    print("\t\t 3. Food Service (Menu Card)\n")
    print("\t\t 4. Record\n")
    print('\t\t 5. Payment\n')
    print("\t\t 0. Exit\n" + END)

    choice = int(input("Enter your choice: "))

    if choice == 1:
        Rooms_info()
    elif choice == 2:
        Booking()
    elif choice == 3:
        Food_service()
    elif choice == 4:
        Record()
    elif choice == 5:
        Payment()
    elif choice == 0:
        print('\nThank you,\nVisit again :)')
        mycon.close()
        sys.exit("")
    else:
        print(RED + BOLD + "You entered an invalid choice. Please enter a valid choice.\n" + END)
        Menu()

def Booking():

    b = False
    while b==False:
        name = input("Enter your name: ")
        address = input("Enter address: ")
        ph_no = input("Enter mobile number: ")

        if (name != "" and address != "" and ph_no.isdigit()==True):
            b = True
        else:
            print(RED + BOLD + "Please enter valid data.\n" + END)

    # Randomly creating customer_id & room_no.
    customer_id = random.randint(100, 999)
    room_no = random.randint(0, 50)
     
    # Checking if customer_id or room_no already exists in table or not.
    cursor.execute("SELECT customer_id FROM record")
    existing_cust_ids = [item[0]
                        for item in cursor.fetchall()]  # Extract ids from the tuples using list comprehension

    if customer_id in existing_cust_ids:  # Check if id already exists in the list
        new_id = random.randint(100, 900)
        customer_id = new_id

    cursor.execute("SELECT room_no FROM record")
    existing_room_nos = [item[0]
                         for item in cursor.fetchall()]  # Extract ids from the tuples using list comprehension

    if room_no in existing_room_nos:  # Check if room_no already exists in the list
        new_room_no = random.randint(0, 50)
        room_no = new_room_no
    
    # For saving checking & checkout dates.
    checkin_date = ""
    checkout_date = ""

    a = False
    while a == False:
        Check_in = input("Enter a check-in date (Year-Month-Date): ")
        Check_out = input("Enter a check-out date (Year-Month-Date): ")

        if (validate_date(Check_in) or validate_date(Check_out) == 1):
            print(RED + BOLD + "Enter date in the given format.\n" + END)

        else:
            # Converting strings to date objects
            date_format = "%Y-%m-%d"
            Check_in_ob = datetime.strptime(Check_in, date_format)
            Check_out_ob = datetime.strptime(Check_out, date_format)

            if (Check_out_ob > Check_in_ob and Check_in_ob != Check_out_ob):
                checkin_date = Check_in_ob
                checkout_date = Check_out_ob
                a = True
            else:
                print(RED + BOLD + "Make sure check-out date is after check-in date.\n" + END)
    
    # Getting number of days:
    delta1 = checkout_date - checkin_date
    delta = delta1.days

    def room_type():
        # local variables.
        room_price = 0
        sel_room_type = ""
        
        print("\n----SELECT ROOM TYPE----")
        print(" 1. Standard Non-AC")
        print(" 2. Standard AC")
        print(" 3. 3-Bed Non-AC")
        print(" 4. 3-Bed AC")
        print(("Press 0 for Room Prices"))
        choice = int(input("\nYour choice: "))
        print("---------------------------------------------------------------")
        
        if choice == 0:
            print(" 1. Standard Non-AC - 300 SR/night")
            print(" 2. Standard AC - 400 SR/night")
            print(" 3. 3-Bed Non-AC - 450 SR/night")
            print(" 4. 3-Bed AC - 500 SR/night\n")
            room_type()

        elif choice == 1:
            sel_room_type = "Standard Non-AC"
            print(YELLOW + BOLD + "\nRoom Type- Standard Non-AC")
            room_price += 300*delta  # Standart rate with respect to n days.
            print("Total Price: %s SR" % (room_price) + END)

        elif choice==2:
            sel_room_type = 'Standard AC'
            print(YELLOW + BOLD + "\nRoom Type- Standard AC")
            room_price += 400*delta
            print("Total Price: %s SR" % (room_price) + END)
        
        elif choice==3:
            sel_room_type = '3-Bed Non-AC'
            print(YELLOW + BOLD + "\nRoom Type- 3-Bed Non-AC")
            room_price += 450*delta
            print("Total Price: %s SR" % (room_price) + END)
            
        elif choice==4:
            sel_room_type = '3-Bed AC'
            print(YELLOW + BOLD + "\nRoom Type- 3-Bed AC")
            room_price += 500*delta
            print("Total Price: %s SR" % (room_price) + END)
        else:
            print(RED + BOLD + " Wrong choice..!!" + END)
            room_type()

        print(YELLOW + BOLD + "\nYour Room no: %s" % room_no + END)
        print(YELLOW + BOLD + 'Your Customer ID: %s' % customer_id + END)

        cursor.execute("INSERT INTO record VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                       (customer_id, name, address, int(ph_no), checkin_date, checkout_date, room_price, sel_room_type, room_no, 0, room_price))
        mycon.commit()

        print(DARKCYAN + UNDERLINE + BOLD + "\n*Room has been booked successfully for %s days*\n" %(delta) + END)
        Menu()

    room_type()


def Rooms_info():
    print("\n		 ------ HOTEL ROOMS INFO ------")
    print("")
    print("STANDARD NON-AC")
    print("---------------------------------------------------------------")
    print("Room amenities include: 1 Double Bed, Television, Telephone,")
    print("Double-Door Cupboard, 1 Coffee table with 2 sofa, Balcony and")
    print("an attached washroom with hot/cold water.\n")
    print("STANDARD AC")
    print("---------------------------------------------------------------")
    print("Room amenities include: 1 Double Bed, Television, Telephone,")
    print("Double-Door Cupboard, 1 Coffee table with 2 sofa, Balcony and")
    print("an attached washroom with hot/cold water + Window/Split AC.\n")
    print("3-Bed NON-AC")
    print("---------------------------------------------------------------")
    print("Room amenities include: 1 Double Bed + 2 Single Bed, Television,")
    print("Telephone, a Triple-Door Cupboard, 1 Coffee table with 2 sofa, 2")
    print("Side table, Balcony with an Accent table with 2 Chair and an")
    print("attached washroom with hot/cold water.\n")
    print("3-Bed AC")
    print("---------------------------------------------------------------")
    print("Room amenities include: 1 Double Bed + 2 Single Bed, Television,")
    print("Telephone, a Triple-Door Cupboard, 1 Coffee table with 2 sofa, ")
    print("2 Side table, Balcony with an Accent table with 2 Chair and an")
    print("attached washroom with hot/cold water + Window/Split AC.\n")

    Menu()

def Food_service():
    cust_id = int(input("Customer ID: "))
    def restaurant():
        global i
        total_bill = 0
        print("-------------------------------------------------------------------------")
        print("						 Hotel Glorious Riverfront")
        print("-------------------------------------------------------------------------")
        print("						 Menu Card")
        print("-------------------------------------------------------------------------")
        print("\n BEVARAGES				     26. Dal Fry................ 14.00")
        print("----------------------------------	     27. Dal Makhani............ 15.00")
        print(" 1. Regular Tea............. 2.00	     28. Dal Tadka.............. 15.00")
        print(" 2. Masala Tea.............. 2.50")
        print(" 3. Coffee.................. 2.50	     ROTI")
        print(" 4. Cold Drink.............. 2.50	     ----------------------------------")
        print(" 5. Bread Butter............ 3.00	     29. Plain Roti.............. 1.50")
        print(" 6. Bread Jam............... 3.00	     30. Butter Roti............. 1.50")
        print(" 7. Veg. Sandwich........... 5.00	     31. Tandoori Roti........... 2.00")
        print(" 8. Veg. Toast Sandwich..... 5.00	     32. Butter Naan............. 2.00")
        print(" 9. Cheese Toast Sandwich... 7.00")
        print(" 10. Grilled Sandwich........ 7.00	     RICE")
        print("					     ----------------------------------")
        print(" SOUPS					     33. Plain Rice.............. 9.00")
        print("----------------------------------	     34. Jeera Rice.............. 9.00")
        print(" 11. Tomato Soup............ 11.00	     35. Veg Pulao.............. 11.00")
        print(" 12. Hot & Sour............. 11.00	     36. Peas Pulao............. 11.00")
        print(" 13. Veg. Noodle Soup....... 11.00")
        print(" 14. Sweet Corn............. 11.00	     SOUTH INDIAN")
        print(" 15. Veg. Munchow........... 11.00	     ----------------------------------")
        print("				             37. Plain Dosa............. 10.00")
        print(" MAIN COURSE				     38. Onion Dosa............. 11.00")
        print("----------------------------------	     39. Masala Dosa............ 13.00")
        print(" 16. Shahi Paneer........... 11.00	     40. Paneer Dosa............ 13.00")
        print(" 17. Kadai Paneer........... 11.00	     41. Rice Idli.............. 13.00")
        print(" 18. Handi Paneer........... 12.00	     42. Sambhar Vada........... 14.00")
        print(" 19. Palak Paneer........... 12.00")
        print(" 20. Chilli Paneer.......... 14.00	     ICE CREAM")
        print(" 21. Matar Mushroom......... 14.00	     ----------------------------------")
        print(" 22. Mix Veg................ 14.00	     43. Vanilla................. 6.00")
        print(" 23. Jeera Aloo............. 14.00	     44. Strawberry.............. 6.00")
        print(" 24. Malai Kofta............ 14.00	     45. Pineapple............... 6.00")
        print(" 25. Aloo Matar............. 14.00	     46. Butter Scotch........... 6.00")
        print("\nPress 0 to end")
        
        ch = 1
        while(ch != 0):
            new_ch = input("-> ")
            if new_ch.isdigit()==False:
                print(RED + BOLD + "Wrong Choice..!!\n" + END)
                ch = 1
            else:
                ch=int(new_ch)

                # if-elif-conditions to assign item
                # prices listed in menu card
                if ch == 1 or ch == 31 or ch == 32:
                    price_of_item = 2
                    total_bill = total_bill+price_of_item
                elif ch <= 4 and ch >= 2:
                    price_of_item = 2.5
                    total_bill = total_bill+price_of_item
                elif ch <= 6 and ch >= 5:
                    price_of_item = 3
                    total_bill = total_bill+price_of_item
                elif ch <= 8 and ch >= 7:
                    price_of_item = 5
                    total_bill = total_bill+price_of_item
                elif ch <= 10 and ch >= 9:
                    price_of_item = 7
                    total_bill = total_bill+price_of_item
                elif (ch <= 17 and ch >= 11) or ch == 35 or ch == 36 or ch == 38:
                    price_of_item = 11
                    total_bill = total_bill+price_of_item
                elif ch <= 19 and ch >= 18:
                    price_of_item = 12
                    total_bill = total_bill+price_of_item
                elif (ch <= 26 and ch >= 20) or ch == 42:
                    price_of_item = 14
                    total_bill = total_bill+price_of_item
                elif ch <= 28 and ch >= 27:
                    price_of_item = 15
                    total_bill = total_bill+price_of_item
                elif ch <= 30 and ch >= 29:
                    price_of_item = 1.5
                    total_bill = total_bill+price_of_item
                elif ch == 33 or ch == 34:
                    price_of_item = 9
                    total_bill = total_bill+price_of_item
                elif ch == 37:
                    price_of_item = 10
                    total_bill = total_bill+price_of_item
                elif ch <= 41 and ch >= 39:
                    price_of_item = 13
                    total_bill = total_bill+price_of_item
                elif ch <= 46 and ch >= 43:
                    price_of_item = 6
                    total_bill = total_bill+price_of_item
                elif ch == 0:
                    pass
                else:
                    print(RED + BOLD + "Wrong Choice..!!\n" + END)
        print(BOLD + "\nTotal Bill: ", total_bill, 'SR\n' + END)

        cursor.execute("SELECT food_price FROM record WHERE customer_id = %s", (cust_id,))
        old_price = cursor.fetchone()

        total_bill_new = total_bill + old_price[0] # select query fetching one field. Adding [0] will give value.
        cursor.execute("UPDATE record SET food_price = %s WHERE customer_id = %s", (total_bill_new, cust_id))
        mycon.commit()

        cursor.execute("SELECT ttpay FROM record WHERE customer_id = %s", (cust_id,))
        past_ttpay = cursor.fetchone()
        total_pay = past_ttpay[0] + total_bill # only food price updation.
        cursor.execute("UPDATE record SET ttpay = %s WHERE customer_id = %s", (total_pay, cust_id))
        mycon.commit()

        Menu()


    cursor.execute("SELECT * FROM record WHERE customer_id = %s", (cust_id,))
    table_verify = cursor.fetchone()

    # cursor.fetchone() returns None when there are no results.
    if table_verify is not None and cust_id == table_verify[0]:
        restaurant()
    else:
        print(RED + BOLD + "Customer ID not found.\n" + END)
        Food_service()


def Record():
    cust_id = int(input("Enter your customer ID: "))

    def Record_prog():
        cursor.execute(
            "SELECT * FROM record WHERE customer_id = %s", (cust_id,))

        # Fetch the column names
        column_names = [desc[0] for desc in cursor.description] # creating a list of column names from the
        # description attribute of the cursor object. Basically a list of column names that will be used later.
        
        rows = cursor.fetchall()

        # Create a PrettyTable object
        table = PrettyTable()
        
        # Add the column names
        table.field_names = column_names
        
        # Add the rows
        for row in rows:
            table.add_row(row)

        # Print the table
        print(table)

    cursor.execute("SELECT * FROM record WHERE customer_id = %s", (cust_id,))
    table_verify = cursor.fetchone()

    # cursor.fetchone() returns None when there are no results.
    if table_verify is not None and cust_id == table_verify[0]:
            Record_prog()
    else:
        print(RED + BOLD + "Customer ID not found.\n" + END)
        Record()

    Menu()

def Payment():
    cust_id = int(input("Enter your Customer ID: "))

    def Paying():
        cursor.execute("SELECT ttpay FROM record WHERE customer_id = %s", (cust_id,))
        overall_total = cursor.fetchone()

        if overall_total is not None and overall_total[0] !=0:
            print("\nYour total unpaid payment: %s Saudi Riyal. Please clear it as soon as possible" % overall_total, '\n\n')

            a = False
            while a == False:
                yes_no = input("Do you want to pay it now? (y/n): ")
                if yes_no == "y" or yes_no == "Y":
                    cursor.execute(
                        "UPDATE record SET ttpay = %s WHERE customer_id = %s", (0, cust_id))
                    mycon.commit()
                    print(BOLD + "\n\nYour payment has been successfully made! Thank you.\n" + END)
                    a = True
                    Menu()

                elif yes_no == 'n' or yes_no == "N":
                    print(BOLD + "Payment cancelled!\n" + END)
                    a = True
                    Menu()
                else:
                    print(RED + BOLD + "Please enter a valid choice.\n" + END)

        else:
            print(BOLD + "\nYou don't have any undue payment. Thank you!\n" + END)
            Menu()


    cursor.execute("SELECT * FROM record WHERE customer_id = %s", (cust_id,))
    table_verify = cursor.fetchone()

    # cursor.fetchone() returns None when there are no results.
    if table_verify is not None and cust_id == table_verify[0]:
        Paying()
    else:
        print(RED + BOLD + "Customer ID not found.\n" + END)
        Payment()

Menu()
mycon.close()