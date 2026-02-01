import mysql.connector
import time as t

# import getpass
# password = getpass.getpass("Enter DB Password: ")

try:
    con = mysql.connector.connect(
         host="localhost",
         user="root",
         # password=password,
         password="pinku@123"
         database="Bank_system1"
        )
    if con.is_connected():
     cur = con.cursor() 
    else:
        exit()    

except mysql.connector.Error as e:
    print("Database error :",e)

def get_current_balance(Id):
    cur.execute("select amount from passbook where Id=%s order by txn_Id desc limit 1",(Id,))
    data=cur.fetchone()
    if data:
        return data[0]
    else:
        return 0
    
# ================= DEPOSIT =================              
def deposit():
    Id = int(input("Enter id : "))
    user_deposit = int(input("Enter amount to deposit : "))
    previous_amount= get_current_balance(Id)
    amount = previous_amount + user_deposit
    debit = 0
    credit = user_deposit
    time_now=t.ctime()
    sql = """
    INSERT INTO Passbook (Id, Amount, Debit, Credit,created_at)
    VALUES (%s, %s, %s, %s,%s)
    """
    values = (Id, amount, debit, credit,time_now)

    cur.execute(sql, values)
    con.commit()
    print("✅Amount deposit successfully :", amount)

    with open("orders.txt", "a") as file:
        file.write("Transaction Type : Deposit\n")        
        file.write(f"Bank Name           : imr college\n")
        file.write(f"Id                  : {Id}\n")
        file.write(f"Current Balance     : {amount}\n")
        file.write(f"Credit              : {credit}\n")
        file.write(f"Time                : {time_now}\n")
        file.write("_" * 40 + "\n")

# ================= WITHDRAW =================
def withdraw():
    Id = int(input("Enter id : "))
    user_withdrowl = int(input("Enter amount to withdraw : "))

    previous_amount = get_current_balance(Id)

    if user_withdrowl <= previous_amount:
        amount = previous_amount - user_withdrowl
        debit = user_withdrowl
        credit = 0
        time_now = t.ctime()

        sql = """
        INSERT INTO Passbook (Id, Amount, Debit, Credit, created_at)
        VALUES (%s, %s, %s, %s, %s)
        """
        values = (Id, amount, debit, credit, time_now)
        cur.execute(sql, values)
        con.commit()

        print("✅ Amount withdrawn successfully :", amount)
    else:
        print("❌ Insufficient Balance")
        return

    with open("orders.txt", "a") as file:
        file.write(f"Bank Name           : imr college\n")
        file.write(f"Id                  : {Id}\n")
        file.write(f"Current Balance     : {amount}\n")
        file.write(f"debit               : {debit}\n")
        file.write(f"Time                : {time_now}\n")
        file.write("_" * 40 + "\n")

# ================= CHECK BALANCE =================        
def Check_balance():
   Id=int(input("Enter id : "))
   balance=get_current_balance(Id)
   print(" Your Current Balance :",balance)
   with open("orders.txt", "a") as file:
        file.write(f"Id      : {Id}\n")
        file.write(f"Balance :{balance}\n")
        file.write("_" * 40 + "\n")
    
   print("Thanks for visting this Bank :")

# ================= DELETE NOTEPAD =================
def Delete_notepad():
   with open("orders.txt","w") as file:
      file.write(" ")
   print("Delete Notepad data List Successfully : ")

# ================= APPLY LOAN =================    
def Apply_loan():
    Name=input("Enter Your Name :")
    mobile=input("Enter Your Mobile Number :")
    income=float(input("Enter Your Monthly Income :"))
  

    sql="insert into customers1(Name,mobile_number,income)values(%s,%s,%s)"
    query=(Name,mobile,income)
    cur.execute(sql,query)
    con.commit()

    customer_id=cur.lastrowid
    print("\n✅ Customer Registered Successfully!")
    print("🆔 Your Customer ID is :", customer_id)

    loan_type=input("Loan Type (Home/Personal/Education):")
    amount=int(input("Loan Amount:"))
    tenure=int(input("Tenure (years): "))

    sql="Insert into loans1(customer_id, loan_type, amount, tenure, status) values(%s,%s,%s,%s,%s) "
    query=(customer_id,loan_type,amount,tenure,"pending")
    cur.execute(sql,query)
    con.commit()

    print("✅ Loan Applied Successfully! Status: Pending")

