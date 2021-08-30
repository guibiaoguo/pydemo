import asyncio

# python3.4 @asyncio.coroutine
async def hello():
    print("Hello world!")
    # 异步调用asyncio.sleep(1):
    # yield from
    r = await asyncio.sleep(1)
    print("Hello again!")

# 获取EventLoop:
loop = asyncio.get_event_loop()
# 执行coroutine
loop.run_until_complete(hello())
loop.close()