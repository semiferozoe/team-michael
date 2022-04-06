from re import I
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
VERBOSE_FLAG = False
class Data_Base:
    def __init__(self):
        # estabish connection to created sql database
        self._conn = sqlite.connect('class_schedule.db')
        # set a variable to be your cursor to process executable commands
        self._curs = self._conn.cursor()

        self._rooms = self.select_rooms()
        self._meetingTimes = self.select_times()
        self._instructors = self.select_instructor()
        self._courses = self.select_courses()
        self._depts = self.select_depts()
        self._numberofClasses = 0
        for i in range(0, len(self._depts)):
            self._numberofClasses += len(self._depts[i].get_courses())
    ##################################################################################
    def select_rooms(self):
        # select all data from the room table
        self._curs.execute("SELECT * FROM room")
        rooms = self._curs.fetchall()
        # this will be the list of rooms that is returned from the table
        returnRooms = []
        for i in range(0,len(rooms)):
            returnRooms.append(Room(rooms[i][0], rooms[i][1]))
        return returnRooms
    def select_times(self):
        self._curs.execute("SELECT * FROM meeting_time")
        meetingTimes = self._curs.fetchall()
        returnMeetingTimes = []
        for i in range(0, len(meetingTimes)):
            returnMeetingTimes.append(MeetingTime(meetingTimes[i][0], meetingTimes[i][1]))
        return returnMeetingTimes
    def select_instructor(self):
        self._curs.execute("SELECT * FROM instructor")
        instructors = self._curs.fetchall()
        returnInstructors = []
        for i in range(0, len(instructors)):
            returnInstructors.append(Instructor(instructors[i][0], instructors[i][1], self.select_availability(instructors[i][0])))
        return returnInstructors
    def select_availability(self, instructor):
        self._curs.execute("SELECT * FROM instructor_availability where instructor_id = '" + instructor + "'")
        instructorTimeRoom = self._curs.fetchall()
        instructorTR = []
        for i in range(0, len(instructorTimeRoom)):
            instructorTR.append(instructorTimeRoom[i][1])
        returnAvailability = list()
        for i in range(0, len(self._meetingTimes)):
            if self._meetingTimes[i].get_id() in instructorTR:
                returnAvailability.append(self._meetingTimes[i])
        return returnAvailability
    def select_courses(self):
        self._curs.execute("SELECT * FROM course")
        courses = self._curs.fetchall()
        returnCourses = []
        for i in range(0, len(courses)):
            returnCourses.append(
                Course(courses[i][0], courses[i][1], self.select_course_instructors(courses[i][0]), courses[i][2]))
        return returnCourses
    def select_depts(self):
        self._curs.execute("SELECT * FROM dept")
        depts = self._curs.fetchall()
        returnDepts = []
        for i in range(0, len(depts)):
            returnDepts.append(Department(depts[i][0], self.select_dept_courses(depts[i][0])))
        return returnDepts
    def select_course_instructors(self, courseNumber):
        self._curs.execute("SELECT * FROM course_instructor where course_number == '" + courseNumber + "'")
        dbInstructorNumbers = self._curs.fetchall()
        instructorNumbers = []
        for i in range(0, len(dbInstructorNumbers)):
            instructorNumbers.append(dbInstructorNumbers[i][1])
        returnValue = []
        for i in range(0, len(self._instructors)):
           if  self._instructors[i].get_id() in instructorNumbers:
               returnValue.append(self._instructors[i])
        return returnValue
    def select_dept_courses(self, deptName):
        self._curs.execute("SELECT * FROM dept_course where name == '" + deptName + "'")
        dbCourseNumbers = self._curs.fetchall()
        courseNumbers = []
        for i in range(0, len(dbCourseNumbers)):
            courseNumbers.append(dbCourseNumbers[i][1])
        returnValue = []
        for i in range(0, len(self._courses)):
           if self._courses[i].get_number() in courseNumbers:
               returnValue.append(self._courses[i])
        return returnValue
    
    def get_rooms(self): return self._rooms
    def get_instructors(self): return self._instructors
    def get_courses(self): return self._courses
    def get_depts(self): return self._depts
    def get_meetingTimes(self): return self._meetingTimes
    def get_numberofClasses(self): return self._numberofClasses        