# ================= EMI CALCULATOR =================
def view_status():
    cid=int(input("Enter Customer Id : "))
    cur.execute("Select * From loans1 Where customer_id=%s",(cid,))
    data=cur.fetchall()

    if data:
     for row in data:  
        print("loan Id :",row[0])
        print("Name    :",row[1])  
        print("Type    :",row[2])
        print("Amount  :",row[3]) 
        print("Tenure  :",row[4])
        print("Status  :",row[5])
        print("--------------------")
    else:
        print("❌ No Loan Found") 

# ================= EMI CALCULATOR =================
def emi_calculator():
    Principal_amount = int(input("Enter Loan Amount: "))
    Interst_rate = float(input("Interest Rate (%): "))
    years = int(input("Tenure (years): "))

    Rate = Interst_rate / (12 * 100)
    Tenure = years * 12
    # emi = (Principal_amount * Rate * (1 + Rate) ** Tenure) / ((1 + Rate) ** Tenure - 1)  

    if Rate == 0:
     emi = Principal_amount / Tenure
    else:
      emi = (Principal_amount * Rate * (1 + Rate) ** Tenure) / ((1 + Rate) ** Tenure - 1)

    print("💸 Monthly EMI:", round(emi, 2))

# ================= ADMIN LOGIN =================
def admin_login():
    username = input("Enter Admin Username: ")
    password = input("Enter Admin Password: ")

    cur.execute(
        "SELECT * FROM admin WHERE username=%s AND password=%s",
        (username, password)
    )
    data = cur.fetchone()

    if data:
        print("✅ Admin Login Successful")
        admin_panel()
    else:
        print("❌ Invalid Admin Credentials")

# ================= ADMIN PANEL =================
def admin_panel():   
    cur.execute("SELECT * FROM loans1 WHERE status='Pending'")
    data = cur.fetchall()

    if not data:
        print(" loan not pending ")
        return
    
    print("\n--- Pending Loans ---")
    for row in data: 
        print("loan Id        :",row[0])  
        print("Customer ID    :",row[1])
        print("Type           :",row[2])
        print("Amount         :",row[3]) 
        print("Tenure         :",row[4])
        print("Status         :",row[5])
        print("--------------------")        
        

    loan_id = int(input("Enter Loan ID to update: "))
    status = input("Enter Status (Approved/Rejected): ").lower()

    if status not in ["approved", "rejected"]:
        print("❌ Invalid status")
        return
    
    cur.execute(
        "UPDATE loans1 SET status=%s WHERE loan_id=%s",
        (status, loan_id)
    )
    con.commit()
    print("✅ Loan Status Updated successfully") 

# ================= MENUS =================        
def banking_menu():
    while True:
       print("""
             ===========Welcome To MY Banking System===========
             1. Dopsit for Amount
             2. Withdror for Amount
             3. Check Balance for Amount
             4. Delete for Notepad
             5. Exit""")

       choice = input("Enter your choice : ")
       if choice == "1":            
            deposit()
       elif choice == "2":         
            withdraw()
       elif choice == "3":          
            Check_balance()
       elif choice == "4":          
            Delete_notepad() 
       elif choice == "5":
            print("Thank You!")
            break
       else:
            print("❌ Invalid Choice")           

def loan_menu():
    while True:
        print("""
        ===== BANK LOAN MANAGEMENT =====
        1. Apply for Loan
        2. View Loan Status
        3. EMI Calculator
        4. Admin Login
        5. Exit
        """)

        choice = input("Enter Your Choice: ")

        if choice == "1":
            Apply_loan()
        elif choice == "2":
            view_status()
        elif choice == "3":
            emi_calculator()
        elif choice == "4":
            admin_login()
        elif choice == "5":
            print("Thank You!")
            break
        else:
            print("❌ Invalid Choice")

def call():
    while True:
        print("1. Banking System")
        print("2. Loan System")
        print("3. Exit")

        choice = input("Enter your choice : ")

        if choice == "1":
            banking_menu()
        elif choice == "2":
            loan_menu()
        elif choice == "3":
            con.close()
            print("Database connection closed")
            break
        else:
            print("❌ Invalid Option")
call()            





