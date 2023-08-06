import os
import json
import pymongo
import logging
import math
from datetime import datetime
from .parameter import Parameter
from .tools import handle_date, handle_db_to_list
from flask import abort, Response
from bson import ObjectId

logging.basicConfig(
    level=logging.WARNING,
    format='[%(asctime)s] [%(levelname)s] %(message)s'
)


class DBConnect():
    def __init__(self, db: str, collection: str, home_kye='MONGODB_HOST', port_kye='MONGODB_PORT'):
        self.mongo_home = os.environ.get(home_kye, None)
        self.mongo_port = os.environ.get(port_kye, 27017)

        if not self.mongo_home or not self.mongo_port:
            logging.error('MongoDB(组件)的组件连接信息是不完整的')

        self.mongo_client = pymongo.MongoClient(
            host=self.mongo_home,
            port=int(self.mongo_port)
        )
        self.mongo_db = self.mongo_client[db]
        self.mongo_collection = self.mongo_db[collection]

    def write_one_docu(self, docu: dict) -> str:
        try:
            if not docu.__contains__('creation_time'):
                docu['creation_time'] = datetime.today()
            new_data = self.mongo_collection.insert_one(docu)
            return new_data.inserted_id
        except Exception as err:
            str_data = 'MongoDB(组件)出现写入错误: {0}'.format(err)
            logging.warning(str_data)
            abort(Response(str_data, 500, {}))

    def does_it_exist(self, docu: dict) -> bool:
        count = self.mongo_collection.count_documents(docu)
        if count != 0:
            return True
        else:
            return False

    def update_docu(self, find_docu: dict, modify_docu: dict, many=False) -> dict:
        try:
            if many:
                student = self.mongo_collection.update_many(
                    find_docu, modify_docu)
            else:
                student = self.mongo_collection.update_one(
                    find_docu, modify_docu)
            # 返回匹配条数、受影响条数
            return {'matched_count': student.matched_count, 'modified_count': student.modified_count}
        except Exception as err:
            str_data = 'MongoDB(组件)出现更新错误: {0}'.format(err)
            logging.warning(str_data)
            abort(Response(str_data, 500, {}))

    def find_docu(self, id: str, raise_err=True) -> dict:
        """
        根据id查找记录
        :param id:记录id
        :param raise_err:是否抛出异常（使用abort抛出），否则返回None
        :return: 将结果转换为字典
        """
        if not isinstance(id, str):
            logging.warning("类型错误，预期 %s ,却得到 %s" % (list, type(id)))
            abort(Response("类型错误，预期 %s ,却得到 %s" % (list, type(id)), 400, {}))
        try:
            objId = ObjectId(id)
        except:
            logging.warning('id不合法，转换失败 id= %s' % (id,))
            abort(Response('id不合法，转换失败 id= %s' % (id,), 400, {}))
        entity = self.mongo_collection.find_one({'_id': objId})
        if entity is None:
            if raise_err:
                logging.info('找不到 id= %s 的记录' % (id,))
                abort(Response('找不到 id= %s 的记录' % (id,), 400, {}))
            else:
                return None
        entity['_id'] = str(entity['_id'])
        return dict(entity)

    def find_docu_list(self, id_list: list) -> list:
        """
        根据id列表查找记录列表
        :param id_list:
        :return:
        """
        if not isinstance(id_list, list):
            logging.warning("类型错误，预期 %s ,却得到 %s" % (list, type(id_list)))
            abort(Response("类型错误，预期 %s ,却得到 %s" % (list, type(id_list)), 400, {}))
        id_search = []
        for id in id_list:
            id_search.append({'_id': ObjectId(id)})
        find_dict = {'$or': id_search}
        data = self.mongo_collection.find(find_dict)
        return handle_db_to_list(data)

    def find_paging(self, parameter: Parameter) -> dict:
        parameter.verification(
            checking=parameter.param_url,
            verify={
                'page_size': str, 'current': str, 'columns': str, 'sort_order': str,
                'filtered_value': str, 'start_date': str, 'end_date': str,
            },
            optional={'start_date': '', 'end_date': ''})
        param = parameter.param_url
        try:
            page_size = int(param['page_size'])  # 每页条数
            current = int(param['current'])  # 当前页数
            if current < 1 or page_size < 1:
                raise Exception('当前页数和每页条数都从 1 开始计算')
            else:
                current -= 1
            columns = json.loads(param['columns'])  # 受控列
            # 排序顺序（对应受控列），asc=升序，desc=降序
            sort_order = json.loads(param['sort_order'])
            # 筛选值（对应受控列）
            filtered_value = json.loads(param['filtered_value'])
            start_date = handle_date(date=param['start_date'])  # 可选——开始日期
            # 可选——结束日期，与开始日期组成日期区间
            end_date = handle_date(date=param['end_date'], date_type='end')
            if len(columns) != len(sort_order) or len(columns) != len(filtered_value):
                raise Exception('三个控制列表的长度不一致')
        except Exception as err:
            str_data = '计算组件分页参数异常: {0}'.format(err)
            logging.warning(str_data)
            abort(Response(str_data, 400, {}))
        # 查找字典和排序列表
        find_dict = {}
        sort_list = []
        if len(columns):
            for i in range(len(columns)):
                # 整理请求参数中的筛选项字典
                if type(filtered_value[i]) == int:
                    find_dict[columns[i]] = filtered_value[i]
                else:
                    if filtered_value[i].strip() != '':
                        find_dict[columns[i]] = {'$regex': filtered_value[i]}
                # 整理请求参数中的筛排序列表
                if type(sort_order[i]) != str:
                    abort(Response('计算组件分页参数异常: 排序参数不支持 int 类型', 400, {}))
                sort_value = sort_order[i].strip()
                if sort_value == 'asc':
                    sort_list.append((columns[i], pymongo.ASCENDING))
                elif sort_value == 'desc':
                    sort_list.append((columns[i], pymongo.DESCENDING))
                elif sort_value == '':
                    pass
                else:
                    abort(Response('计算组件分页参数异常: 仅支持 asc 和 desc 两个值', 400, {}))
        # 仅存在日期查询区间参数时，进行额外的创建时间区间查询
        if start_date and end_date:
            find_dict['creation_time'] = {
                '$gte': start_date, '$lte': end_date}
        find_data = self.mongo_collection.find(find_dict)
        records_filtered = find_data.count()
        if not records_filtered:
            return {
                'records_total': self.mongo_collection.estimated_document_count(),
                'records_filtered': 0,
                'query_result': [],
                'total_pages': 0,
            }
        if sort_list:
            find_data.sort(sort_list).limit(
                page_size).skip(page_size * current)
        else:
            find_data.limit(page_size).skip(page_size * current)
        # 处理返回数据
        query_result = []
        for data in find_data:
            data['_id'] = str(data['_id'])
            query_result.append(data)
        return {
            'records_total': self.mongo_collection.estimated_document_count(),
            'records_filtered': records_filtered,
            'query_result': query_result,
            'total_pages': math.ceil(records_filtered / page_size),
        }