# class for the scheduling section of the output. Setup for the fitness and conflict columns of your table
class Schedule:
    def __init__(self):
        self._data = db
        self._classes = []
        self._numbOfConflicts = 0
        self._fitness = -1
        self._classNumb = 0
        self._isFitnessChanged = True
    def get_classes(self):
        self._isFitnessChanged = True
        return self._classes
    def get_numbOfConflicts(self):
         return self._numbOfConflicts
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
                newClass.set_meetingTime(db.get_meetingTimes()[rnd.randrange(0, len(db.get_meetingTimes()))])
                newClass.set_room(db.get_rooms()[rnd.randrange(0, len(db.get_rooms()))])
                newClass.set_instructor(courses[j].get_instructors()[rnd.randrange(0, len(courses[j].get_instructors()))])
                self._classes.append(newClass)
        return self
    # calculates the ratio of conflicts in each current schedule. Lower ratio/fitness means more conflicts
    def calculate_fitness(self):
       self._conflicts = []
       classes = self.get_classes()
       for i in range(0, len(classes)):
           seatingCapacityConflict = list()
           seatingCapacityConflict.append(classes[i])
           if (classes[i].get_room().get_seatingCapacity() < classes[i].get_course().get_maxNumbOfStudents()):
               self._conflicts.append(Conflict(Conflict.ConflictType.NUMB_OF_STUDENTS, seatingCapacityConflict))
           if (classes[i].get_meetingTime() not in classes[i].get_instructor().get_availability()):
               conflictBetweenClasses = list()
               conflictBetweenClasses.append(classes[i])
               self._conflicts.append(Conflict(Conflict.ConflictType.INSTRUCTOR_AVAILABILITY, conflictBetweenClasses))
           for j in range(0, len(classes)):
               if (j >= i):
                   if (classes[i].get_meetingTime() == classes[j].get_meetingTime() and
                   classes[i].get_id() != classes[j].get_id()):
                       if (classes[i].get_room() == classes[j].get_room()):
                           roomBookingConflict = list()
                           roomBookingConflict.append(classes[i])
                           roomBookingConflict.append(classes[j])
                           self._conflicts.append(Conflict(Conflict.ConflictType.ROOM_BOOKING, roomBookingConflict))
                       if (classes[i].get_instructor() == classes[j].get_instructor()):
                           instructorBookingConflict = list()
                           instructorBookingConflict.append(classes[i])
                           instructorBookingConflict.append(classes[j])
                           self._conflicts.append(Conflict(Conflict.ConflictType.INSTRUCTOR_BOOKING, instructorBookingConflict))
       return 1 / ((1.0 * len(self._conflicts) + 1))
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
        self._data = db
        self._schedules = []
        for i in range(0, size): self._schedules.append(Schedule().initialize())
    def get_schedules(self): return self._schedules
# Main Genetic Agorithm used to create generations and eventually find a schedule with no and stop once the desire amount is found
class Algorithm:
    # evolve function brings in the crossover population and mutates it
    def evolve(self, population): return self._mutate_population(self._crossover_population(population))
    # The corssover population function is what appends the the schedules that won the tournament of the current 
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
    def __init__(self, id, name, availability):
        self._id = id
        self._name = name
        self._availability = availability
    def get_id(self): return self._id
    def get_name(self): return self._name
    def get_availability(self): return self._availability
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
class Conflict:
    class ConflictType(Enum):
        INSTRUCTOR_BOOKING = 1
        ROOM_BOOKING = 2
        NUMB_OF_STUDENTS = 3
        INSTRUCTOR_AVAILABILITY = 4
    def __init__(self, conflictType, conflictBetweenClasses):
        self._conflictType = conflictType
        self._conflictBetweenClasses = conflictBetweenClasses
    def get_conflictType(self): return self._conflictType
    def get_conflictBetweenClasses(self): return self._conflictBetweenClasses
    def __str__(self): return str(self._conflictType)+" "+str(" and ".join(map(str, self._conflictBetweenClasses)))
