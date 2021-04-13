import prettytable as prettytable
import random as rnd

POPULATION_SIZE = 9
NUMB_OF_ELITE_SCHEDULES = 1
TOURNAMENT_SELECTION_SIZE = 3
MUTATION_RATE= 0.1
class Data:
    ROOMS = [["R1", 20], ["R2", 15], ["R3", 22], ["R4", 22], ["R5", 15]]
    INSTRUCTORS = [["I1", "Le Thi An"], ["I2", "Nguyen Binh"], ["I3", "Dang Van DUng"], ["I4", "Nguyen van Hoang"]]
    MEETING_TIMES = [["MT1", "HTS 8:00 10:00"], ["MT2", "HTS 10:00 12:00"], ["MT3", "BN 8:00 10:00"], ["MT4", "BN 10:00 12:00"]]

    def __init__(self):
        self._rooms = []
        self._instructors = []
        self._meetingTimes = []
        for i in range(0, len(self.ROOMS)):
            self._rooms.append(Room(self.ROOMS[i][0], self.ROOMS[i][1]))
        for i in range(0, len(self.INSTRUCTORS)):
            self._instructors.append(Instructor(self.INSTRUCTORS[i][0], self.INSTRUCTORS[i][1]))
        for i in range(0, len(self.MEETING_TIMES)):
         	self._meetingTimes.append(MeetingTime(self.MEETING_TIMES[i][0], self.MEETING_TIMES[i][1]))
        course1 = Course("C1", "SL1", [self._instructors[0], self._instructors[1]], 20)
        course2 = Course("C2", "SL2", [self._instructors[0], self._instructors[1], self._instructors[2]], 12)
        course3 = Course("C3", "SL3", [self._instructors[1], self._instructors[2], self._instructors[3]], 12)
        course4 = Course("C4", "SL4", [self._instructors[0], self._instructors[3]], 20)
        course5 = Course("C5", "WR1", [self._instructors[2], self._instructors[3]], 22)
        course6 = Course("C6", "WR2", [self._instructors[0], self._instructors[1]], 22)
        course7 = Course("C7", "WR3", [self._instructors[2], self._instructors[3]], 22)
        self._courses = [course1, course2, course3, course4, course5, course6, course7]
        dept1 = Department("IE1", [course1, course5])
        dept2 = Department("IE2", [course2, course3, course6])
        dept3 = Department("IE3", [course4, course7])
        self._depts = [dept1, dept2, dept3]
        self._numberOfClasses = 0
        for i in range(0, len(self._depts)):
            self._numberOfClasses += len(self._depts[i].get_courses())

    def get_rooms(self):
        return self._rooms

    def get_instructors(self):
        return self._instructors

    def get_courses(self):
        return self._courses

    def get_depts(self):
        return self._depts

    def get_meetingTimes(self):
    	return self._meetingTimes

    def get_numberOfClasses(self):
        return self._numberOfClasses
class Schedule:
    def __init__(self):
        self._data = data
        self._classes = []
        self._numberOfConflicts = 0
        self._fitness = -1
        self._classNumb = 0
        self._isFitnessChanged = True

    def get_classes(self):
        self._isFitnessChanged = True
        return self._classes

    def get_numberOfConflicts(self):
        return self._numberOfConflicts

    def get_fitness(self):
        if (self._isFitnessChanged == True):
            self._fitness = self.caculate_finess
            self._isFitnessChanged = False
        return self._fitness

    def initialize(self):
        depts = self._data.get_depts()
        for i in range(0, len(depts)):
            courses = depts[i].get_courses()
            for j in range(0, len(courses)):
                newClass = Class(self._classNumb, depts[i], courses[j])
                self._classNumb += 1
                newClass.set_meetingTime(data.get_meetingTimes()[rnd.randrange(0, len(data.get_meetingTimes()))])
                newClass.set_room(data.get_rooms()[rnd.randrange(0, len(data.get_rooms()))])
                newClass.set_instructor(data.get_instructors()[rnd.randrange(0, len(courses[j].get_instructors()))])
                self._classes.append(newClass)
        return self

    @property
    def caculate_finess(self):
        self._numberOfConflicts = 0
        classes = self.get_classes()
        for i in range(0, len(classes)):
            if (classes[i].get_room().get_seatingcapacity() < classes[i].get_course().get_maxNumbOfStudents()):
                self._numberOfConflicts += 1
            for j in range(0, len(classes)):
                if (j >= i):
                    if(classes[i].get_meetingTime() == classes[j].get_meetingTime() and classes[i].get_idClass() != classes[j].get_idClass()):
                        if(classes[i].get_room() == classes[j].get_room()):
                            self._numberOfConflicts += 1
                        if(classes[i].get_instructor() == classes[j].get_instructor()):
                            self._numberOfConflicts += 1
        return 1 / (1.0 * self._numberOfConflicts + 1)

    def __str__(self):
        returnValue = ""
        for i in range(0, len(self._classes) - 1):
            returnValue += str(self._classes[i]) + ","
        returnValue += str(self._classes[len(self._classes) - 1])
        return returnValue
