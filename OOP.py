class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def add_courses(self, course_name):
        self.finished_courses.append(course_name)

    def rate_lecturer(self, lecturer_name, course, grade):
        if isinstance(lecturer_name, Lecturer) and course in lecturer_name.courses_attached and \
                course in self.courses_in_progress and 0 <= grade <= 10:
            if course in lecturer_name.grades:
                lecturer_name.grades[course] += [grade]
            else:
                lecturer_name.grades[course] = [grade]
        else:
            return "Ошибка"

    def average_grades_hw(self):  # Подсчет средней оценки за д/з
        total = 0
        counter = 0
        for key, value in self.grades.items():
            for grades in value:
                total += grades
                counter += 1
        return round(total / counter, 1)

    def __eq__(self, other):
        if not isinstance(other, Student):
            print("Not a Student")
            return
        return self.average_grades_hw() == other.average_grades_hw()

    def __gt__(self, other):
        if not isinstance(other, Student):
            print("Not a Student")
            return
        return self.average_grades_hw() > other.average_grades_hw()

    def __str__(self):
        res = f"Имя: {self.name} \nФамилия: {self.surname} \nСредняя оценка за домашние задания: " \
              f"{self.average_grades_hw()} \nКурсы в процессе изучения: {self.courses_in_progress} \n" \
              f"Завершенные курсы: {self.finished_courses}"
        return res


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}

    def average_grades(self):  # Подсчет средней оценки за лекции
        total = 0
        counter = 0
        for key, value in self.grades.items():
            for grades in value:
                total += grades
                counter += 1
        return round(total / counter, 1)

    def __eq__(self, other):
        if not isinstance(other, Lecturer):
            print("Not a Lecturer")
            return
        return self.average_grades() == other.average_grades()

    def __gt__(self, other):
        if not isinstance(other, Lecturer):
            print("Not a Lecturer")
            return
        return self.average_grades() > other.average_grades()

    def __str__(self):
        res = f"Имя: {self.name} \nФамилия: {self.surname} \nСредняя оценка за лекции: {self.average_grades()}"
        return res


class Reviewer(Mentor):
    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self):
        res = f"Имя: {self.name} \nФамилия: {self.surname}"
        return res


best_student = Student('Ruoy', 'Eman', 'M')  # Студент №1
best_student.courses_in_progress += ['Python']
best_student.courses_in_progress += ["Введение"]
best_student.finished_courses += ["Git"]

worst_student = Student("Peter", "Parker", "M")  # Студент №2
worst_student.courses_in_progress += ['Python']
worst_student.courses_in_progress += ["Введение"]
worst_student.finished_courses += ["Git"]

cool_lecturer = Lecturer('Some', 'Buddy')  # Лектор №1
cool_lecturer.courses_attached += ['Python']
cool_lecturer.courses_attached += ['Введение']
cool_lecturer.courses_attached += ["Git"]

bad_lecturer = Lecturer("Andrey", "Koval")  # Лектор №2
bad_lecturer.courses_attached += ['Python']
bad_lecturer.courses_attached += ['Введение']
bad_lecturer.courses_attached += ["Git"]

new_reviewer = Reviewer("Bella", "Ert")  # Проверяющий №1
new_reviewer.courses_attached += ['Python']
new_reviewer.courses_attached += ['Введение']

new_reviewer.rate_hw(best_student, "Python", 8)  # Ставим оценки студентам
new_reviewer.rate_hw(best_student, "Python", 8)
new_reviewer.rate_hw(best_student, "Введение", 9)
new_reviewer.rate_hw(worst_student, "Python", 5)
new_reviewer.rate_hw(worst_student, "Python", 4)
new_reviewer.rate_hw(worst_student, "Введение", 6)

best_student.rate_lecturer(cool_lecturer, "Python", 10)  # Ставим оценки лекторам
best_student.rate_lecturer(cool_lecturer, "Введение", 9)
best_student.rate_lecturer(cool_lecturer, "Python", 8)
best_student.rate_lecturer(bad_lecturer, "Python", 10)
best_student.rate_lecturer(bad_lecturer, "Введение", 9)
best_student.rate_lecturer(bad_lecturer, "Python", 8)

list_students = [best_student, worst_student]
list_lecturer = [cool_lecturer, bad_lecturer]


def all_grades_students_in_course(lst, course):  # Средняя оценка всех студентов в рамках курса
    all_grades = []
    for student in lst:
        for key, value in student.grades.items():
            if key == course:
                for grade in value:
                    all_grades.append(grade)
    if not all_grades:
        return "Ошибка"
    else:
        return round((sum(all_grades) / len(all_grades)), 1)


def all_grades_lecturer_in_course(lst, course):
    all_grades = []
    for lecturer in lst:
        for key, value in lecturer.grades.items():
            if key == course:
                for grade in value:
                    all_grades.append(grade)
    if not all_grades:
        return "Ошибка"
    else:
        return round((sum(all_grades) / len(all_grades)), 1)


print(best_student)
print()
print(bad_lecturer)
print()
print(new_reviewer)
print()
print(all_grades_students_in_course(list_students, "Python"))
print(all_grades_lecturer_in_course(list_lecturer, "Python"))
