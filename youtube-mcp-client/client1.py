import asyncio
from langchain.mcp import MCPAdapter
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import ToolMessage
import json

load_dotenv()

SERVERS = {
    "mcpServers": {
        # "math": {
        #     "command": r"C:\Users\anjal\AppData\Local\Programs\Python\Python312\Scripts\uv.exe",
        #     "args": [
        #         "run",
        #         "--project",
        #         r"D:\anjal\MCP\youtube-mcp-client",
        #         "fastmcp",
        #         "run",
        #         r"D:\anjal\MCP\youtube-mcp-client\main.py"
        #     ]
        # },
        "expense": {
        "url": "https://absolute-apricot-reptile.fastmcp.app/mcp",
        "auth": "oauth"
        }
    }
}

async def main():
    async with MCPAdapter(SERVERS) as adapter:
        tools = await adapter.list_tools()

    named_tools = {}
    for tool in tools:
        named_tools[tool.name] = tool        

    llm = ChatGroq(model="openai/gpt-oss-20b")
    llm_with_tools = llm.bind_tools(tools)

    prompt = "Add an expense ₹804 for groceries on 4th of November."
    response = await llm_with_tools.ainvoke(prompt)
    if not getattr(response, "tool_calls", None):
        print("\nLLM Reply:", response.content)
        return

    tool_messages = []
    for tc in response.tool_calls:
        selected_tool = tc["name"]
        selected_tool_args = tc.get("args") or {}
        selected_tool_id = tc["id"]

        result = await named_tools[selected_tool].ainvoke(selected_tool_args)
        tool_messages.append(ToolMessage(tool_call_id=selected_tool_id, content=json.dumps(result)))
        

    final_response = await llm_with_tools.ainvoke([prompt, response, *tool_messages])
    print(f"Final response: {final_response.content}")


if __name__ == '__main__':
    asyncio.run(main())