import csv
import csp

def get_rows(filename):
    data = list()
    file =  open(filename, mode="r", encoding='UTF8')
    reader = csv.reader(file)
    header =next(reader)
    if header:
        for row in reader:
            data.append(row)
    file.close()
    return data



def create_courses_for_labs(filename):
    file =  open(filename, mode="r+", encoding="UTF8")
    csvwriter = csv.writer(file) 
    reader = csv.reader(file)
    lab = list()
    for row in reader:
        if row[4] == "TRUE":
            lab.append([1, row[1] + "_lab", row[2], "FALSE", "FALSE"])
    csvwriter.writerows(lab)

    file.close()


def getCourses(data):
    courses = list()
    for row in data:
        courses.append(row[1])
    return courses

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
        values = list()
        self.domains = dict()
        self.neighbors = dict()

        # Φτιαξε τα values
        for i in range(1, days + 1):
            for j in range(1, timeslots + 1):
                values.append((i,j))

        # Φτιαξε τα variables
        self.variables = getCourses(data)

        # Φτιαξε τα domains
        for var in self.variables:
            self.domains[var] = values

        #Φτιαξε τα neighbors
        for var in self.variables:
            self.neighbors[var] = [] 
            for var2 in self.variables:
                if var != var2:
                    self.neighbors[var].append(var2)
            
        csp.CSP.__init__(self, self.variables, self.domains, self.neighbors, self.schedule_constraint)

    def schedule_constraint(self, A, a, B, b):
        flag = True
        filename = "lessons.csv"
        data = get_rows(filename)

    
        if(withLab(A, data) and a[1] + 1 == b[1] and a[0] == b[0] and B != A + "_lab"):
            flag = False
        if(withLab(B, data) and b[1] + 1 == a[1] and a[0] == b[0] and A != B + "_lab"):
            flag = False

        if(A == B and (a != b)):
            flag = False
        if(A != B and (a == b)):
            flag = False
        if(a[0] == b[0] and find_semester(A, data) == find_semester(B, data) and (A != B + "_lab" and B != A + "_lab")):
            flag = False
        if(a[0] == b[0] and find_teacher(A, data) == find_teacher(B, data) and (A != B + "_lab" and B != A + "_lab")):
            flag = False
        if(is_hard(A, data) and is_hard(B, data) and abs(a[0] - b[0]) < 2 and (A != B + "_lab" and B != A + "_lab")):
            flag = False

        if( (withLab(A, data) and a[1] == 3 ) or (withLab(B, data) and b[1] == 3) ):
            flag = False
        
     
        return flag

    def display(self, assignment, timeslots, filename):

        data = get_rows(filename)
        counter = 0
        assignment = dict(sorted(assignment.items(), key=lambda item: item[1]))
        items = assignment.items()
        for item in items:
            print(item, end = " ")
            print(find_semester(item[0], data), end = " ")
            print(find_teacher(item[0], data), end = " ")
            print(is_hard(item[0], data), end = " ")
            print(withLab(item[0], data))
            counter = counter + 1
            if(counter == timeslots):
                print("\n")
                counter = 0

    def getVar(self):
        return self.variables
    def getDomains(self):
        return self.domains



if __name__ == "__main__":
    filename = 'lessons.csv'
    # create_courses_for_labs(filename)
    data = get_rows(filename)
    timeslots = 3
    Schedule = Scheduling(data)

    assignment = dict()
    for var in Schedule.getVar():
            assignment[var] = ""

    removals = list()

    assignment = csp.backtracking_search(Schedule)
    # assignments = csp.forward_checking(Schedule, tuple(Schedule.getVar()), Schedule.getDomains, assignment, removals)
    Schedule.display(assignment, timeslots, filename)
