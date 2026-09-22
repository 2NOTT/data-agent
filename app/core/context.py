import asyncio
from contextvars import ContextVar

# 创建一个用来存储请求ID的ContextVar对象

_req_context_var: ContextVar = ContextVar("req_id", default=0)


# 保存请求id
def set_req_id(request_id: int):
    _req_context_var.set(request_id)


# 获取请求id
def get_req_id() -> int:
    return _req_context_var.get()


if __name__ == "__main__":
    async def req1():
        print(f"请求1开始准备执行:req_id={_req_context_var.get()}")  # 0
        _req_context_var.set(1)
        print(f"请求1执行完毕:req_id={_req_context_var.get()}")  # 1

    async def req2():
        print(f"请求2开始准备执行:req_id={_req_context_var.get()}")  # 0
        _req_context_var.set(2)
        print(f"请求2执行完毕:req_id={_req_context_var.get()}")  # 2

    def test2():
        print(f"---------{_req_context_var.get()}")# 0
        _req_context_var.set(3)
        print(f"---------{_req_context_var.get()}")# 3
        _req_context_var.set(4)
        print(f"---------{_req_context_var.get()}")# 4

    async def test():
        cor1=req1()
        cor2=req2()

        await asyncio.gather(cor1, cor2)

    # asyncio.run(test())
    test2()

