from timetabledata.models import ConexionType, Teacher, Group, Room, Data, Tag, Activity
ConexionType.objects.all().delete()
Teacher.objects.all().delete()
Group.objects.all().delete()
Room.objects.all().delete()
Data.objects.all().delete()
Tag.objects.all().delete()
Activity.objects.all().delete()
