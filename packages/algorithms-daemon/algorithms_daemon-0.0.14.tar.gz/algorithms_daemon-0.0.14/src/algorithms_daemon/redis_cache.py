from .config import RedisHost, RedisPort, TaskId, WorkerIdentity
import redis

pool = redis.ConnectionPool(
    host=RedisHost, port=RedisPort, password='', decode_responses=True)
rs = redis.StrictRedis(connection_pool=pool)


def set_value(value):
    with rs.lock(f'lock_{TaskId}', 10):
        rs.hset(f'task_daemon_{TaskId}', WorkerIdentity, value)


def get_value():
    return rs.hget(f'task_daemon_{TaskId}', WorkerIdentity)


def get_all_values():
    return rs.hgetall(f'task_daemon_{TaskId}')


if __name__ == "__main__":
    set_value('1')
    print(get_all_values())  # value contains jobid-value