class Population:
    def __init__(self, size):
        self._size = size
        self._data = data
        self._schedules = []
        for i in range(0, size):
            self._schedules.append(Schedule().initialize())

    def get_schedules(self): return self._schedules


class Ga:
	def envolve(self, population):return self._mutate_population(self._crossover_population(population))
	def _crossover_population(self, pop): #lai tao
		crossover_pop= Population(0)
		for i in range(NUMB_OF_ELITE_SCHEDULES):
			crossover_pop.get_schedules().append(pop.get_schedules()[i])
		i = NUMB_OF_ELITE_SCHEDULES
		while i< POPULATION_SIZE:
			schedule1 =self._select_tournament_population(pop).get_schedules()[0]
			schedule2 =self._select_tournament_population(pop).get_schedules()[0]
			crossover_pop.get_schedules().append(self._crossover_schedule(schedule1, schedule2))
			i+=1
		return crossover_pop

	def _mutate_population(self, population): #dot bien
		for i in range(NUMB_OF_ELITE_SCHEDULES,POPULATION_SIZE): 
			self._mutate_schedule(population.get_schedules()[i])
		return population
	def _crossover_schedule(self, schedule1, schedule2):
		crossoverSchedule =Schedule().initialize()
		for i in range(0,len(crossoverSchedule.get_classes())):
			if(rnd.random() > 0.5): crossoverSchedule.get_classes()[i] = schedule1.get_classes()[i]
			else:crossoverSchedule.get_classes()[i] = schedule2.get_classes()[i]
		return crossoverSchedule
	def _mutate_schedule(self, mutateSchedule):
		schedule = Schedule().initialize()
		for i in range(0, len(mutateSchedule.get_classes())):
			if (MUTATION_RATE > rnd.random()):
				mutateSchedule.get_classes()[i] = schedule.get_classes()[i]
		return mutateSchedule

	def _select_tournament_population(self, pop):
		tournament_pop = Population(0)
		i = 0
		while i< TOURNAMENT_SELECTION_SIZE:
			tournament_pop.get_schedules().append(pop.get_schedules()[rnd.randrange(0, POPULATION_SIZE)])
			i +=1
		tournament_pop.get_schedules().sort(key= lambda x: x.get_fitness(), reverse= True)
		return tournament_pop


class Course:
    def __init__(self, number, name, instructors, maxNumbOfStudents):
        self._number = number
        self._name = name
        self._instructors = instructors
        self._maxNumbOfStudents = maxNumbOfStudents

    def get_number(self): return self._number

    def get_name(self): return self._name

    def get_instructors(self): return self._instructors

    def get_maxNumbOfStudents(self): return self._maxNumbOfStudents

    def __str__(self): return self._name


class Instructor:
    def __init__(self, idIns, name):
        self._idIns = idIns
        self._name = name

    def get_idIns(self): return self._idIns

    def get_name(self): return self._name

    def __str__(self): return self._name


class Room:
    def __init__(self, number, seatingCapacity):
        self._number = number
        self._seatingCapacity = seatingCapacity

    def get_number(self): return self._number

    def get_seatingcapacity(self): return self._seatingCapacity


class MeetingTime:
	def __init__(self, idMT, time):
		self._idMT= idMT
		self._time = time
	def get_idMT(self): return self._idMT
	def get_time(self): return self._time
class Department:
    def __init__(self, name, courses):
        self._name = name
        self._courses = courses

    def get_name(self): return self._name

    def get_courses(self): return self._courses
