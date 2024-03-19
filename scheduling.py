import csv
import time
import csp

# Finds the days and hours that have been reserved for the courses that have labs
# and places the lab of each such course the next three hours the same day
def insertLabs(assignment, data):
    for row in data:
        if row[4] == "TRUE":
            value = assignment[row[1]]
            assignment[row[1] + "_lab"] = (value[0], value[1] + 1)
            data.append([row[0], row[1] + "_lab", row[2], "FALSE", "FALSE"])

# Implementation of dom/wdeg
def domWdeg(assignment, csp):
    filename = 'lessons.csv'
    data = get_rows(filename)

    res = dict()

    # Initialization of the dict
    for var in csp.variables:
        res[var] = 1
    
    for var in csp.variables:
        for neigh in csp.neighbors[var]:
            if (neigh not in assignment):
                res[var] += csp.weight[(var, neigh)]
        res[var]  =  res[var] / len(csp.domains[var])

    result = min(res, key=res.get)

    return result

# Returns the information of the csv file
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

# Writes in the csv file the labs as separate courses
# (was not used)
def create_courses_for_labs(filename):
    file =  open(filename, mode="r+", encoding="UTF8")
    csvwriter = csv.writer(file) 
    reader = csv.reader(file)
    lab = list()
    for row in reader:
        if row[4] == "TRUE":
            lab.append([row[0], row[1] + "_lab", row[2], "FALSE", "FALSE"])
    csvwriter.writerows(lab)

    file.close()

# Returns the names of the courses (Variables for Scheduling)
def getCourses(data):
    courses = list()
    for row in data:
        courses.append(row[1])
    return courses

# Finds the semester in which the _course_ is taught
def find_semester(course, data):
    for row in data:
        if row[1] == course:
            return row[0]
    return 0

# If a course is hard it returns true
def is_hard(course, data):
    for row in data:
        if row[1] == course:
            if row[3] == "TRUE":
                return True
    return False

# Finds the teacher of a specific course
def find_teacher(course, data):  
    for row in data:
        if row[1] == course:
            return row[2]
    return 0

# If a course has a lab it returns true
def withLab(course, data):
    for row in data:
        if row[1] == course:
            if row[4] == "TRUE":
                return True
    return False

# If a course is a lab it returns true
# (was not used)
def isLab(course, data):
    for row in data:
        if row[1] == course:
            if course[-4:] == "_lab":
                return True
    return False

class Scheduling(csp.CSP):

    def __init__(self, data):
        """Initialize data structures for Scheduling."""
        timeslots = 3
        days = 21
        self.variables = list()
        self.values = list()
        self.domains = dict()
        self.neighbors = dict()
        self.weight = dict()

        # Create the values
        for i in range(1, days + 1):
            for j in range(1, timeslots + 1):
                self.values.append((i,j))

        # Create the variables
        self.variables = getCourses(data)

        # Create the domains
        for var in self.variables:
            self.domains[var] = self.values

        # Create the neighbors
        for var in self.variables:
            self.neighbors[var] = [] 
            for var2 in self.variables:
                if var != var2:
                    self.neighbors[var].append(var2)

        # Create the weights for all pairs (var, neighbor) for each neighbor of var
        # and initialize them to 1
        for var in self.variables:
            for neigh in self.neighbors[var]:
                self.weight[(var, neigh)] = 1
                
        # Define the csp
        csp.CSP.__init__(self, self.variables, self.domains, self.neighbors, self.schedule_constraint)

    # Constraint function
    def schedule_constraint(self, A, a, B, b):
        filename = "lessons.csv"
        data = get_rows(filename)
        

        # Two variables cannot have the same value
        if(A == B and (a != b)):
            return False

        if(A != B and (a == b)):
            return False

        # Courses of the same semester cannot be on the same day.
        if(a[0] == b[0] and find_semester(A, data) == find_semester(B, data)):
            return False

        # Courses of the same teacher cannot be on the same day.
        if(a[0] == b[0] and find_teacher(A, data) == find_teacher(B, data)):
            return False
        # Two hard courses must have at least one day off between them.
        if(is_hard(A, data) and is_hard(B, data) and abs(a[0] - b[0]) < 2):
            return False
        # A lab course cannot be placed in the third hour.
        if((withLab(A, data) and a[1] == 3 ) or (withLab(B, data) and b[1] == 3) ):
            return False
        
        # If the course has a lab, reserve the next hour to place
        # the lab of the specific course.
        if(withLab(A, data) and ((a[1] + 1) == b[1]) and (a[0] == b[0])):
            return False
        
        if(withLab(B, data) and (b[1] + 1) == a[1] and (a[0] == b[0])):
            return False
        
        return True

    # Prints the created schedule (not per day) in the form:
    # ('Course', Day-Hour(First, Second, Third)) Semester, Teacher, Hard, Lab
    def display(self, assignment, timeslots, data):

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

if __name__ == "__main__":
    filename = 'lessons.csv'
    data = get_rows(filename)

    Schedule = Scheduling(data)
    removals = list()

    print("Backtracking Algorithm")

    begin = time.time()

    assignment = csp.backtracking_search(Schedule)
    # assignment = csp.backtracking_search(Schedule, csp.mrv)
    # assignment = csp.backtracking_search(Schedule, csp.mrv, csp.lcv)
    # assignment = csp.backtracking_search(Schedule, csp.mrv, csp.lcv, csp.forward_checking)
    # assignment = csp.backtracking_search(Schedule, csp.mrv, csp.lcv, csp.mac)
    # assignment = csp.min_conflicts(Schedule)
    # assignment = csp.backtracking_search(Schedule, domWdeg)
    # assignment = csp.backtracking_search(Schedule, domWdeg, csp.lcv)
    # assignment = csp.backtracking_search(Schedule, domWdeg, csp.lcv, csp.forward_checking)
    # assignment = csp.backtracking_search(Schedule, domWdeg, csp.lcv, csp.mac)

    end = time.time()

    insertLabs(assignment, data)
    timeslots = 3
    Schedule.display(assignment, timeslots, data)
    print("Total time is: " + str(end - begin))
