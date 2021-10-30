try:
    a = int(input("Enter value of a: "))
    b = int(input("Enter value of b: "))
    c = a/b
    """The try function above attempts to execute the code it is provided, but does not print the result until the
    conditions below have been tested."""  
    
except ZeroDivisionError:
    print("Cannot devide by zero!")
    """If the user inputs a value of 0 for b, instead of producing the ZeroDivisionError and crashing, it prints that
    you cannot devide by zero"""    
    
except ValueError:
    print("Value is wrong")
    """If the user enters characters from the alphabet for a or b, instead of producing a ValueError and crashing, it
    prints that the value is wrong"""
    
else:
    print("a divided by b: ", c)
    """If neither of the exceptions above are encountered, the program will print the result of c"""
