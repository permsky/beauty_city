import json
import datetime

from .models import (
    Salon,
    Master,
    Procedure,
    SchedulePoint,
)


def fill_database(filepath):
    with open(filepath, encoding='UTF-8', mode='r') as f:
        salons = json.loads(f.read())
    for item in salons:
        if item['type'] == 'salons':
            for salon in item['salons']:
                Salon.objects.get_or_create(
                    name=salon['name'],
                    address=salon['address'],
                    photo=salon['photo']
                )
        if item['type'] == 'masters':
            for master in item['masters']:
                current_date = datetime.datetime.now().date()
                new_master, _ = Master.objects.get_or_create(
                    name=master['name'],
                    photo=master['photo'],
                    specialty=master['specialty']
                )
                for _ in range(7):
                    current_date += datetime.timedelta(days=1)
                    for time in master['time']:
                        SchedulePoint.objects.get_or_create(
                            date=current_date,
                            time=datetime.time(time, 0, 0),
                            master=new_master
                        )
        if item['type'] == 'procedures':
            for procedure in item['procedures']:
                Procedure.objects.get_or_create(
                    name=procedure['name'],
                    photo=procedure['photo'],
                    price=procedure['price'],
                )
