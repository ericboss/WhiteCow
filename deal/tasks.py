from celery import shared_task

@shared_task
def print_hobby():
    hobby = "django"
    f = open ("deal/demo.txt", "a")
    f.write(hobby)
    f.close()


days = ['mon,tue,wed,thu,fri,sat,sun', 'sat,sun']
times = [5,6,7,8,20,21,22]