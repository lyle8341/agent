from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain.agents.middleware import (
    PIIMiddleware,
    SummarizationMiddleware,
    ToolRetryMiddleware
)

load_dotenv()


# 定义一个简单的工具函数
@tool("query_order_state", description="根据订单号查询订单状态")
def query_order_state(order_id: str) -> str:
    if order_id == '1024':
        return "订单1024的状态是： 已发货。。。。"
    else:
        return f"未找到订单{order_id}的信息"


agent = create_agent(
    model="openai:gpt-4o",
    tools=[query_order_state],
    middleware=[
        # 脱敏中间件
        PIIMiddleware(
            pii_type="email",
            strategy="redact",
            apply_to_input=True,
        ),
        # 自动总结中间件
        SummarizationMiddleware(
            model="openai:gpt-4o-mini",
            trigger=('tokens', 4000),
            keep=('messages', 20)
        ),
        # 工具调用失败自动重试
        ToolRetryMiddleware(
            max_retries=3,
            backoff_factor=2,
            initial_delay=1.0,
            max_delay=60.0,
            jitter=True
        )
    ]
)

if __name__ == '__main__':
    result = agent.invoke({
        "message": [{"role": "user", "content": "帮我查一下订单1024的状态"}]
    })
    print(result['messages'][-1].content)
