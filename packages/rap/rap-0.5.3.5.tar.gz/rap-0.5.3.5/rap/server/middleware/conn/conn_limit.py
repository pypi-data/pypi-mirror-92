import logging

from rap.common.conn import ServerConnection
from rap.common.utlis import Constant, Event
from rap.manager.redis_manager import redis_manager
from rap.server.middleware.base import BaseConnMiddleware
from rap.server.model import ResponseModel
from rap.server.response import Response


class ConnLimitMiddleware(BaseConnMiddleware):
    """
    feat: limit server max conn num
    """

    def __init__(self, max_conn: int = 1024):
        self._max_conn: int = max_conn
        self._conn_count: int = 0
        self.register(self.modify_max_conn)

    def modify_max_conn(self, max_conn: int) -> None:
        self._max_conn = max_conn

    async def dispatch(self, conn: ServerConnection):
        if self._conn_count > self._max_conn:
            logging.error(f"Currently exceeding the maximum number of connections limit, close {conn.peer_tuple}")
            await Response(conn)(
                ResponseModel(
                    body=Event(Constant.EVENT_CLOSE_CONN, "Currently exceeding the maximum number of connections limit")
                ),
            )
            await conn.await_close()
            return
        else:
            try:
                self._conn_count += 1
                await self.call_next(conn)
            finally:
                self._conn_count -= 1


class IpMaxConnMiddleware(BaseConnMiddleware):
    """
    feat: Limit the number of connections of a specified IP within a unit time
    """

    def __init__(self, ip_max_conn: int = 128, timeout: int = 180):
        self._ip_max_conn: int = ip_max_conn
        self._timeout: int = timeout
        self.register(self.modify_max_ip_max_conn)
        self.register(self.modify_ip_max_timeout)

    def modify_max_ip_max_conn(self, ip_max: int) -> None:
        self._ip_max_conn = ip_max

    def modify_ip_max_timeout(self, timeout: int) -> None:
        self._timeout = timeout

    async def dispatch(self, conn: ServerConnection):
        key: str = redis_manager.namespace + conn.peer_tuple[0]
        if (await redis_manager.redis_pool.get(key)) > self._ip_max_conn:
            logging.error(f"Currently exceeding the maximum number of ip conn limit, close {conn.peer_tuple}")
            await Response(conn)(
                ResponseModel(
                    body=Event(Constant.EVENT_CLOSE_CONN, "Currently exceeding the maximum number of ip conn limit")
                ),
            )
            await conn.await_close()
            return
        else:
            await redis_manager.redis_pool.incr(key)
            try:
                await self.call_next(conn)
            finally:
                await redis_manager.redis_pool.decr(key)
                await redis_manager.redis_pool.expire(key, self._timeout)
