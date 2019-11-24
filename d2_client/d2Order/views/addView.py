from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseServerError
import simplejson
from d2Order.models import d2OrderModel
import datetime
import logging
logger = logging.getLogger('django')



def Zadd(request):

    get_data = simplejson.loads(request.body)
    try:
        telephone = get_data['telephone']
        data = get_data['data']
        order_name = data['orderName']
        word = data['word']
        word_list = word['list']
    except Exception as err:
        logger.error(err)
        return HttpResponseBadRequest('关键参数丢失')
    else:
        init_last_time = datetime.datetime.strptime('1981-11-11 11:11:11', '%Y-%m-%d %H:%M:%S')
        counts = d2OrderModel.objects().count()
        order = d2OrderModel(
            GorderId=counts,
            GorderName=order_name,
            GorderKeywordList=word_list,
            GorderLastTime=init_last_time,
            GuserTelephone=telephone,
            GorderSpiderList='1'*100,
            GorderCreateTime=datetime.datetime.now(),
        )
        
        try:
            order.save()
        except Exception as err:
            logger.error(err)
            return HttpResponseServerError()

        rev_data = {
            'code': 0,
            'msg': "添加成功",
            'data': {}
        }
        return JsonResponse(rev_data)