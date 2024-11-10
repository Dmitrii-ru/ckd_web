import os

from celery import shared_task

from base_app.utils.errors_plase import create_error
from core_app.redis_cli import RedisClientMain
from zaek.models import ZaekPrice
from ckd.unils.parser_magadel.parser_maga_file_v3 import ExcelParser



@shared_task
def parse_price_zeak_file_task(odj_pk):
    price= ZaekPrice.objects.get(pk=odj_pk)
    client = RedisClientMain()
    client.clean_db()
    ExcelParser(price).parse()


@shared_task
def need_price_task():
    try:
        from zaek.utils.parser_price.need_price import CreatePriceExcel
        cl = CreatePriceExcel()
        cl.get_product_all()
    except Exception as e:
        create_error(
            name='need_price_task',
            path=os.path.abspath(__file__),
            error=e
        )


@shared_task
def get_price_task(price_path):
    try:
        from zaek.utils.parser_price.parser_price import DataPrice
        data = DataPrice(price_path=price_path)
        data.get_price()
    except Exception as e:
        create_error(
            name='get_price_task',
            path=os.path.abspath(__file__),
            error=e
        )


