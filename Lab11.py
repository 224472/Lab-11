

import matplotlib.pyplot as plt
import os




class Student:
    def __init__(self,name, id_num):
        self.name = name
        self.id_num = id_num


class Assignment:
    def __init__(self,name,ass_id,point):
        self.name = name
        self.ass_id=ass_id
        self.point = point

class Submissions:
    def __init__(self,id_num,ass_id,percent):
        self.id_num = id_num
        self.ass_id=ass_id
        self.percent = percent

    def calculate(self,ass_pts):
        # self.ass_pts=ass_pts, useless
        total_pts_scored=ass_pts*(self.percent/100)
        return total_pts_scored

class GradeCalculator:
    def __init__(self):
        self.students={}
        self.assignments={}
        self.submissions=[]
    def get_students(self):
        with open('students.txt','r') as file:
            for line in file:
                line = line.strip()
                student_id = line[:3]
                student_name = line[3:]
                student=Student(line[3:],line[:3])


                self.students[student_name]=student
    def get_assignments(self):
        #
        # with open('assignments.text','r') as file:
        #     lines = file.readlines()
        #     name_ass=[]
        #     for line in range(0,len(lines),3):
        #         name_ass.append(line)
        #     id_ass=[]
        #     for line in range(1,len(lines),3):
        #         id_ass.append(line)
        #     grd_pt=[]
        #     for line in range(2,len(lines),3):
        #         grd_pt.append(line)

        with open('assignments.txt','r') as file:
            lines = file.readlines()

            for line in range(0,len(lines),3):
                ass_name= lines[line].strip()
                ass_id=lines[line+1].strip()
                ass_pt=int(lines[line+2].strip())
                assignment = Assignment(ass_name,ass_id,ass_pt)
                self.assignments[ass_name]=assignment
    def get_submissions(self):

        submission_folder = 'submissions'
        for files in os.listdir(submission_folder):
            filepath = os.path.join(submission_folder, files)

            with open(filepath,'r') as file:
                for line in file:
                    line = line.strip()
                    line = line.split("|")
                    student_id = line[0]
                    ass_id = line[1]
                    percent = float(line[2])
                    submission = Submissions(student_id, ass_id, percent)
                    self.submissions.append(submission)

    def load_data(self):
        self.get_students()
        self.get_assignments()
        self.get_submissions()
    def calculate_grade(self,student_name):

        student=self.students[student_name]
        sub_student=[]
        total_pts_scored = 0
        for submission in self.submissions:
            if submission.id_num==student.id_num:
                sub_student.append(submission)
        for submission in sub_student:
            for assignment in self.assignments.values():
                if assignment.ass_id==submission.ass_id:
                    # sub_student.append(assignment)
                    pt_earned=submission.calculate(assignment.point)
                    total_pts_scored+=pt_earned
        percentage=total_pts_scored/1000*100
        return round(percentage)
    def calc_ass_stat(self,assignment_name):
        if assignment_name not in self.assignments:
            return None
        assignment = self.assignments[assignment_name]
        scores = []

        for submission in self.submissions:
            if submission.ass_id == assignment.ass_id:
                scores.append(submission.percent)

        if not scores:
            return None
        return {
            'min': round(min(scores)),
            'avg': round(sum(scores) / len(scores)),
            'max': round(max(scores))
        }
    def display_ass_gr(self, assignment_name):
        if assignment_name not in self.assignments:
            return False
        assignment = self.assignments[assignment_name]
        scores = []
        for submission in self.submissions:
            if submission.ass_id == assignment.ass_id:
                scores.append(submission.percent)
        if not scores:
            return False
        plt.hist(scores, bins=[0, 25, 50, 75, 100], edgecolor='black')
        plt.xlabel('Score (%)')
        plt.ylabel('Number of Students')
        plt.title(f'Score Distribution for {assignment_name}')
        plt.grid(axis='y', alpha=0.3)
        plt.show()

        return True



def main():
    print("1. Student grade")
    print("2. Assignment statistics")
    print("3. Assignment graph")
    calc=GradeCalculator()
    calc.load_data()
    select=int(input("Select an option: "))
    if select == 1:
        student_name = input("What is the student's name: ")
        grade = calc.calculate_grade(student_name)
        print(f"{grade}%")
    elif select == 2:
        assignment_name = input("What is the assignment name: ")
        stats = calc.calc_ass_stat(assignment_name)
        if stats:
            print(f"Min: {stats['min']}%")
            print(f"Avg: {stats['avg']}%")
            print(f"Max: {stats['max']}%")

    elif select == 3:
            assignment_name = input("What is the assignment name: ")
            calc.display_ass_gr(assignment_name)

if __name__ == "__main__":
    main()














