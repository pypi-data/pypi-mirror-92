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


def handle_db_to_list(db_list: list) -> list:
    """
    将db列表数据，转换为list（原db的id是ObjectId类型，转为json会报错）
    :param db_list:db列表数据（find()获取）
    :return:转换后的列表
    """
    if not isinstance(db_list, list):
        raise TypeError("a %s is required (got type %s)" % (list, type(db_list)))
    for db in db_list:
        db['_id'] = str(db['_id'])
    return db_list
