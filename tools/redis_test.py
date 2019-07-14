# -*- coding: utf-8 -*-
import redis

redis_cli = redis.StrictRedis()
redis_cli.incr("cls_count")

