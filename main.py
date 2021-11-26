from functions import  *

def main():
    while True:
        clear()
        print("VITABLE\n")
        opt = input("""Enter option you would like to choose
                       1. Show Timetable
                       2. Show full timetable
                       3. Show a day's timetable
                       4. Add Courses
                       5. Delete courses
                       6. Delete timetable
                       7. Exit- """)

        if opt == "1" :
            showtodaytt()
        elif opt == "2" :
            showfulltt()
        elif opt == "3" :
            showdaytt()
        elif opt == "4" :
            addcourse()
        elif opt == "5" :
            deletecourse()
        elif opt == "6" :
            deletetimetable()
        elif opt == "7" :
            break
        else:
            print("INVALID INPUT")

if __name__ == "__main__" :
    main()
