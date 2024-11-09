
from celery import shared_task

from core_app.redis_cli import RedisClientMain
from zaek.models import ZaekPrice
from ckd.unils.parser_magadel.parser_maga_file import parser_maga_file_func
from ckd.unils.parser_magadel.parser_maga_file_v3 import ExcelParser


@shared_task
def parse_price_zeak_file_task(odj_pk):
    price= ZaekPrice.objects.get(pk=odj_pk)
    client = RedisClientMain()
    client.clean_db()
    ExcelParser(price).parse()