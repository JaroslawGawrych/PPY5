import smtplib
from email.mime.text import MIMEText

dict_list = []

filepath = "./students.txt"


def send_email(subject, body, sender, recipients, password):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ','.join(recipients)
    smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtp_server.login(sender, password)
    smtp_server.sendmail(sender, recipients, msg.as_string())
    smtp_server.quit()


def save():
    res = ""
    for element in dict_list:
        res += element["imie"] + " " + element["nazwisko"] + " " + element["email"] + " " + str(
            element["punkty"]) + " " + str(element["ocena"]) + " " + element["status"] + "\n"
    with open(filepath, "w") as file_object:
        file_object.write(res)


def giveGrade(points):
    grade = 0
    points = int(points)
    if 50 < points <= 60:
        grade = 3
    elif 60 < points <= 70:
        grade = 3.5
    elif 70 < points <= 80:
        grade = 4
    elif 80 < points <= 90:
        grade = 4.5
    elif points > 90:
        grade = 5
    else:
        grade = 2

    return grade


with open(filepath) as file_object:
    for x in file_object:
        line = x.rstrip().split(" ")
        student = {}
        student["imie"] = line[0]
        student["nazwisko"] = line[1]
        student["email"] = line[2]
        student["punkty"] = line[3]
        if len(line) == 4:
            student["ocena"] = ""
            student["status"] = ""
        if len(line) == 5:
            if line[4] == "2" or line[4] == "3" or line[4] == "3.5" or line[4] == "4" or line[4] == "4.5" or line[4] == "5":
                student["ocena"] = line[4]
                student["status"] = ""
            else:
                student["ocena"] = ""
                student["status"] = line[4]
        if len(line) == 6:
            student["ocena"] = line[4]
            student["status"] = line[5]
        dict_list.append(student)

opt = ""
while True:
    index = 0
    for x in dict_list:
        print(str(index) + ". " + str(x))
        index += 1
    print("==============================")
    print("0. zakoncz")
    print("1. dodaj studenta")
    print("2. usun studenta")
    print("3. wyslij maile")
    print("4. oceń uczniów automatycznie")
    opt = input("Podaj wybor: ")
    match opt:
        case "1":
            isUnique = True
            student = {}
            student["imie"] = input("podaj imie: ")
            student["nazwisko"] = input("podaj nazwisko: ")
            email = input("podaj email: ")
            for x in dict_list:
                if x["email"] == email:
                    isUnique = False
            while isUnique == False:
                isUnique = True
                print("email zajety")
                email = input("podaj email: ")
                for x in dict_list:
                    if x["email"] == email:
                        isUnique = False
            student["email"] = email
            student["punkty"] = input("podaj punkty: ")
            student["ocena"] = input("podaj ocene (puste jesli brak)")
            student["status"] = input("podaj status (puste jesli brak)")
            dict_list.append(student)
            save()
        case "2":
            index = input("podaj index studenta ktorego chcesz usunac: ")
            if int(index) <= len(dict_list) - 1 and int(index) >= 0:
                dict_list.pop(int(index))
            save()
        case "3":
            for x in dict_list:
                if x["status"] != "MAILED":
                    subject = "ocena z PPY"
                    body = "otrzymujesz ocenę : " + str(x["ocena"])
                    sender = "testguiwno@gmail.com"  ## mail
                    recipients = x["email"]
                    password = "rflfgovjrrootwcu"  ## hasło do aplikacji
                    send_email(subject, body, sender, recipients, password)
                    x["status"] = "MAILED"
            save()
        case "4":
            for x in dict_list:
                if x["status"] != "GRADED" or x["status"] != "MAILED":
                    x["ocena"] = giveGrade(int(x["punkty"]))
                    x["status"] = "GRADED"
            save()
        case "0":
            save()
            break
