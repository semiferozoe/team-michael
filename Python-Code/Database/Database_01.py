# import the sql connection library
import sqlite3 as sql
# connect to sql
connect = sql.connect('class_schedule.db')

# Connect to cursor in the databa creation
c= connect.cursor()

# database 1 small amount of teachers, classes, rooms, and departments
#   larger amount of class times

# Create another database with more information and increased amount of scenerios later.
c.execute("""create table room (number text, cpacity integer)""")
c.execute("insert into room Values ('Cott 111', 25),"
                                  "('Cott 115', 50),"
                                  "('JoeJ 211', 14),"
                                  "('JoeJ 226', 25),"
                                  "('BobB 314', 30),"
                                  "('BobB 330', 30),"
                                  "('BobB 335', 30)")
c.execute("""create table meeting_time (id text, time text)""")
c.execute("insert into meeting_time Values ('MT1', 'MWF 08:00 - 9:15'),"
                                          "('MT2', 'MWF 8:00 - 9:50'),"
                                          "('MT3', 'MWF 10:00 - 11:00'),"
                                          "('MT4', 'MWF 12:00 - 01:00'),"
                                          "('MT5', 'TTH 08:00 - 9:15'),"
                                          "('MT6', 'TTH 8:00 - 9:50'),"
                                          "('MT7', 'TTH 10:00 - 11:00'),"
                                          "('MT8', 'TTH 12:00 - 01:00'),"
                                          "('MT9', 'TTH 12:00 - 01:50')")
c.execute("""create table instructor (number text, name text)""")
c.execute("insert into instructor Values ('I1', 'Dr. Songming Hou'),"
                                        "('I2', 'Dr. Kyle Prather'),"
                                        "('I3', 'Dr. Bruce Magee'),"
                                        "('I4', 'Mr. Joel Stake'),"
                                        "('I5', 'Dr. Krystal Corbett')")
c.execute("""create table instructor_availability (instructor_id text, meeting_time_id text)""")
c.execute("insert into instructor_availability(instructor_id, meeting_time_id) values "
                                                   "('I1', 'MT1'),"
									               "('I1', 'MT2'),"
                                                   "('I1', 'MT3'),"
                                                   "('I2', 'MT1'),"				
									    		   "('I2', 'MT2'),"
									    		   "('I2', 'MT3'),"
									    		   "('I2', 'MT4'),"
									    		   "('I3', 'MT5'),"
									    		   "('I3', 'MT6'),"
									    		   "('I3', 'MT7'),"
                                                   "('I3', 'MT8'),"
                                                   "('I3', 'MT9'),"
												   "('I4', 'MT1'),"
												   "('I4', 'MT2'),"
												   "('I4', 'MT3'),"
                                                   "('I4', 'MT4'),"
                                                   "('I4', 'MT5'),"
                                                   "('I4', 'MT6'),"
                                                   "('I4', 'MT7'),"
                                                   "('I4', 'MT8'),"
									    		   "('I4', 'MT9'),"
                                                   "('I5', 'MT1'),"
                                                   "('I5', 'MT3'),"
                                                   "('I5', 'MT5'),"
                                                   "('I5', 'MT7'),"
                                                   "('I5', 'MT9')")
c.execute("""create table course_instructor (course_number text, instructor_number text)""")
c.execute("insert into course_instructor Values ('C1', 'I2'),"
                                               "('C2', 'I1'),"
                                               "('C3', 'I5'),"
                                               "('C4', 'I1'),"
                                               "('C5', 'I3'),"
                                               "('C6', 'I4'),"
                                               "('C7', 'I4')")
c.execute("""create table course (number text, name text, max_numb_of_students)""")
c.execute("insert into course Values ('C1', '406', 15),"
                                    "('C2', '122', 35)," 
                                    "('C3', '308', 25),"
                                    "('C4', '311', 30),"
                                    "('C5', '102', 20),"
                                    "('C6', '130', 45),"
                                    "('C7', '131', 45)")
c.execute("""create table dept (name text)""")
c.execute("insert into dept Values ('BISC'),"
                                  "('CSC'),"
                                  "('ENGL'),"
                                  "('ENGR'),"
                                  "('MATH')")
c.execute("""create table dept_course (name text, course_numb text)""")
c.execute("insert into dept_course Values ('CSC', 'C1'),"
                                         "('ENGR', 'C3'),"
                                         "('MATH', 'C2'),"
                                         "('MATH', 'C4'),"
                                         "('ENGL', 'C5'),"
                                         "('BISC', 'C6'),"
                                         "('BISC', 'C7')")
connect.commit()
c.close()
connect.close()