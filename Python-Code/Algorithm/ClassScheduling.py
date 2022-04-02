import prettytable as prettytable
import random as rnd
import sqlite3 as sqlite
from enum import Enum
# profiling
import numpy as np
import time
from memory_profiler import profile
from guppy import hpy
h = hpy()

# Population size is the number of schedules created per generation
POPULATION_SIZE = 9
# This variable will determine how many parents are left and used for the crossovers
NUMB_OF_ELITE_SCHEDULES = 1
# How many schedules will be taken from the current generation and put into the next
TOURNAMENT_SELECTION_SIZE = 3
# Compared to randomly generated numbers to determine mutations later on
MUTATION_RATE = 0.1
class Data_Base:
    def __init__(self):
        # estabish connection to created sql database
        self.conn = sqlite.connect('class_schedule.db')
        # set a variable to be your cursor to process executable commands
        self.curs = self.conn.cursor()
    def select_rooms(self):
        # select all data from the room table
        self.curs.execute("SELECT * FROM room")
        rooms = self.curs.fetchall()
        # this will be the list of rooms that is returned from the table
        returnRooms = []
        for i in range(0,len(rooms)):
            returnRooms.append(Room(rooms[i][0], rooms[i][1]))
        return returnRooms
    def select_times(self):
        self.curs.execute("SELECT * FROM meeting_time")
        meetingTimes = self.curs.fetchall()
        returnMeetingTimes = []
        for i in range(0, len(meetingTimes)):
            returnMeetingTimes.append(MeetingTime(meetingTimes[i][0], meetingTimes[i][1]))
        return returnMeetingTimes
"""
class Data:
    ##################################################
    ## Information given, convert into sql database ##
    ##################################################
    ROOMS = [["R1",25], ["R2",45], ["R3",35]]
    MEETING_TIMES = [["MT1", "MWF 8:00 - 9:15"],
                    ["MT2", "MWF 10:00 - 11:15"],
                    ["MT3", "TTR 09:00 - 10:30"],
                    ["MT4", "TTR 10:30 - 12:00"]]
    INSTRUCTORS = [["I1", "Kyle Prather"],
                ["I2", "John Cena"],
                ["I3", "Cotton EyeJoe"],
                ["I4", "The Rock"]]
    def __init__(self):
        self._rooms = []; self._meetingTimes = []; self._instructors = []
        for i in range(0, len(self.ROOMS)):
            self._rooms.append(Room(self.ROOMS[i][0], self.ROOMS[i][1]))
        for i in range(0, len(self.MEETING_TIMES)):
            self._meetingTimes.append(MeetingTime(self.MEETING_TIMES[i][0], self.MEETING_TIMES[i][1]))
        for i in range(0, len(self.INSTRUCTORS)):
            self._instructors.append(Instructor(self.INSTRUCTORS[i][0], self.INSTRUCTORS[i][1]))
        course1 = Course("C1", "330", [self._instructors[0], self._instructors[1]], 25)
        course2 = Course("C2", "405", [self._instructors[0], self._instructors[1], self._instructors[2]], 35)
        course3 = Course("C3", "406", [self._instructors[0], self._instructors[1]], 25)
        course4 = Course("C4", "450", [self._instructors[2], self._instructors[3]], 30)
        course5 = Course("C5", "222", [self._instructors[3]], 35)
        course6 = Course("C6", "101", [self._instructors[0], self._instructors[2]], 45)
        course7 = Course("C7", "654", [self._instructors[1], self._instructors[3]], 45)
        self._courses = [course1, course2, course3, course4, course5, course6, course7]
        # this is where you set what course number goes to which department
        dept1 = Department("CSC", [course1, course3])
        dept2 = Department("MATH", [course2, course4, course5])
        dept3 = Department("ENGR", [course6, course7])
        self._depts = [dept1, dept2, dept3]
        self._numberOfClasses = 0
        for i in range(0, len(self._depts)):
            self._numberOfClasses += len(self._depts[i].get_courses())
    # call your get functions into your __init__ finction
    def get_rooms(self): return self._rooms
    def get_instructors(self): return self._instructors
    def get_courses(self): return self._courses
    def get_depts(self): return self._depts
    def get_meetingTimes(self): return self._meetingTimes
    def get_numberOfClasses(self): return self._numberOfClasses
"""
# class for the scheduling section of the output. Setup for the fitness and conflict columns of your table
class Schedule:
    def __init__(self):
        self._data = data
        self._classes = []
        self._numbOfConflicts = 0
        self._fitness = -1
        self._classNumb = 0
        self._isFitnessChanged = True
    def get_classes(self):
        self._isFitnessChanged = True
        return self._classes
    def get_numbOfConflicts(self): return self._numbOfConflicts
    def get_fitness(self):
        if (self._isFitnessChanged == True):
            self._fitness = self.calculate_fitness()
            self._isFitnessChanged = False
        return self._fitness
    # this initializer set your courses and all other informtion into the scheduler section of your output
    def initialize(self):
        depts = self._data.get_depts()
        for i in range(0, len(depts)):
            courses = depts[i].get_courses()
            for j in range(0, len(courses)):
                newClass = Class(self._classNumb, depts[i], courses[j])
                self._classNumb += 1
                newClass.set_meetingTime(data.get_meetingTimes()[rnd.randrange(0, len(data.get_meetingTimes()))])
                newClass.set_room(data.get_rooms()[rnd.randrange(0, len(data.get_rooms()))])
                newClass.set_instructor(courses[j].get_instructors()[rnd.randrange(0, len(courses[j].get_instructors()))])
                self._classes.append(newClass)
        return self
    # calculates the ratio of conflicts in each current schedule. Lower ratio/fitness means more conflicts
    def calculate_fitness(self):
        self._numbOfConflicts = 0
        classes = self.get_classes()
        for i in range(0, len(classes)):
            if (classes[i].get_room().get_seatingCapacity() < classes[i].get_course().get_maxNumbOfStudents()):
                self._numbOfConflicts += 1
            for j in range(0, len(classes)):
                if (j >= i):
                    if (classes[i].get_meetingTime() == classes[j].get_meetingTime() and
                    classes[i].get_id() != classes[j].get_id()):
                        if (classes[i].get_room() == classes[j].get_room()): self._numbOfConflicts += 1
                        if (classes[i].get_instructor() == classes[j].get_instructor()): self._numbOfConflicts += 1
        return 1 / ((1.0*self._numbOfConflicts + 1))
    # string function that edits the layout of the output for the schedule section
    def __str__(self):
        returnValue = ""
        for i in range(0, len(self._classes)-1):
            returnValue += str(self._classes[i]) + ", "
        returnValue += str(self._classes[len(self._classes)-1])
        return returnValue