class Class:
    def __init__(self, idClass, dept, course):
        self._idClass = idClass
        self._dept = dept
        self._course = course
        self._instructor = None
        self._room = None
        self._meetingTime = None

    def get_idClass(self): return self._idClass

    def get_dept(self): return self._dept

    def get_course(self): return self._course

    def get_instructor(self): return self._instructor

    def get_room(self): return self._room

    def get_meetingTime(self): return self._meetingTime

    def set_instructor(self, instructor):
        self._instructor = instructor

    def set_room(self, room):
        self._room = room
    def set_meetingTime(self, meetingTime):
        self._meetingTime= meetingTime
    def __str__(self):
        return str(self._dept.get_name()) + "," + str(self._course.get_name()) + "," + str(self._room.get_number()) + "," + \
               str(self._instructor.get_idIns()) + "," + str(self._meetingTime.get_idMT()) + " | "
class Display:
    def print_available_data(self):
        print("> All available data")
        self.print_dept()
        self.print_course()
        self.print_room()
        self.print_instructor()

    def print_dept(self):
        depts = data.get_depts()
        availableDeptsTable = prettytable.PrettyTable(['dept', 'courses'])
        for i in range(0, len(depts)):
            courses = depts.__getitem__(i).get_courses()
            tempStr = "["
            for j in range(0, len(courses) - 1):
                tempStr += courses[j].__str__() + ","
            tempStr += courses[len(courses) - 1].__str__() + "]"
            availableDeptsTable.add_row([depts.__getitem__(i).get_name(), tempStr])
        print(availableDeptsTable)

    def print_course(self):
        courses = data.get_courses()
        availableCoursesTable = prettytable.PrettyTable(['id', 'course #', 'max # of students', 'instructors'])
        for i in range(0, len(courses)):
            instructors = courses[i].get_instructors()
            tempStr = " "
            for j in range(0, len(instructors)-1):
                tempStr += instructors[j].__str__() + ","
            tempStr += instructors[len(instructors)-1].__str__()
            availableCoursesTable.add_row(
                [courses[i].get_number(), courses[i].get_name(), str(courses[i].get_maxNumbOfStudents()), tempStr])
        print(availableCoursesTable)

    def print_room(self):
        rooms = data.get_rooms()
        availableRoomsTable = prettytable.PrettyTable(['room', 'max seating capacity'])
        for i in range(0, len(rooms)):
            availableRoomsTable.add_row([str(rooms[i].get_number()), str(rooms[i].get_seatingcapacity())])
        print(availableRoomsTable)

    def print_instructor(self):
        instructors = data.get_instructors()
        availableInstructorsTable = prettytable.PrettyTable(['id', 'instructor'])
        for i in range(0, len(instructors)):
            availableInstructorsTable.add_row([instructors[i].get_idIns(), instructors[i].get_name()])
        print(availableInstructorsTable)

    def print_generation(self, population):
        table1 = prettytable.PrettyTable(
            ['schedule', 'fitness', ' number of conflicts', 'instructor(course, class, room, instructor, meeting time)'])
        schedules = population.get_schedules()
        for i in range(0, len(schedules)):
            table1.add_row([str(i), round(schedules[i].get_fitness(), 3), schedules[i].get_numberOfConflicts(), schedules[i].__str__()])
        print(table1)

    def print_schedule_as_table(self, schedule):
        classes = schedule.get_classes()
        table = prettytable.PrettyTable(
            ['class', 'dept', 'course[number, max of student]', 'room(capacity)', 'instructor', 'meeting time'])
        for i in range(0, len(classes)):
            table.add_row([str(i), classes[i].get_dept().get_name(), classes[i].get_course().get_name() + "(" +
                           classes[i].get_course().get_number() + "," + str(classes[
                               i].get_course().get_maxNumbOfStudents()) + ")",
                           str(classes[i].get_room().get_number()) + "(" + str(classes[i].get_room().get_seatingcapacity()) + ")",
                           classes[i].get_instructor().get_name(), classes[i].get_meetingTime().get_time()])
        print(table)
data = Data()
display = Display()
display.print_available_data()
generationNumber = 0
print("\n> generation #" + str(generationNumber))
population = Population(POPULATION_SIZE)
population.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)
display.print_generation(population)
display.print_schedule_as_table(population.get_schedules()[0])
gA = Ga()
while (population.get_schedules()[0].get_fitness() != 1.0):
	generationNumber += 1
	print("\n> generation "+ str(generationNumber))
	population= gA.envolve(population)
	population.get_schedules().sort(key= lambda x: x.get_fitness(), reverse = True)
	display.print_generation(population)
	display.print_schedule_as_table(population.get_schedules()[0])
print("\n\n")
