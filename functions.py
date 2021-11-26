from Slotdata import *
from datetime import datetime
from initialize import *


def addcourse_db(Course):
    cursor.execute("INSERT INTO Courses values (?,?,?,?)",
                    (Course.name, str(Course.slots), Course.type, str(Course.dt)))
    mycon.commit()

def addschedule_db(Day):
    cursor.execute("UPDATE Schedules SET schedule = ? WHERE day = ?", (str(Day.schedule), Day.day,))
    mycon.commit()

def loadcourse(name):
    cursor.execute("SELECT * FROM Courses WHERE name = ?",(name,))
    name, slots, type, dt = cursor.fetchall()[0]
    slots, dt = eval(slots), eval(dt)
    Course = course(name, slots, type, dt)
    return Course

def loadday(name):
    cursor.execute("SELECT * FROM Schedules WHERE day = ?",(name,))
    name, schedule = cursor.fetchall()[0]
    schedule = eval(schedule)
    Day = day(name, schedule)
    return Day



def addcourse():
    clear()
    while True:
        Course = course()
        Course.name = input("\nEnter course name : ")

        Course.type = Course.name[7].upper()
        while Course.type not in ["L","P"]:
            print("Couldn't automatically identify course type!")
            Course.type = input("Please enter type of course (Theory - L | Practical/Lab - P) : ").upper()[:1]

        Course.slots = input("Please enter course slots (eg- E2+TE2) : ").upper().split("+")

        if Course.type == "L":
            daysTL = daysTh
            days = list(daysTL.keys())
            times = thSlots
        else:
            daysTL = daysLb
            days = list(daysTL.keys())
            times = lbSlots
        for slot in Course.slots:
            for day in daysTL:
                dt = {}
                dt[day]=[]
                daysl = daysTL[day]
                if slot in daysl:
                    for i in range(len(daysl)):
                        if slot == daysl[i]:
                            time = times[i]
                            dt[day].append(time)
                            coursedetails = [time, Course.name, slot, Course.type]
                            d1 = loadday(day)
                            d1.schedule.append(coursedetails)
                            d1.schedule.sort()
                            addschedule_db(d1)
        addcourse_db(Course)
        print("\nSuccessfully added course!")
        opt = input("Do you want to add more courses (y/n) : ").lower()[:1]
        if opt == "n":
            break


def deletecourse():
    clear()
    cursor.execute("SELECT name, slots FROM Courses")
    courses = cursor.fetchall()
    cursor.execute("SELECT schedule FROM Schedules")
    days = cursor.fetchall()
    print("Courses\n")
    for i in range(len(courses)):
        print(i+1,courses[i][0],f"({'+'.join(eval(courses[i][1]))})")
    deletecourse = input(("Input enter the sno of course to be deleted from above : "))
    if not deletecourse.isdigit():
        print("\nPlease enter a valid number!")
        input("\nPress Enter to Continue..")
        return
    deletecourse = int(deletecourse)
    if deletecourse>len(courses) or deletecourse<1:
        print("\nInvalid option plese enter valid option!")
        input("\nPress Enter to Continue..")
        return
    coursename, courseslot = courses[deletecourse-1]
    cursor.execute("DELETE FROM Courses WHERE name = ?",(coursename,))
    for i in days:
        i = eval(i[0])
        k = list(i)
        for j in i:
            if j[1] == coursename :
                k.remove(j)
        cursor.execute("UPDATE Schedules SET schedule = ? WHERE schedule = ?",
                        (str(k), str(i)))
    mycon.commit()
    print("Course deleted!")
    input("\nPress Enter to Continue..")



def deletetimetable():
    clear()
    confirm = input("""Are you sure you want to clear all the contents of the timetable?
This step is irreversible. Type "yes" to confirm : """)

    if confirm != "yes" :
        print("\nTimetable not deleted, if you want to delete the timetable try again!\n")
        input("Press enter to continue..")
        return
    cursor.execute("DELETE FROM Schedules")
    cursor.execute("DELETE FROM Courses")
    mycon.commit()
    print("Deleted timetable!")
    input("Press enter to continue..")


def showdaytt():
    Day = input("Enter the day : ").lower()
    if Day not in days :
        print("Please Enter a valid day (eg - monday, friday)")
        input("\nPress enter to continue..")
        return
    cursor.execute("SELECT schedule FROM Schedules WHERE day = ?",(Day,))
    timetable = eval(cursor.fetchone()[0])
    clear()
    print(f"Day's schedule : {Day}")
    for i in timetable:
        print(i[1])
        print(f"Course type : {i[3]}")
        print(f"Slot : {i[2]}")
        print(f"Time : {i[0]}\n")

    input("\nPress enter to continue..")



def showtodaytt():
    d, time = datetime.now().strftime("%A %H:%M").lower().split()
    cursor.execute("SELECT schedule FROM Schedules WHERE day = ?",(d,))
    timetable = eval(cursor.fetchall()[0][0])
    ongoing = False
    for i in range(len(timetable)):
        end = timetable[i][0].split()[2]
        if end<time:
            continue
        else:
            start = timetable[i][0].split()[0]
            if start < time:
                ongoing = True
            timetable = timetable[i:]
            break
    else:
        timetable = []

    clear()
    print("Today's Timetable :  Classes left\n")
    if timetable == []:
        print("No classes left to attend today!")
        return
    if ongoing:
        print("-> Ongoing!")
    else:
        print("-> Next class")
    for i in timetable:
        print(i[1])
        print(f"Course type : {i[3]}")
        print(f"Slot : {i[2]}")
        print(f"Time : {i[0]}\n")

    input("\nPress enter to continue..")



def showfulltt():
    clear()
    cursor.execute("SELECT * FROM Schedules")
    data = cursor.fetchall()
    for k in data:
        day, schedule = k
        schedule = eval(schedule)
        print(f"Day's schedule : {day}\n")
        for i in schedule:
            print(i[1])
            print(f"Course type : {i[3]}")
            print(f"Slot : {i[2]}")
            print(f"Time : {i[0]}\n")
        print("-"*50)
    input("\nPress Enter to continue..")
