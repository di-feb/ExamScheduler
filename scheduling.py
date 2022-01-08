import csv
import csp

def get_rows(filename):
    data = list()
    file =  open(filename, mode="r", encoding='utf-8-sig')
    reader = csv.reader(file)
    header =next(reader)
    if header:
        for row in reader:
            data.append(row)
    return data



def create_courses_for_labs(filename):
    file =  open(filename, mode="r+", encoding='utf-8-sig')
    csvwriter = csv.writer(file) 
    reader = csv.reader(file)
    for row in reader:
        if row[4] == 'TRUE':
            csvwriter.writerow([row[0], row[1] + "_lab", row[2], row[3], "FALSE"])
            # data.append([row[0], row[1] + "_lab", row[2], row[3], "FALSE"])

    file.close()


def getNames(data):
    names = list()
    for row in data:
        names.append(row[1])
    return names

# Finds the semester that a specific course is taught.
def find_semester(course, data):
    for row in data:
        if row[1] == course:
            return row[0]
    return 0

def is_hard(course, data):
    for row in data:
        if row[1] == course:
            if row[3] == "TRUE":
                return True
    return False

# Finds the teacher of a specific course.
def find_teacher(course, data):  
    for row in data:
        if row[1] == course:
            return row[2]
    return 0

def withLab(course, data):
    for row in data:
        if row[1] == course:
            if row[4] == "TRUE":
                return True
    return False


class Scheduling(csp.CSP):

    def __init__(self, data):
        """Initialize data structures for Scheduling."""
        timeslots = 3
        days = 21
        self.variables = list()
        self.domains = dict()
        self.neighbors = dict()

        # Φτιαξε τα variables
        for i in range(1, timeslots + 1):
            for j in range(1, days + 1):
                self.variables.append((i,j))

        # Φτιαξε τα domains
        for var in self.variables:
            self.domains[var] = getNames(data)
        
        #Φτιαξε τα neighbors
        for var in self.variables:
            self.neighbors[var] = [] 
            
            if(var[0] == 1):
                for i in range(0, 3):
                    for j in range(1, days - var[1] + 1):
                        self.neighbors[var].append((var[0] + i, var[1] + j))
                    for k in range(1, var[1]):
                        self.neighbors[var].append((var[0] + i, var[1] - k))
                    if(var != (var[0] + i, var[1])):
                        self.neighbors[var].append((var[0] + i, var[1]))
            elif(var[0] == 2):
                for i in range(-1, 2):
                    for j in range(1, days - var[1] + 1):
                        self.neighbors[var].append((var[0] + i, var[1] + j))
                    for k in range(1, var[1]):
                        self.neighbors[var].append((var[0] + i, var[1] - k))
                    if(var != (var[0] + i, var[1])):
                        self.neighbors[var].append((var[0] + i, var[1]))
            else:
                for i in range(-2, 1):
                    for j in range(1, days - var[1] + 1):
                        self.neighbors[var].append((var[0] + i, var[1] + j))
                    for k in range(1, var[1]):
                        self.neighbors[var].append((var[0] + i, var[1] - k))
                    if(var != (var[0] + i, var[1])):
                        self.neighbors[var].append((var[0] + i, var[1]))        
        csp.CSP.__init__(self, self.variables, self.domains, self.neighbors, self.schedule_constraint)

    def schedule_constraint(self, A, a, B, b):
        flag = True
        filename = "lessons.csv"
        data = get_rows(filename)
        # if(a == b and (A != B)):
        #     flag = False
        if(A[1] == B[1] and find_semester(a, data) == find_semester(b, data)):
            flag = False
        if(A[1] == B[1] and find_teacher(a, data) == find_teacher(b, data)):
            flag = False
        if(is_hard(a, data) and is_hard(b, data) and abs(A[1] - B[1]) < 2):
            flag = False
        if(withLab(a, data) and A[0] + 1 == B[0] and A[1] == B[1] and b != a + "_lab"):
            flag = False
        return flag

    def display(self, assignment, days):
        counter = 0
        items = assignment.items()
        for item in items:
            print(item, end=" ")
            counter = counter + 1
            if(counter == days):
                print("\n")
                counter = 0

    def getVar(self):
        return self.variables
    def getDomains(self):
        return self.domains



if __name__ == "__main__":
    filename = 'lessons.csv'
    data = get_rows(filename)
    days = 21

    Schedule = Scheduling(data)

    assignment = dict()
    for var in Schedule.getVar():
            assignment[var] = ""

    removals = list()

    assignment = csp.backtracking_search(Schedule)
    # assignments = csp.forward_checking(Schedule, tuple(Schedule.getVar()), Schedule.getDomains, assignment, removals)
    Schedule.display(assignment, days)



# def schedule_constraint(self, schedule):
#     # Δεν υπαρχει μαθημα του ιδιου εξαμηνου που να εξεταζεται την ιδια μερα.
#     different_semester = True
#     different_teacher = True
#     twoHard_inTwoDays = True
#     lab_after_theory = True
#     counter = 0
#     days = 21
#     while counter < days:
#         if( find_semester(schedule[0][counter]) == find_semester(schedule[1][counter]) and 
#             find_semester(schedule[1][counter]) == find_semester(schedule[2][counter]) and 
#             find_semester(schedule[0][counter]) == find_semester(schedule[2][counter]) ):
#             different_semester  = False
#         if(find_teacher(schedule[0][counter]) == find_teacher(schedule[1][counter]) and 
#             find_teacher(schedule[1][counter]) == find_teacher(schedule[2][counter]) and 
#             find_teacher(schedule[0][counter]) == find_teacher(schedule[2][counter]) ):
#             different_semester  = False
#         if(is_hard(schedule[0][counter]) or is_hard(schedule[1][counter]) or is_hard(schedule[2][counter])):
#             if(is_hard(schedule[0][counter + 1]) or is_hard(schedule[1][counter + 1]) or is_hard(schedule[2][counter + 1]) 
#             or is_hard(schedule[0][counter + 2]) or is_hard(schedule[1][counter + 2]) or is_hard(schedule[2][counter + 2])):
#                 twoHard_inTwoDays = False
#         if(withLab(schedule[2][counter])):
#             lab_after_theory = False
#         elif(withLab(schedule[1][counter]) and schedule[2][counter] != schedule[1][counter] + "_lab"):
#             lab_after_theory = False
#         elif(withLab(schedule[0][counter]) and schedule[1][counter] != schedule[1][counter] + "_lab"):
#             lab_after_theory = False

#     return different_semester and different_teacher and twoHard_inTwoDays and lab_after_theory 