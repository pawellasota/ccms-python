import ui
import sqlite3
import data
import assignment
import submission
import datetime
import attendance
import data
import sqlite3


class User:
    """
        Base class creates user object

        Args:
            name: check_if_correct(name, str)
            surname: check_if_correct(surname, str)
            check_gender: gender
            gender: gender
            date_validate: birth_date
            birth_date: birth_date
            email:
            login:login
            password: check_if_correct(password, str)
    """
    def __init__(self, _id, name, surname, gender, birth_date, email, login, password):
        """
        Initialize user object

        Args:
            name: check_if_correct(name, str)
            surname: check_if_correct(surname, str)
            check_gender: gender
            gender: gender
            date_validate: birth_date
            birth_date: birth_date
            email:
            login:login
            password: check_if_correct(password, str)
        """
        self._id = _id
        self.name = self.check_if_correct(name, str)
        self.surname = self.check_if_correct(surname, str)
        self.check_gender(gender)
        self.gender = gender
        self.date_validate(birth_date)
        self.birth_date = birth_date
        self.email = email
        self.login = login
        self.password = self.check_if_correct(password, str)

    @staticmethod
    def check_if_correct(validate, check_type):
        """
        Checks if variable is expected type and convert it to integer type if it contains just digits

        Args:
            validate: variable to check
            check_type: expected type of variable

        Returns:
            validated variable
        """
        if type(validate) != check_type:
            raise TypeError("Wrong format for: " + str(validate))
        elif type(validate) == check_type:
            if validate.isdigit():
                validate = int(validate)
                return validate
            elif all(i.isalpha() or i.isspace() for i in validate):
                return validate
            else:
                raise TypeError("Wrong format for: " + str(validate))

    def check_gender(self, gender):
        """
        Checks if variable is correct type of gender, if not - it raises an error

        Args:
            gender: variable to check

        Returns:
            None
        """
        gender_list = ['male', 'female', 'not sure']
        if gender.lower() not in gender_list:
            raise NameError('Gender should be: male, female, not sure')

    def date_validate(self, birth_date):
        """
        Checks if data format is correct

        Args:
            birth_date: variable to check

        Returns:
         True if data format is correct
        """
        if datetime.datetime.strptime(birth_date, '%Y-%m-%d').strftime('%Y-%m-%d'):
            return True


class Employee(User):
    """Class creates object employee"""
    def __init__(self, _id, name, surname, gender, birth_date, email, login, password):
        """
        Initialize employee object that inherits from User class

        Args:
            name: check_if_correct(name, str)
            surname: check_if_correct(surname, str)
            check_gender: gender
            gender: gender
            date_validate: birth_date
            birth_date: birth_date
            email:
            login:login
            password: check_if_correct(password, str)
        """
        super().__init__(_id, name, surname, gender, birth_date, email, login, password)

    def list_students(self):
        """
        Return student list to display

            Args:
                organisation

            Returns:

                student list
        """
        student_list = []
        cursor = data.Data.init_db()
        cursor.execute("SELECT * FROM `User` WHERE User_type='student'")
        students = cursor.fetchall()
        n = 1
        for student in students:
            student_list.append([str(n) + ".", student[1], student[2]])
            n += 1
        return student_list

    def view_student_details(self):
        """
        Returns students details list to display

            Args:
                organisation

            Returns:

                student detail list
        """

        student_list = []
        cursor = data.Data.init_db()
        cursor.execute("SELECT * FROM `User` WHERE User_type='student'")
        students = cursor.fetchall()
        n = 1
        for student in students:
            student_list.append([str(n) + ".", student[1], student[2], student[3],
                                 student[4], student[5], student[6], student[7]])
            n += 1
        return student_list


