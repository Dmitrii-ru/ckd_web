
from celery import shared_task

from main.unils.parser_magadel.parser_maga_file import parser_maga_file_func


@shared_task
def parse_maga_file_task(file_path):
    print('ТАСК')
    parser_maga_file_func(file_path)