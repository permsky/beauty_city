from django import template


register = template.Library()

@register.filter(name='format_delta')
def format_timedelta(timedelta):
    '''Convert a datetime.timedelta object into Years, Months.'''
    timedelta_in_seconds = timedelta.total_seconds()
    formated_time = ''
    if timedelta_in_seconds > 31536000: # 60sec * 60min * 24hrs * 365days
        years = timedelta_in_seconds // 31536000
        if any([
            str(int(years)).endswith('0'),
            str(int(years)).endswith('5'),
            str(int(years)).endswith('6'),
            str(int(years)).endswith('7'),
            str(int(years)).endswith('8'),
            str(int(years)).endswith('9'),
            str(int(years)).endswith('11'),
            str(int(years)).endswith('12'),
            str(int(years)).endswith('13'),
            str(int(years)).endswith('14')
        ]):
            formated_time += f'{int(years)} лет'
        elif int(years) == 1:
            formated_time += f'{int(years)} год'
        else:
            formated_time += f'{int(years)} года'
        timedelta_in_seconds = timedelta_in_seconds - years*31536000

    if timedelta_in_seconds > 2592000: # 60sec * 60min * 24hrs * 30days
        months = timedelta_in_seconds // 2592000
        if any([int(months) == 2, int(months) == 3, int(months) == 4]):
            formated_time += f' {int(months)} месяца'
        elif int(months) == 1:
            formated_time += f' {int(months)} месяц'
        else:
            formated_time += f' {int(months)} месяцев'
        timedelta_in_seconds = timedelta_in_seconds - months*2592000

    return formated_time