# This function is how everything is being printed and  implemented into prettyTable using the python prettyTable library.
# This function was implemented using a previously created online source and only slightly adjusted to meet th requirments needed 
# for this source code.
class DisplayMgr:
    @staticmethod
    def display_input_data():
        print("> All Available Data")
        DisplayMgr.display_dept()
        DisplayMgr.display_course()
        DisplayMgr.display_room()
        DisplayMgr.display_instructor()
        DisplayMgr.display_meeting_times()
    @staticmethod
    def display_dept():
        depts = db.get_depts()
        availableDeptsTable = prettytable.PrettyTable(['dept', 'courses'])
        for i in range(0, len(depts)):
            courses = depts.__getitem__(i).get_courses()
            tempStr = "["
            for j in range(0, len(courses) - 1):
                tempStr += courses[j].__str__() + ", "
            tempStr += courses[len(courses) - 1].__str__() + "]"
            availableDeptsTable.add_row([depts.__getitem__(i).get_name(), tempStr])
        print(availableDeptsTable)
    @staticmethod
    def display_course():
        availableCoursesTable = prettytable.PrettyTable(['id', 'course #', 'max # of students', 'instructors'])
        courses = db.get_courses()
        for i in range(0, len(courses)):
            instructors = courses[i].get_instructors()
            tempStr = ""
            for j in range(0, len(instructors) - 1):
                tempStr += instructors[j].__str__() + ", "
            tempStr += instructors[len(instructors) - 1].__str__()
            availableCoursesTable.add_row(
                [courses[i].get_number(), courses[i].get_name(), str(courses[i].get_maxNumbOfStudents()), tempStr])
        print(availableCoursesTable)
    @staticmethod
    def display_instructor():
        availableInstructorsTable = prettytable.PrettyTable(['id', 'instructor', 'availability'])
        instructors = db.get_instructors()
        for i in range(0, len(instructors)):
            availability = []
            for j in range(0, len(instructors[i].get_availability())):
                availability.append(instructors[i].get_availability()[j].get_id())
            availableInstructorsTable.add_row([instructors[i].get_id(),instructors[i].get_name(), availability])
        print(availableInstructorsTable)
    @staticmethod
    def display_room():
        availableRoomsTable = prettytable.PrettyTable(['room #', 'max seating capacity'])
        rooms = db.get_rooms()
        for i in range(0, len(rooms)):
            availableRoomsTable.add_row([str(rooms[i].get_number()), str(rooms[i].get_seatingCapacity())])
        print(availableRoomsTable)
    @staticmethod
    def display_meeting_times():
        availableMeetingTimeTable = prettytable.PrettyTable(['id', 'Meeting Time'])
        meetingTimes = db.get_meetingTimes()
        for i in range(0, len(meetingTimes)):
            availableMeetingTimeTable.add_row([meetingTimes[i].get_id(), meetingTimes[i].get_time()])
        print(availableMeetingTimeTable)
    @staticmethod
    def display_generation(population):
        table1 = prettytable.PrettyTable(['schedule #', 'fitness', '# of conflicts', 'classes [dept,class,room,instructor,meeting-time]'])
        schedules = population.get_schedules()
        for i in range(0, len(schedules)):
            table1.add_row([str(i+1), round(schedules[i].get_fitness(),3), len(schedules[i].get_conflicts()), schedules[i].__str__()])
        print(table1)
    @staticmethod
    def display_schedule_as_table(schedule):
        classes = schedule.get_classes()
        table = prettytable.PrettyTable(['Class #', 'Dept', 'Course (number, max # of students)', 'Room (Capacity)', 'Instructor (Id)',  'Meeting Time (Id)'])
        for i in range(0, len(classes)):
            table.add_row([str(i+1), classes[i].get_dept().get_name(), classes[i].get_course().get_name() + " (" +
                           classes[i].get_course().get_number() + ", " +
                           str(classes[i].get_course().get_maxNumbOfStudents()) +")",
                           classes[i].get_room().get_number() + " (" + str(classes[i].get_room().get_seatingCapacity()) + ")",
                           classes[i].get_instructor().get_name() +" (" + str(classes[i].get_instructor().get_id()) +")",
                           classes[i].get_meetingTime().get_time() +" (" + str(classes[i].get_meetingTime().get_id()) +")"])
        print(table)
    @staticmethod
    def display_schedule_meetingTimes(schedule):
        print("> from 'meeting time' perspective")
        meetingTimesTable = prettytable.PrettyTable(['id', 'meeting time', 'classes [dept,class,room,instructor,meeting-time] '])
        meetingTimes = db.get_meetingTimes()
        for i in range(0, len(meetingTimes)):
            classes = list()
            for j in range(0, len(schedule.get_classes())):
                if schedule.get_classes()[j].get_meetingTime() == meetingTimes[i]:
                    classes.append(str(schedule.get_classes()[j]))
            meetingTimesTable.add_row([meetingTimes[i].get_id(), meetingTimes[i].get_time(), str(classes)])
        print(meetingTimesTable)
    @staticmethod
    def display_schedule_rooms(schedule):
        print("> from 'room' perspective")
        scheduleRoomsTable = prettytable.PrettyTable(['room','classes [dept,class,room,instructor,meeting-time] '])
        rooms = db.get_rooms()
        for i in range(0, len(rooms)):
            roomSchedule = list()
            for j in range(0, len(schedule.get_classes())):
                if schedule.get_classes()[j].get_room() == rooms[i]:
                    roomSchedule.append(str(schedule.get_classes()[j]))
            scheduleRoomsTable.add_row([str(rooms[i].get_number()), str(roomSchedule)])
        print(scheduleRoomsTable)
    @staticmethod
    def display_schedule_instructors(schedule):
        print("> from 'instructor' perspective")
        instructorsTable = prettytable.PrettyTable(['id', 'instructor', "classes [dept,class,room,instructor,meeting-time]",'availability'])
        instructors = db.get_instructors()
        for i in range(0, len(instructors)):
            availability = []
            for j in range(0, len(instructors[i].get_availability())):
                availability.append(instructors[i].get_availability()[j].get_id())
            classSchedule = list()
            for j in range(0, len(schedule.get_classes())):
                if schedule.get_classes()[j].get_instructor() == instructors[i]:
                    classSchedule.append(str(schedule.get_classes()[j]))
            instructorsTable.add_row([instructors[i].get_id(), instructors[i].get_name(), str(classSchedule), availability])
        print(instructorsTable)
    @staticmethod
    def display_schedule_conflicts(schedule):
        conflictsTable = prettytable.PrettyTable(['conflict type', 'conflict between classes'])
        conflicts = schedule.get_conflicts()
        for i in range(0, len(conflicts)):
            conflictsTable.add_row([str(conflicts[i].get_conflictType()),
                                    str("  and  ".join(map(str, conflicts[i].get_conflictBetweenClasses())))])
        if (len(conflicts) > 0): print(conflictsTable)