class Student(User):
    """Class creates object student"""
    def __init__(self, _id, name, surname, gender, birth_date, email, login, password):
        """
        Initialize student object that inherits from User class

       Args:
            name: check_if_correct(name, str)
            surname: check_if_correct(surname, str)
            check_gender: gender
            gender: gender
            date_validate: birth_date
            birth_date: birth_date
            email:
            login:login
            password: check_if_correct(password, str)
        """
        super().__init__(_id, name, surname, gender, birth_date, email, login, password)
        self.my_submissions_list = []

    def __str__(self):
        return self.name+self.surname

    def view_my_grades(self, organisation):
        """
        Method display list of submitted assignment with grades

        Args:
            organisation

        Return:
            list of submitted assignment with grades

        """
        my_submissions_list = []
        i = 0
        for submission_ in organisation.submissions_list:
            if submission_.student.name == self.name and submission_.student.surname == self.surname:
                if submission_.grade:
                    submission_to_add = [str(i+1), submission_.assignment.name, submission_.grade]
                    my_submissions_list.append(submission_to_add)
                    i += 1
        return my_submissions_list

    def submit_assignment(self, organisation):
        """
        Method allows student to submit assignment

        Args:
            organisation

        Return:
            list of submitted assignment

        """
        submission_list_done = []
        for submission_ in organisation.submissions_list:
            if submission_.student.name == self.name and submission_.student.surname == self.surname:
                if submission_.grade == "":
                    submission_list_done.append(submission_.assignment) # submission_list_done -
                                                                        # graded assignments of actual student
        final_list = [assignment for assignment in organisation.assignments_list if assignment not in submission_list_done]
        if final_list:
            table_to_print = []
            id_ = 1
            for assignment in final_list:
                table_to_print.append([str(id_), assignment.name, assignment.max_points,
                                       assignment.delivery_date, assignment.content])
                id_ += 1
            ui.Ui.print_table(table_to_print, ["ID", "Assignment name", "Assignment max points",
                                               "delivery date", "Content"])
            options = ui.Ui.get_inputs(["->"], "")
            if options[0] == "0":
                return
            picked_assignment = final_list[int(options[0]) - 1]
            new_submission = submission.Submission(picked_assignment, self)
            new_submission.provide_result()
            organisation.submissions_list.append(new_submission)
        else:
            print("No assignments left.")
            return