# this class is what populates the tables with the population size you enter at the top of the code.
class Population:
    def __init__(self, size):
        self._size = size
        self._data = data
        self._schedules = []
        for i in range(0, size): self._schedules.append(Schedule().initialize())
    def get_schedules(self): return self._schedules
# Main Genetic Agorithm used to create generations and eventually find the Elite_Schedule and stop once the desire amount is found
class Algorithm:
    # evolve function brings in the crossover population and mutates it
    def evolve(self, population): return self._mutate_population(self._crossover_population(population))
    # The corssover population function is what appends the the schedules that won the tournament of the current generation. 
    # ie. The current top Schedules with the least amount of conflicts/the highest fitness ratio
    def _crossover_population(self, pop):
        crossover_pop = Population(0)
        for i in range(NUMB_OF_ELITE_SCHEDULES):
            crossover_pop.get_schedules().append(pop.get_schedules()[i])
        i = NUMB_OF_ELITE_SCHEDULES
        while i < POPULATION_SIZE:
            schedule1 = self._select_tournament_population(pop).get_schedules()[0]
            schedule2 = self._select_tournament_population(pop).get_schedules()[0]
            crossover_pop.get_schedules().append(self._crossover_schedule(schedule1, schedule2))
            i += 1
        return crossover_pop
    # This brings in the current pop into the mutate schedule function the returns what is recieved
    def _mutate_population(self, population):
        for i in range(NUMB_OF_ELITE_SCHEDULES, POPULATION_SIZE):
            self._mutate_schedule(population.get_schedules()[i])
        return population
    # Create two random crossover points in the parent and copy the segment between them from the 
    # first parent to the first offspring. Now, starting from the second crossover point in the second 
    # parent, copy the remaining unused numbers from the second parent to the first child, wrapping around the list
    def _crossover_schedule(self, schedule1, schedule2):
        crossoverSchedule = Schedule().initialize()
        for i in range(0, len(crossoverSchedule.get_classes())):
            if (rnd.random() > 0.5): crossoverSchedule.get_classes()[i] = schedule1.get_classes()[i]
            else: crossoverSchedule.get_classes()[i] = schedule2.get_classes()[i]
        return crossoverSchedule
    # for each class in a schedule, if the random number created it smaller than the set mutation rate then than 
    # class will be mutated and returned for the next generation
    def _mutate_schedule(self, mutateSchedule):
        schedule = Schedule().initialize()
        for i in range(0, len(mutateSchedule.get_classes())):
            if(MUTATION_RATE > rnd.random()): mutateSchedule.get_classes()[i] = schedule.get_classes()[i]
        return mutateSchedule
    # This is where the schedules are chosen for the tournament of each generation
    def _select_tournament_population(self, pop):
        tournament_pop = Population(0)
        i = 0
        while i < TOURNAMENT_SELECTION_SIZE:
            tournament_pop.get_schedules().append(pop.get_schedules()[rnd.randrange(0, POPULATION_SIZE)])
            i += 1
        tournament_pop.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)
        return tournament_pop