def find_fittest_schedule(verboseFlag):
    generationNumber = 0
    if (verboseFlag): print("> Generation # "+str(generationNumber))
    population = Population(POPULATION_SIZE)
    population.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)
    if (verboseFlag):
        DisplayMgr.display_generation(population)
        DisplayMgr.display_schedule_as_table(population.get_schedules()[0])
        DisplayMgr.display_schedule_conflicts(population.get_schedules()[0])
    algorithm = Algorithm()
    while (population.get_schedules()[0].get_fitness() != 1.0):
        generationNumber += 1
        if (verboseFlag): print("\n> Generation # " + str(generationNumber))
        population = algorithm.evolve(population)
        population.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)
        if (verboseFlag):
            DisplayMgr.display_generation(population)
            DisplayMgr.display_schedule_as_table(population.get_schedules()[0])
            DisplayMgr.display_schedule_conflicts(population.get_schedules()[0])
    print("> solution found after " + str(generationNumber) + " generations")
    return population.get_schedules()[0]
def handle_command_line(verboseFlag):
    while (True):
        entry = input("> What do you want to do (i:nitial data display, f:ind fittest schedule, d:efault mode, v:erbose mode, e:xit)\n")
        if (entry == "i"): DisplayMgr.display_input_data()
        elif (entry == "f"):
            schedule = find_fittest_schedule(verboseFlag)
            handle_schedule_display(schedule)
        elif (entry == "d"): verboseFlag = False
        elif (entry == "v"): verboseFlag = True
        elif (entry == "e"): break
def handle_schedule_display(schedule):
    while (True):
        entry = input("> What do you want to display (c:lass schedule, t:ime schedule, r:oom schedule, i:nstructor schedule, e:lse)\n")
        if (entry == "c"):
            print("> from 'class' perspective")
            DisplayMgr.display_schedule_as_table(schedule)
        elif (entry == "t"): DisplayMgr.display_schedule_meetingTimes(schedule)
        elif (entry == "r"): DisplayMgr.display_schedule_rooms(schedule);
        elif (entry == "i"): DisplayMgr.display_schedule_instructors(schedule);
        elif (entry == "e"): break
db = Data_Base()
handle_command_line(VERBOSE_FLAG)
# used for profiling
h.heap()