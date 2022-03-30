# import uuid
import shortuuid


def create_uiid():
    return shortuuid.uuid()
    # return uuid.uuid4()


def create_rand_uiid(length: int):
    return shortuuid.ShortUUID().random(length=length)
