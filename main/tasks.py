
from celery import shared_task

from core_app.redis_cli import RedisClientMain
from main.models import FileMaga
from main.unils.parser_magadel.parser_maga_file import parser_maga_file_func
from main.unils.parser_magadel.parser_maga_file_v3 import ExcelParser


@shared_task
def parse_maga_file_task(maga_pk):
    maga= FileMaga.objects.get(pk=maga_pk)
    client = RedisClientMain()
    client.clean_db()
    ExcelParser(maga).parse()