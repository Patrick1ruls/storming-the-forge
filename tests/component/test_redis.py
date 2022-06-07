import pytest
import redis
import logging
import json
import random
import string


@pytest.fixture
def r(scope="class"):
    logging.info("Connecting to redis...")
    try:
        r = redis.StrictRedis(host='localhost', port=6379, db=0)
        yield r
        r.flushdb()
    except (redis.exceptions.ConnectionError, ConnectionRefusedError):
        logging.error("Redis connection error!")
        

def test_redis_is_available(r):
    assert is_redis_available(r)


def is_redis_available(r):
    try:
        r.ping()
        logging.info("Successfully connected to redis")
    except (redis.exceptions.ConnectionError, ConnectionRefusedError):
        logging.error("Redis connection error!")
        return False
    return True


def generate_vote_json():
    vote = random.choice(["a", "b"])
    voter_id = "".join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(15))
    return {"vote": vote, "voter_id": voter_id}


def test_redis_queue_push_pull(r):
    vote_input = json.dumps(generate_vote_json())
    r.lpush("test", vote_input)
    vote_output = r.rpop("test").decode("ASCII")
    assert vote_input == vote_output
