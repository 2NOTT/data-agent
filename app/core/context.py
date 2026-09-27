from contextvars import ContextVar


# 创建一个用来存储请求id的ContextVar对象

_req_context_var = ContextVar("req_id", default="")

# 保存请求id
def set_req_id(request_id: str):
    _req_context_var.set(request_id)
    return request_id

# 获取请求id
def get_req_id() -> str:
    return _req_context_var.get()

