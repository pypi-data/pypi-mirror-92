print("Created by Pranay Chopra, for more projects check https://github.com/Pranay-Chopra")
def init():
    import sys
    def bye():
        q=input("Quit? (y/n)")
        if q=='y' or q=='Y':
            sys.exit()
        elif q=='n' or q=='N':
            pass
        else:
            bye()
