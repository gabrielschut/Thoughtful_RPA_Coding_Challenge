from datetime import timedelta, date, datetime
from dateutil.relativedelta import relativedelta

@staticmethod
def is_before(date_to_check, months):
    now = datetime.now()
    limit = date(now.year, now.month, now.day)
    limit = date(limit.year, limit.month, 1)
    if(months <= 1):
        months = 1
        
    limit = limit - relativedelta(months=months-1)
                                
    return date_to_check < limit