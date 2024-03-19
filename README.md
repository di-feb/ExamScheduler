# Scheduling

The project is part of the course "Artificial Intelligence" at the Department of Informatics and Telecommunications, University of Athens. The purpose of the project is to implement a scheduling application for the winter exam schedule of the Department of Informatics and Telecommunications (DIT) at the University of Athens (UoA). The application uses constraint satisfaction problem (CSP) techniques to generate a schedule that meets various constraints.

The project utilizes several Python files:

- `utils.py`: This file contains utility functions that assist in the scheduling process.
- `search.py`: This file includes search algorithms that are used to find a solution that satisfies all constraints.
- `csp.py`: This file defines the structure and methods of a constraint satisfaction problem, which is the core of the scheduling application.

**The main functionality of the application** is encapsulated in the `scheduling.py` file.  
This file contains the Scheduling class, which is a subclass of the CSP class defined in csp.py.  
The Scheduling class models the scheduling problem and uses the utility functions and search algorithms to generate a valid exam schedule.

## Methods Used

The application uses different methods to solve the scheduling problem, such as:  

- `minimum remaining values (mrv)`  
- `least constraining value (lcv)`  
- `forward checking (fc)`  
- `maintaining arc consistency(mac)`
- `domain/weight degree (domWdeg)`  
- `min conflicts`

The execution times of these methods are recorded and can be viewed **below**.

## Constraints

The constraints of the scheduling problem are:

- Two variables cannot have the same value.
- Courses of the same semester cannot be on the same day.
- Courses of the same teacher cannot be on the same day.
- Two hard courses must have at least one day off between them.
- A lab course cannot be placed in the third hour.
- If the course has a lab, reserve the next hour to place the lab of the specific course.  

## Project Files

- `lessons.csv`: Contains information about the winter semester courses.
- `scheduling.py`: Contains the Scheduling class, a subclass of csp.py.  
This class models the constraint satisfaction problem for solving the winter exam schedule of `DIT, UoA` based on specific constraints defined in the exercise.  
The main function is located within scheduling.py.

## Execution

You can call the backtracking function in different ways, which are commented out in the code.  
Uncomment and run whichever you prefer.  
The executable is run with the command: `python3 scheduling.py`.

## Statistics

Execution times for the backtracking function with different arguments:

| Method | Execution Time |
| --- | --- |
| Default arguments | 3.97s |
| mrv, unordered_domain_values, no inference | 3.56s |
| mrv, lcv, no inference | 7.14s |
| mrv, lcv, fc | 8.06s |
| mrv, lcv, mac | 164.50s |
| domWdeg, unordered_domain_values, no inference | 3.87s |
| domWdeg, lcv, no inference | 7.14s |
| domWdeg, lcv, fc | 8.06s |
| domWdeg, lcv, mac | 124.50s |
| min_conflicts | 7.19s |

## Observations

Generally, using inference methods like Forward Checking (FC) and Maintaining Arc Consistency (MAC) results in increased execution time. These methods try to preemptively eliminate conflicts, which can be computationally expensive. However, in this problem, the range of days is large and the conflicts are relatively few, making the overhead of these inference methods less beneficial. It is more convenient to do backtracking normally as it is not needed very often.

Regarding the heuristics Minimum Remaining Values (MRV) and Degree of Constraint (dom/wdeg), the conflicts are very few, so the extra work for the selection of the "most suitable for each function variable" is almost not worth it. These heuristics are designed to prioritize variables that are likely to cause conflicts, but the relatively low conflict rate in this problem may reduce their effectiveness.

The Least Constraining Value (LCV) heuristic, when used without inference, seems to have a noticeable impact on execution time, making it longer than using MRV or dom/wdeg with unordered domain values. This suggests that the process of ordering values in terms of least constraint can be time-consuming in this context.

The min_conflicts method, which iteratively selects the variable with the least conflicts and changes its value, shows competitive results. This method might be effective in this problem because it can quickly find a good initial state and make minor adjustments to reach a solution. It presents very good results, probably because there are many days and once it finds a good initial state and places values, it will not need to make many changes to bring the problem to a correct state.

However, the fastest method appears to be using MRV with unordered domain values and no inference, suggesting that in this problem, a simple heuristic without inference can be more efficient.

## Output Format Explanation

The output of the backtracking algorithm is a list of tuples, each representing a course. Here's a breakdown of the tuple elements:

- **Course Name**: This is a string representing the name of the course. For example, `'Linear Algebra'`.

- **Tuple (Day, Shift)**: This is a tuple of two integers. The first integer represents the day of the course (1 for the first day, 2 for the second day, etc.). The second integer represents the 3-hour shift of the course on that day (1 for the first shift, 2 for the second shift, etc.). For example, `(1, 1)` means the course is on the first day during the first shift.

- **Semester Number**: This is an integer representing the semester number. For example, `1` for the first semester, `3` for the third semester, etc.

- **Professor's Name**: This is a string representing the name of the professor teaching the course. For example, `'GIANNOPULOU'`.

- **Difficulty**: This is a boolean value indicating whether the course is difficult. `True` means the course is difficult, and `False` means it is not.

- **Laboratory Component**: This is a boolean value indicating whether the course has a laboratory component. `True` means the course has a lab, and `False` means it does not.

Here's an example of a course tuple:

```python
('Linear Algebra', (1, 1)) 1 GIANNOPULOU True False
```

This represents a course named 'Linear Algebra', taking place on the first day during the first shift,  
in the first semester, taught by a professor named 'GIANNOPULOU'.  
The course is marked as difficult (True) and does not have a laboratory component (False).  
  