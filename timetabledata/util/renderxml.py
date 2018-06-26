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