# Course class that gets the information needed for each course
class Course:
    def __init__(self, number, name, instructors, maxNumbOfStudents):
        self._number = number
        self._name = name
        self._maxNumbOfStudents = maxNumbOfStudents
        self._instructors = instructors
    def get_number(self): return self._number
    def get_name(self): return self._name
    def get_instructors(self): return self._instructors
    def get_maxNumbOfStudents(self): return self._maxNumbOfStudents
    def __str__(self): return self._name
# Instructor class that gets the information of each instrutor
class Instructor:
    def __init__(self, id, name):
        self._id = id
        self._name = name
    def get_id(self): return self._id
    def get_name(self): return self._name
    def __str__(self): return self._name
# Room class that gets the information of each Room
class Room:
    def __init__(self, number, seatingCapacity):
        self._number = number
        self._seatingCapacity = seatingCapacity
    def get_number(self): return self._number
    def get_seatingCapacity(self): return self._seatingCapacity
# Meeting time class that gets the information of each Meeting time
class MeetingTime:
    def __init__(self, id, time):
        self._id = id
        self._time = time
    def get_id(self): return self._id
    def get_time(self): return self._time
# Department class that gets the information of each Department
class Department:
    def __init__(self, name, courses):
        self._name = name
        self._courses = courses
    def get_name(self): return self._name
    def get_courses(self): return self._courses
# Class class that gets the information of each Class
# **Note that a Class is different from a course in the sense that a class is the course along with
# the department it belongs to and all other information that comes along with that class.
# A class is the finalized item for the schedule
class Class:
    def __init__(self, id, dept, course):
        self._id = id
        self._dept = dept
        self._course = course
        self._instructor = None
        self._meetingTime = None
        self._room = None
    def get_id(self): return self._id
    def get_dept(self): return self._dept
    def get_course(self): return self._course
    def get_instructor(self): return self._instructor
    def get_meetingTime(self): return self._meetingTime
    def get_room(self): return self._room
    def set_instructor(self, instructor): self._instructor = instructor
    def set_meetingTime(self, meetingTime): self._meetingTime = meetingTime
    def set_room(self, room): self._room = room
    def __str__(self):
        return str(self._dept.get_name()) + "," + str(self._course.get_number()) + "," + \
            str(self._room.get_number()) + "," + str(self._instructor.get_id()) + "," + str(self._meetingTime.get_id())