class Mentor(Employee):
    """Class creates object mentor"""
    def __init__(self, _id, name, surname, gender, birth_date, email, login, password):
        """
        Initialize mentor object that inherits from User class

        Args:
            name: check_if_correct(name, str)
            surname: check_if_correct(surname, str)
            check_gender: gender
            gender: gender
            date_validate: birth_date
            birth_date: birth_date
            email:
            login:login
            password: check_if_correct(password, str)
        """
        super().__init__(_id, name, surname, gender, birth_date, email, login, password)

    def add_student(self):
        """
        Method allows mentor to add student to students list

        Args:
            organisation
        Return:
             None
        """
        options = ui.Ui.get_inputs(["Name", "Surname", "Gender", "Birth date", "Email", "Login",
                                    "Password"], "Provide information about new student")

        if options[0].isalpha() and options[1].isalpha() and options[2] in ['male', 'female', 'not sure']:
            if options[3].isalpha():
                print('Data should have format: YYYY-MM-DD')
                return
        else:
            print('\nWrong input!\nName: only letters\nSurname: only letters\n'
                  'Gender: you can choose only male, female or not sure\nData format: YYYY-MM-DD\n')
            return

        data = sqlite3.connect("program.db")
        cursor = data.cursor()
        cursor.execute("INSERT INTO `User` (`name`, `surname`, `gender`, `birth_date`, `email`, `login`, `password`, `user_type`) "
                       "VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')"
                       .format(options[0], options[1], options[2], options[3],
                               options[4], options[5], options[6], "student"))
        data.commit()
        data.close()
        print("Student was added.")

    def check_attendance(self, organisation):
        """
        Method allows mentor check students attendance

        Args:
            organisation
        Return:
             None
        """
        students_list = []
        i = 0
        for student in organisation.students_list:
            students_list.append(student.surname+" "+student.name)
        options = ui.Ui.get_inputs(students_list, "Starting attendance check (mark 0 for absence, Enter otherwise)")

        for student in organisation.students_list:
            new_attendance = attendance.Attendance(student, str(datetime.date.today()), options[i])
            organisation.attendance_list.append(new_attendance)
            i += 1

    def remove_student(self):
        """
        Method allows mentor remove students from students list

        Args:
            organisation
        Return:
             None
        """
        self.list_students()
        options = ui.Ui.get_inputs([""], "Enter number to erase student from database: ")
        if int(options[0]) < 0 or int(options[0]) > len(self.list_students()):
            print("There is no such student number on the list")
            return

        data = sqlite3.connect("program.db")
        cursor = data.cursor()
        cursor.execute("SELECT * FROM `user` WHERE `user_type`='student'")
        students = cursor.fetchall()
        student_to_erase_name = students[int(options[0])-1][1]
        student_to_erase_surname = students[int(options[0])-1][2]
        print(student_to_erase_name, student_to_erase_surname)
        cursor.execute("DELETE FROM `User` WHERE `name`='{}' AND `surname`='{}'"
                       .format(student_to_erase_name, student_to_erase_surname))
        data.commit()
        data.close()
        print("Student was erased.")


    def edit_student(self):
        """
        Method allows mentor edit students specific data

        Args:
            organisation
        Return:
             None
        """
        self.list_students()
        choosed_student = ui.Ui.get_inputs([""], "Enter number to edit student's data")
        if choosed_student[0] == "0" or int(choosed_student[0]) > len(self.list_students()):
            return
        options = ui.Ui.get_inputs(["Name", "Surname", "Gender", "Birth date", "Email", "Login",
                                    "Password"], "Edit information about student")
        if options[0].isalpha() and options[1].isalpha() and options[2] in ['male', 'female', 'not sure']:
            if options[3].isalpha():
                print('Data should have format: YYYY-MM-DD')
                return
        else:
            print('\nWrong input!\nName: only letters\nSurname: only letters\n'
                  'Gender: you can choose only male, female or not sure\nData format: YYYY-MM-DD\n')
            return
        data = sqlite3.connect("program.db")
        cursor = data.cursor()
        cursor.execute("SELECT * FROM `user` WHERE `user_type`='student'")
        students = cursor.fetchall()
        student_to_edit_name = students[int(choosed_student[0]) - 1][1]
        student_to_edit_surname = students[int(choosed_student[0]) - 1][2]

        cursor.execute(
            "UPDATE `User` SET `name`='{}', `surname`='{}', `gender`='{}', `birth_date`='{}', `email`='{}', `login`='{}', `password`='{}' "
            " WHERE "
            "`name`='{}' AND `surname`='{}'"
            .format(options[0], options[1], options[2], options[3],
                    options[4], options[5], options[6], student_to_edit_name, student_to_edit_surname))
        data.commit()
        data.close()
        print("Update completed")

    def grade_submission(self, organisation):
        """
        Method allows mentor grade students submitted assignment

        Args:
            organisation
        Return:
             None
        """
        list_submission = []
        i = -1
        for submission_ in organisation.submissions_list:
            if not submission_.grade:
                list_submission.append(submission_)
            else:
                i += 1
        if not list_submission:
            print("No submission available")
            return
        table_to_print = []
        id_ = 1
        for submission_ in list_submission:
            table_to_print.append([str(id_), submission_.assignment.name, submission_.result])
            id_ += 1
        ui.Ui.print_table(table_to_print, ["ID", "Assignment name", "Submission result"])
        options = ui.Ui.get_inputs(["->"], "")
        if options[0].isalpha() or int(options[0]) > len(list_submission):
            print("There is no such number of assignment on list")
            return
        if options[0] == "0":
            return
        picked_submission = list_submission[int(options[0])-1]
        options = ui.Ui.get_inputs(["Enter grade for this submission: "], "")
        if options[0].isalpha() or int(options[0]) < 0 or int(options[0]) > 5:
            print("Grade can be only number in range 0-5")
            return
        picked_submission.grade = options[0]

    def add_assignment(self):
        """
        Method allows mentor add new assignment to assignment list

        Args:
            organisation
        Return:
             None
        """
        options = ui.Ui.get_inputs(["Name", "Type", "Max. points to receive", "Delivery date", "Content"],
                                    "Provide information about new assignment")
        # if options[0].isalpha() and options[1].isdigit():
        #     if options[2].isalpha():
        #         print('\nData format: YYYY-MM-DD\n')
        #         return
        # else:
        #     print('\nWrong input!\nName: only letters\nMax Points: only numbers\nData should have format: YYYY-MM-DD\n')
        #     return

        data = sqlite3.connect("program.db")
        cursor = data.cursor()
        cursor.execute(
            "INSERT INTO `assignment` (`name`, `type`, `max_points`, `delivery_date`, `content`) "
            "VALUES ('{}', '{}', '{}', '{}', '{}')"
            .format(options[0], options[1], options[2], options[3],
                    options[4]))
        data.commit()
        data.close()
        print("Assignment was added.")


    def add_team(self):
        pass


