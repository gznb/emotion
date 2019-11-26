class AggregateRule(object):

    # 时间间隔
    def time_interval_rule(self, key_release_time, begin_time, end_time):
        """
        :param key_release_time:
        :param begin_time:
        :param end_time:
        :return:
        """
        return {"$match": {key_release_time: {"$gt": begin_time, "$lt": end_time}}}

    # key-value
    def equal_rule(self, key, value):
        """
        :param key:
        :param value:
        :return:
        """
        return {"$match": {key: value}}

    # 判断是不是在列表中，但是首先判断是否为全选，全选返回一个空字典
    def list_in_rule(self, key, value_list):
        """
        :param key:
        :param is_all:
        :param s_count:
        :param value_list:
        :return:
        """
        return {"$match": {key: {"$in": value_list}}}

    # 表联合
    def look_up_role(self, foreign_list, local_field, foreign_field, alias):
        """
        :param foreign_list:
        :param local_field:
        :param foreign_field:
        :param alias:
        :return:
        """
        return {
            "$lookup": {
                "from": foreign_list,
                "localField": local_field,
                "foreignField": foreign_field,
                "as": alias
            }
        }

    # 排序后统计数量
    def sort_by_count(self, field):
        """
        :param field:
        :return:
        """
        if "$" not in field:
            field = "${}".format(field)
        return {"$sortByCount":  field}

    # 根据指定的key, 进行 re 正则表达式的筛选
    def re_rule(self, key, value):
        return {"$match": {key: {"$regex": value}}}

    # 分页
    def skip_limit(self, skip, limit):

        return [
            {
                "$skip": (skip-1)*limit
            },
            {
                "$limit": limit
            }
        ]


    # 加入排序
    def my_sort(self, key, vlue):
        return {'$sort': {key: vlue}}

    # 得到一个根据时间的分组
    def time_group(self, time_format, key):
        if '$' not in key:
            key = '${}'.format(key)
        return {
            '$group': {
                '_id': {'$dateToString': {'format': time_format, 'date': key}},
                'now_time': {'$first': key},
                'count': {'$sum': 1}
            }
        }