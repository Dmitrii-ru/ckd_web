from core_app.redis_cli import RedisClientMain
from ckd.models import Magadel


def add_maga_to_context(request):
    rm = RedisClientMain()
    maga = rm.get_maga(model=Magadel)
    return {'maga': maga}