class Manager(Employee):
    """Class creates object mentor"""
    def __init__(self, _id, name, surname, gender, birth_date, email, login, password):
        """
        Initialize mentor object that inherits from User class

        Args:
            name: check_if_correct(name, str)
            surname: check_if_correct(surname, str)
            check_gender: gender
            gender: gender
            date_validate: birth_date
            birth_date: birth_date
            email:
            login:login
            password: check_if_correct(password, str)
        """
        super().__init__(_id, name, surname, gender, birth_date, email, login, password)

    def add_mentor(self):
        """
        Method allows manager to add mentor to mentors list

        Args:
            organisation
        Return:
             None
        """
        options = ui.Ui.get_inputs(["Name", "Surname", "Gender", "Birth date", "Email", "Login",
                                    "Password"], "Provide information about new mentor")
        if options[0].isalpha() and options[1].isalpha() and options[2] in ['male', 'female', 'not sure']:
            if options[3].isalpha():
                print('\nData should have format: YYYY-MM-DD\n')
                return
        else:
            print('\nWrong input!\nName: only letters\nSurname: only letters\n'
                  'Gender: you can choose only male, female or not sure\nData should have format: YYYY-MM-DD\n')
            return

        # new_mentor = Mentor(options[0], options[1], options[2], options[3], options[4], options[5],
        #                     options[6])

        data = sqlite3.connect("program.db")
        cursor = data.cursor()
        cursor.execute("INSERT INTO `User`(Name, Surname, Gender, Birth_date, Email, Login, Password, User_type) "
                       "VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')"
                       .format(options[0], options[1], options[2], options[3],
                               options[4], options[5], options[6], "mentor"))
        data.commit()
        data.close()
        print("Mentor was added.")

    def remove_mentor(self):
        """
        Method allows manager to remove mentor from mentors list

        Args:
            organisation
        Return:
             None
        """
        options = ui.Ui.get_inputs(["Name", "Surname"], "Enter number to erase mentor from database")

        if options[0].isnumeric() and options[1].isnumeric():
            print('\n You have to type  Name and Surname from Mentors list')
            return

            mydata = c.execute('DELETE FROM Zoznam WHERE Name=?', (data3,))
        data = sqlite3.connect("program.db")
        cursor = data.cursor()
        cursor.execute("DELETE FROM `User` WHERE Name = '{}' and Surname= '{}'").format(options[0], options[1])
        data.commit()
        data.close()

        print("Mentor was erased.")

    def edit_mentor(self, organisation):
        """
        Method allows manager to edit mentor specific data

        Args:
            organisation
        Return:
             None
        """
        self.list_mentors(organisation)
        options = ui.Ui.get_inputs([""], "Enter number to edit mentor's data")
        mentor = organisation.mentors_list[int(options[0]) - 1]
        options = ui.Ui.get_inputs(["Name", "Surname", "Gender", "Birth date", "Email", "Login",
                                    "Password"], "Edit information about mentor")
        if options[0].isalpha() and options[1].isalpha() and options[2] in ['male', 'female', 'not sure']:
            if options[3].isalpha():
                print('\nData should have format: YYYY-MM-DD\n')
                return
        else:
            print('\nWrong input!\nName: only letters\nSurname: only letters\n'
                  'Gender: you can choose only male, female or not sure\n')
            return
        mentor.name = options[0]
        mentor.surname = options[1]
        mentor.gender = options[2]
        mentor.birth_date = options[3]
        mentor.email = options[4]
        mentor.login = options[5]
        mentor.password = options[6]
        print("Update completed")
        self.list_mentors(organisation)

    def list_mentors(self):
        """
        Method allows manager to list all mentor from list

        Args:
            organisation
        Return:
             None
        """
        mentor_list = []
        data = sqlite3.connect("program.db")
        cursor = data.cursor()
        cursor.execute("SELECT * FROM `User` WHERE User_type='mentor'")
        mentors = cursor.fetchall()
        n = 1
        for mentor in mentors:
            mentor_list.append([str(n) + ".", mentor[1], mentor[2]])
            n += 1
        data.commit()
        data.close()
        return mentor_list


    def view_mentors_details(self):
        """
        Returns mentors details list to display

        Args:
            organisation

        Returns:

            student detail list
        """
        mentors_details_list = []
        data = sqlite3.connect("program.db")
        cursor = data.cursor()
        cursor.execute("SELECT * FROM `User` WHERE User_type='mentor'")
        mentors = cursor.fetchall()
        n = 1
        for mentor in mentors:
            mentors_details_list.append([str(n) + ".", mentor[1], mentor[2], mentor[3], mentor[4],
                                         mentor[5], mentor[6], mentor[7]])
            n += 1
        data.commit()
        data.close()
        return mentors_details_list

    def average_grade():
        pass
    def full_stats():
        pass