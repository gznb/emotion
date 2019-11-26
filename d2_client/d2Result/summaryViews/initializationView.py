from django.http import JsonResponse, HttpResponseServerError
from rest_framework.views import APIView
from d2Result.models import d2ResultModel
from d2Order.models import d2OrderModel
from d2Result.utils.check_get_data import CheckReceiveFormat

import logging
logger = logging.getLogger('django')


class IniTializationView(APIView):

    # 得到来源
    def get_source(self, order_id):
        res_list = d2ResultModel._get_collection().aggregate([
            {
                "$match": {
                    "GorderId": order_id
                }
            },
            {
                "$lookup": {
                    "from": "d2_spider_model",
                    "localField": "GspiderId",
                    "foreignField": "GspiderId",
                    "as": "spider"
                }
            },
            {
                "$sortByCount": "$spider.GspiderClassification"
            }
        ])
        source = {
            'isAll': 1,
            "count": 0,
            "total": 0,
            "list": [],
        }
        for res in res_list:
            source['count'] += 1
            source['total'] += res['count']
            source['list'].append({'name': ''.join(res['_id']), 'total': res['count']})
        return source

    # 得到属性
    def get_attribute(self, order_id):
        res_list = d2ResultModel._get_collection().aggregate([
            {
                "$match": {
                    "GorderId": order_id
                }
            },
            {
                "$sortByCount": "$GresultAttribute"
            }
        ])
        attribute = {
            "total": 0,
            "positive": 0,
            "negative": 0,
            "neutral": 0
        }
        for res in res_list:
            attribute['total'] += res['count']
            if '中性' in res['_id']:
                attribute['neutral'] += res['count']
            elif '正面' in res['_id']:
                attribute['positive'] += res['count']
            elif '负面' in res['_id']:
                attribute['negative'] += res['count']
        return attribute

    # 得到监测词
    def get_word(self, keyword_list):
        word = {
            'isAll': 1,
            'count': len(keyword_list),
            'list': keyword_list
        }
        return word

    def post(self, requst, *args, **kwargs):
        rev_data = {}
        check = CheckReceiveFormat()
        order_id = requst.data.get('orderId')
        try:
            order_id = check.check_order_id({'orderId':order_id})
        except (TypeError, ValueError) as err:
            return JsonResponse({'code': 2, 'msg': err, 'data': {}})
        except Exception as err:
            logger.error(err)
            return HttpResponseServerError()

        order = d2OrderModel.objects(GorderId=order_id).first()

        if order is None:
            return JsonResponse({'code': 2, 'msg': "该订单不存在", 'data': {}})
        else:
            try:
                source = self.get_source(order.GorderId)
                # print(source)
                attribute = self.get_attribute(order.GorderId)
                # print(attribute)
                word = self.get_word(order.GorderKeywordList)
                # print(word)
            except Exception as err:
                logger.error(err)
                return HttpResponseServerError()
            else:
                rev_data = {
                    'code': 0,
                    'msg': "成功",
                    'data': {
                        'attribute': attribute,
                        'source': source,
                        'word': word
                    }
                }
            finally:
                return JsonResponse(rev_data)