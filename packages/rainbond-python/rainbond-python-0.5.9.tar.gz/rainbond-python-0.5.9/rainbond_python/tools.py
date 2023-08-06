import logging
import time
from datetime import datetime, timedelta
from pymongo.cursor import Cursor
from bson.objectid import ObjectId
from flask import abort, Response

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
        str_data = '日期字符串解析异常: {0}'.format(err)
        logging.warning(str_data)
        abort(Response(str_data, 400, {}))


def handle_db_to_list(db_cursor: Cursor) -> list:
    """
    将db列表数据，转换为list（原db的id是ObjectId类型，转为json会报错）
    :param db_cursor:db列表数据（find()获取）
    :return:转换后的列表
    """
    if not isinstance(db_cursor, Cursor):
        str_data = '类型必须是 %s (获取类型为 %s)' % (Cursor, type(db_cursor))
        logging.warning(str_data)
        abort(Response(str_data, 500, {}))
    result = []
    for db in db_cursor:
        db['_id'] = str(db['_id'])
        db['creation_time'] = int(time.mktime(
            db['creation_time'].timetuple())) * 1000
        result.append(dict(db))
    return result


def handle_db_id(data_dict: dict) -> dict:
    try:
        if data_dict.__contains__('_id'):
            data_dict['_id'] = ObjectId(str(data_dict['_id']))
        return data_dict
    except Exception as err:
        str_data = 'MongoDB id 格式解析异常: {0}'.format(err)
        logging.warning(str_data)
        abort(Response(str_data, 400, {}))
