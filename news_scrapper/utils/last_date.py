from datetime import timedelta, date, datetime
from dateutil.relativedelta import relativedelta

@staticmethod
def is_before(date_to_check, months):
    now = datetime.now()
    limit = date(now.year, now.month, now.day)
    if(months < 1):
        months = 1
        limit = date(limit.year, limit.month, 1)
    else :
        limit = limit - relativedelta(months=months-1)
                                
    return date_to_check > limit