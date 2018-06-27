from django.shortcuts import render
from django.template import loader


def renderSameTime(list):
    template = loader.get_template('timetabledata/ConstraintActivitiesSameStartingTime.xml')
    context = {
        'activities': list
    }
    return template.render(context)

def renderMinDaysBetweenActivities(list):
    template = loader.get_template('timetabledata/ConstraintMinDaysBetweenActivities.xml')
    context = {
        'activities': list
    }
    return template.render(context)

def renderActiviy(list):
    template = loader.get_template('timetabledata/Activity.xml')
    context = {
        'activities': list,
        'teachers':list,
        'subject':list,
        'students':list,
        'duration':list,
        'total_duration':list,
        'activity_id':list,
        'group_id':list
    }
    return template.render(context)

def renderBuildingRooms(buildings,rooms):
    template = loader.get_template('timetabledata/BuildingsRooms.xml')
    context = {
        'buildings': buildings,
        'rooms': rooms
    }
    return template.render(context)

def renderActivity(context):
    template = loader.get_template('timetabledata/Activity.xml')
    return template.render(context)

def renderSubjects(subjects):
    template = loader.get_template('timetabledata/Subject.xml')
    context = {
        'subjects': subjects
    }
    return template.render(context)

def renderTeachers(teachers):
    template = loader.get_template('timetabledata/Teachers.xml')
    context = {
        'teachers': teachers
    }
    return template.render(context)

def renderStudents(students):
    template = loader.get_template('timetabledata/Students.xml')
    print(students.keys())
    for k in students:
        print(students[k])
    context = {
        'students': students
    }
    return template.render(context)

def xmldefinition():
    '''
    Institution_Name
    Comments
    Days_List
             Day
             Number_of_Days
    Hours_List
             Number_of_Hours
             Hour
    Subjects_List
             Subject
    Activity_Tags_List
             Activity_Tag
    Teachers_List
             Teacher
    Students_List
             Year
    Activities_List
             Activity
    Buildings_List
             Building
    Rooms_List
             Room
    Time_Constraints_List
             ConstraintActivitiesNotOverlapping
             ConstraintTeachersMaxSpanPerDay
             ConstraintTeachersActivityTagMaxHoursContinuously
             ConstraintStudentsSetNotAvailableTimes
             ConstraintActivitiesSameStartingTime
             ConstraintActivitiesOccupyMaxTimeSlotsFromSelection
             ConstraintMinDaysBetweenActivities
             ConstraintTeacherMaxDaysPerWeek
             ConstraintTeachersMaxHoursDaily
             ConstraintTeacherNotAvailableTimes
             ConstraintBasicCompulsoryTime
             ConstraintActivitiesPreferredTimeSlots
             ConstraintTeacherIntervalMaxDaysPerWeek
    Space_Constraints_List
             ConstraintActivityPreferredRoom
             ConstraintTeachersMaxBuildingChangesPerDay
             ConstraintTeachersMinGapsBetweenBuildingChanges
             ConstraintStudentsSetHomeRoom
             ConstraintActivityPreferredRooms
             ConstraintBasicCompulsorySpace
             ConstraintRoomNotAvailableTimes
    '''
    pass