# This function is how everything is being printed and  implemented into prettyTable using the python prettyTable library.
# This function was implemented using a previously created online source and only slightly adjusted to meet th requirments needed 
# for this source code.
class DisplayMgr:
    def print_available_data(self):
        print("> All Available Data")
        self.print_dept()
        self.print_course()
        self.print_room()
        self.print_instructor()
        self.print_meeting_times()
    def print_dept(self):
        depts = data.get_depts()
        availableDeptsTable = prettytable.PrettyTable(['dept', 'courses'])
        for i in range(0, len(depts)):
            courses = depts.__getitem__(i).get_courses()
            tempStr = "["
            for j in range(0, len(courses) - 1):
                tempStr += courses[j].__str__() + ", "
            tempStr += courses[len(courses) - 1].__str__() + "]"
            availableDeptsTable.add_row([depts.__getitem__(i).get_name(), tempStr])
        print(availableDeptsTable)
    def print_course(self):
        availableCoursesTable = prettytable.PrettyTable(['id', 'course #', 'max # of students', 'instructors'])
        courses = data.get_courses()
        for i in range(0, len(courses)):
            instructors = courses[i].get_instructors()
            tempStr = ""
            for j in range(0, len(instructors) - 1):
                tempStr += instructors[j].__str__() + ", "
            tempStr += instructors[len(instructors) - 1].__str__()
            availableCoursesTable.add_row(
                [courses[i].get_number(), courses[i].get_name(), str(courses[i].get_maxNumbOfStudents()), tempStr])
        print(availableCoursesTable)
    def print_instructor(self):
        availableInstructorsTable = prettytable.PrettyTable(['id', 'instructor'])
        instructors = data.get_instructors()
        for i in range(0, len(instructors)):
            availableInstructorsTable.add_row([instructors[i].get_id(), instructors[i].get_name()])
        print(availableInstructorsTable)
    def print_room(self):
        availableRoomsTable = prettytable.PrettyTable(['room #', 'max seating capacity'])
        rooms = data.get_rooms()
        for i in range(0, len(rooms)):
            availableRoomsTable.add_row([str(rooms[i].get_number()), str(rooms[i].get_seatingCapacity())])
        print(availableRoomsTable)
    def print_meeting_times(self):
        availableMeetingTimeTable = prettytable.PrettyTable(['id', 'Meeting Time'])
        meetingTimes = data.get_meetingTimes()
        for i in range(0, len(meetingTimes)):
            availableMeetingTimeTable.add_row([meetingTimes[i].get_id(), meetingTimes[i].get_time()])
        print(availableMeetingTimeTable)
    def print_generation(self, population):
        table1 = prettytable.PrettyTable(['schedule #', 'fitness', '# of conflicts', 'classes [dept,class,room,instructor,meeting-time]'])
        schedules = population.get_schedules()
        for i in range(0, len(schedules)):
            table1.add_row([str(i), round(schedules[i].get_fitness(),3), schedules[i].get_numbOfConflicts(), schedules[i].__str__()])
        print(table1)
    def print_schedule_as_table(self, schedule):
        classes = schedule.get_classes()
        table = prettytable.PrettyTable(['Class #', 'Dept', 'Course (number, max # of students)', 'Room (Capacity)', 'Instructor (Id)',  'Meeting Time (Id)'])
        for i in range(0, len(classes)):
            table.add_row([str(i), classes[i].get_dept().get_name(), classes[i].get_course().get_name() + " (" +
                        classes[i].get_course().get_number() + ", " +
                        str(classes[i].get_course().get_maxNumbOfStudents()) +")",
                        classes[i].get_room().get_number() + " (" + str(classes[i].get_room().get_seatingCapacity()) + ")",
                        classes[i].get_instructor().get_name() +" (" + str(classes[i].get_instructor().get_id()) +")",
                        classes[i].get_meetingTime().get_time() +" (" + str(classes[i].get_meetingTime().get_id()) +")"])
        print(table)
# Runs the code for each generation
data = Data()
displayMgr = DisplayMgr()
displayMgr.print_available_data()
# start at generation 0
generationNumber = 0
print("\n> Generation # "+str(generationNumber))
# populate the table
population = Population(POPULATION_SIZE)
population.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)
# display current generation
displayMgr.print_generation(population)
displayMgr.print_schedule_as_table(population.get_schedules()[0])
# run algorithm to adjust and mutate current generation for next generation
algorithm = Algorithm()
#adjust and continues above code util a schedule with 0 conflicts/fitnes of 1.0 is found
while (population.get_schedules()[0].get_fitness() != 1.0):
    generationNumber += 1
    print("\n> Generation # " + str(generationNumber))
    population = algorithm.evolve(population)
    population.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)
    displayMgr.print_generation(population)
    displayMgr.print_schedule_as_table(population.get_schedules()[0])
print("\n\n")

# used for profiling
h.heap()