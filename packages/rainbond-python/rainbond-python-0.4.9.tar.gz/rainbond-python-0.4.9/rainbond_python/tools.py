import logging
from datetime import datetime, timedelta

logging.basicConfig(
    level=logging.WARNING,
    format='[%(asctime)s] [%(levelname)s] %(message)s'
)


def handle_date(date: str, date_type='start') -> datetime:
    try:
        if not date:
            date_data = None
        elif date.isdigit():
            date_time = date[:10]
            date_data = datetime.fromtimestamp(int(date_time))
        else:
            date_data = datetime.strptime(date, "%Y-%m-%d")
        if date_type == 'end' and date_data:
            date_data += timedelta(hours=23, minutes=59, seconds=59)
    except Exception as err:
        date_data = None
        logging.warning('日期字符串解析异常: {0}'.format(err))
    return date_data
