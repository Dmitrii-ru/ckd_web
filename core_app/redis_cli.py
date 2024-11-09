from datetime import datetime
import json
import redis
from .settings import REDIS_DB_CKD, REDIS_PORT, TIME_ZONE
from django.core.serializers.json import DjangoJSONEncoder
from zoneinfo import ZoneInfo
from typing import Dict, Any

class RedisClientMain:

    def __init__(
            self,
            time_cache=60*60,
            db = REDIS_DB_CKD
    ):
        self.time_cache = time_cache
        self.redis_client = redis.StrictRedis(
            host='localhost',
            port=REDIS_PORT,
            db=db,
            decode_responses=True
        )

    def clean_db(self):
        self.redis_client.flushdb()

    def get_maga(self, model=None):

        key = 'first_magadel'
        cached_data = self.redis_client.get(key)
        try:
            if not cached_data:
                obj = model.objects.all().first()
                if obj:
                    serialized_data = json.dumps({
                        'name': obj.name,
                    }, cls=DjangoJSONEncoder)

                    self.redis_client.set(key, serialized_data, ex=self.time_cache)
                    cached_data = serialized_data


            return json.loads(cached_data) if cached_data else None
        except:
            return None

    def get_products_parents(self, model_product, model_group):

        key_products = 'Products'
        key_groups = 'Groups'

        cached_products = self.redis_client.get(key_products)
        cached_groups = self.redis_client.get(key_groups)

        if not cached_products:
            products = model_product.objects.select_related('parent').all()
            db_products_dict = {
                obj.code: {
                    'name': obj.name,
                    'parent': obj.parent.name if obj.parent else None,
                    'free_balance': obj.free_balance,
                    'list_possible_deliveries': obj.list_possible_deliveries,
                    'sum_possible_deliveries': obj.sum_possible_deliveries,
                    'unit': obj.unit,
                    'price':obj.price
                }
                for obj in products
            }
            serialized_products = json.dumps(db_products_dict, cls=DjangoJSONEncoder)
            self.redis_client.set(key_products, serialized_products, ex=self.time_cache)
            cached_products = serialized_products

        if not cached_groups:
            self.clean_db()
            groups = model_group.objects.all()

            db_groups_dict = {
                obj.id: {
                    'name': obj.id
                }
                for obj in groups
            }

            serialized_groups = json.dumps(db_groups_dict, cls=DjangoJSONEncoder)
            self.redis_client.set(key_groups, serialized_groups, ex=self.time_cache)
            cached_groups = serialized_groups

        return (
            json.loads(cached_products) if cached_products else None,
            json.loads(cached_groups) if cached_groups else None
        )

    def get_key_values(
            self,
            key_name:str,
    ) -> Dict[str, Any]:

        data = self.redis_client.get(key_name)
        if data:
            deserialized_data = json.loads(data)
            return deserialized_data


    def create_key(
            self,
            key_name: str,
            data:Dict[str,Any]
    ) -> Dict[str, Any]:
        
        serialized_groups = json.dumps(data, cls=DjangoJSONEncoder)
        self.redis_client.set(key_name, serialized_groups, ex=self.time_cache)
        return data