cash=3000
x=cash
code =1234


def withdraw ():
    amt=int (input("Please Enter Amount : "))
    print("1 for confirm")
    print("2 for exit")
    ch=int(input())
    if ch==1:
        pin=int(input("Enter your pin:"))
        print("1 for confirm")
        print("2 for exit")
        cho=int(input())
        if pin==code:
            if cho==1:
                print("Transaction is being processed !!!")
                print("Please wait")
                cash=cash-amt
                if cash<1000:
                    print("Insufficient Balance ")
                    print("Can't withdraw money")
                    cash=x
                else:
                    print("Please collect your cash ")
                    print("Remaining Balance: ", cash)
            else:
                exit
        else:
            print("Invalid pin code")
            exit
    else:
        exit


#x={"Manish":1234,"Harsh":9876}
print("Welcome to XYZ ATM Service")
name=input(("Enter your Name : "))
print("Hello", name)
print("Please Select a language")
print("1 for hindi")
print("2 for English")
lang=int(input())
if lang==2:
    print("Dear customer please select the transaction ")
    print("1 for Banking")
    print("2 for pin generation")
    print("3 for fast cash")
    print("4 for cash withdraw")
    print("5 for cash deposit")
    trans=int(input())
    if trans==4:
        withdraw ()
    else:
        print("Function will run shortly")
        exit
else:
    print("hindi is currently not available")
    exit







