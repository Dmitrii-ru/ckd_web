import os

from celery import shared_task

from base_app.utils.errors_plase import create_error
from core_app.redis_cli import RedisClientMain
from zaek.consts_zaek import custom_price_name
from zaek.models import ZaekPrice
from ckd.unils.parser_magadel.parser_maga_file import parser_maga_file_func
from ckd.unils.parser_magadel.parser_maga_file_v3 import ExcelParser
from zaek.utils.parser_price.need_price import CreatePriceExcel


@shared_task
def parse_price_zeak_file_task(odj_pk):
    price= ZaekPrice.objects.get(pk=odj_pk)
    client = RedisClientMain()
    client.clean_db()
    ExcelParser(price).parse()


@shared_task(bind=True)
def need_price_task(self):
    try:
        price = ZaekPrice.objects.get(name=custom_price_name)
    except ZaekPrice.DoesNotExist:
        try:
            cl = CreatePriceExcel()
            price = cl.get_product_all()
        except Exception as e:
            create_error(
                name='need_price_func',
                path=os.path.abspath(__file__),
                error=e
            )
            price = None
    return price, custom_price_name