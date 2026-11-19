from pydantic import BaseModel, Field


class AgentChatRequest(BaseModel):
    question: str = Field(min_length=3, max_length=2000)
    confirmed: bool = False


class AgentChatResponse(BaseModel):
    answer: str
    model: str
    tools_used: list[str]