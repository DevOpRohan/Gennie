import json
from pydantic import BaseModel, Field

from tool_manager.ToolManager import ToolManager
from utils.llm import open_ai_tools_execution

class SumInput(BaseModel):
    a: int = Field(...)
    b: int = Field(...)

def sum_numbers(a: int, b: int) -> int:
    return a + b

class LongInput(BaseModel):
    length: int = Field(...)

def long_text(length: int) -> str:
    return "x" * length

def test_tool_registration_and_execution():
    tm = ToolManager()
    tm.register_tool(
        func=sum_numbers,
        name="sum_numbers",
        description="add two numbers",
        full_arg_spec=SumInput,
        return_direct=True,
        exposed_args=["a", "b"],
    )

    tools = [
        {
            "id": "1",
            "type": "function",
            "function": {
                "name": "sum_numbers",
                "arguments": json.dumps({"a": 2, "b": 3}),
            },
        }
    ]

    result = open_ai_tools_execution(tm, tools)
    assert result == [
        {
            "tool_call_id": "1",
            "role": "tool",
            "name": "sum_numbers",
            "content": "5",
        }
    ]


def test_long_output_truncation():
    tm = ToolManager()
    tm.register_tool(
        func=long_text,
        name="long_text",
        description="generate long text",
        full_arg_spec=LongInput,
        return_direct=True,
        exposed_args=["length"],
    )

    tools = [
        {
            "id": "2",
            "type": "function",
            "function": {
                "name": "long_text",
                "arguments": json.dumps({"length": 8000}),
            },
        }
    ]

    result = open_ai_tools_execution(tm, tools)
    response = result[0]["content"]
    expected_suffix = " RESPONSE IS CUTTED BECAUSE OF MORE THAN 1000 CHARS"
    assert response.endswith(expected_suffix)
    assert len(response) == 7000 + len(expected_suffix)
    assert response[:7000] == "x" * 7000
