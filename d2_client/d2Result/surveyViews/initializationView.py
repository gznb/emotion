from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseServerError
from rest_framework.views import APIView
from d2Result.models import d2ResultModel
from d2Order.models import d2OrderModel
import datetime
from d2Result.utils.check_get_data import CheckReceiveFormat

from conf.time_conf import DATETIME_FORMAT_STR
import logging
logger = logging.getLogger('django')


class InitView(APIView):
    mainsource = {'name': 'X', 'count': 0}
    negative_counts = 0
    def get_channel(self, order_id):
        res_list = d2ResultModel._get_collection().aggregate([
            {
                "$match": { "GorderId": order_id}
            },
            {
              "$match": {"GresultAttribute": "负面"}
            },
            {
                '$lookup': {
                    'from': "d2_spider_model",
                    'localField': "GspiderId",
                    'foreignField': "GspiderId",
                    'as': "spider"
                }
            },
            {
                '$sortByCount': "$spider.GspiderClassification"
            }
        ])
        count = 0
        c_list = []
        for res in res_list:
            count += 1
            c_list.append(res['_id'][0])

        channel = {
            "isAll": 1,
            "count": count,
            "list": c_list
        }
        return channel

    def get_source(self, order_id):
        res_list = d2ResultModel._get_collection().aggregate([
            {
                "$match": {"GorderId": order_id}
            },
            {
                "$match": {"GresultAttribute": "负面"}
            },
            {
                '$lookup': {
                    'from': "d2_spider_model",
                    'localField': "GspiderId",
                    'foreignField': "GspiderId",
                    'as': "spider"
                }
            },
            {
                '$sortByCount': "$spider.GspiderName"
            }
        ])
        cover_count = 0
        for res in res_list:
            cover_count += 1
            if res['count'] > self.mainsource['count']:
                self.mainsource['count'] = res['count']
                self.mainsource['name'] = res['_id'][0]
            self.negative_counts += res['count']
        return cover_count

    def post(self, request, *args, **kwargs):
        # 得到渠道数
        order_id = request.data.get('orderId')
        check = CheckReceiveFormat()
        try:
            order_id = check.check_order_id(request.data)
        except (TypeError, ValueError) as err:
            return JsonResponse({'code': 0, 'msg': str(err), 'data': {}})
        except Exception as err:
            logger.error(err)
            return HttpResponseServerError()
        channel = self.get_channel(order_id)
        # print(channel)
        cover_count = self.get_source(order_id)
        # print(self.mainsource)
        # print(cover_count)
        info_counts = d2ResultModel.objects(GorderId=order_id).count()
        order = d2OrderModel.objects(GorderId=order_id).first()
        word_list = order.GorderKeywordList
        # print(info_counts)
        end_time = datetime.datetime.now()
        begin_time = end_time - datetime.timedelta(days=1)
        begin_time = begin_time.strftime(DATETIME_FORMAT_STR)
        end_time = end_time.strftime(DATETIME_FORMAT_STR)
        # print(begin_time, end_time)
        rev_data = {
            'code': 0,
            'msg': '成功',
            'data': {
                'infoCounts':info_counts,
                'negativeCounts': self.negative_counts,
                'mainsource': self.mainsource,
                'coverCount': cover_count,
                'source': channel,
                'word': {
                    'isAll': 1,
                    'count': len(word_list),
                    'list': word_list
                },
                'data': {
                    'timeInterval': 1,
                    'thisPeriod': {
                        'beginTime': begin_time,
                        'endTime': end_time
                    }
                }
            }
        }
        return JsonResponse(rev_data)
