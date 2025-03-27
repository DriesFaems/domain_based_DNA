from typing import List, Optional
from pydantic import BaseModel
from openai import AsyncOpenAI

class AgentOutput(BaseModel):
    answer: str
    reasoning: str

class Agent:
    def __init__(
        self,
        name: str,
        instructions: str,
        handoff_description: Optional[str] = None,
        handoffs: Optional[List['Agent']] = None,
        input_guardrails: Optional[List] = None
    ):
        self.name = name
        self.instructions = instructions
        self.handoff_description = handoff_description
        self.handoffs = handoffs or []
        self.input_guardrails = input_guardrails or []

    async def process(self, input_data: str, context: dict) -> AgentOutput:
        client = AsyncOpenAI(api_key=context.get("api_key"))
        
        messages = [
            {"role": "system", "content": self.instructions},
            {"role": "user", "content": input_data}
        ]
        
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.7
        )
        
        return AgentOutput(
            answer=response.choices[0].message.content,
            reasoning="Based on my expertise and the provided information"
        )

class Runner:
    @staticmethod
    async def run(agent: Agent, input_data: str, context: dict) -> AgentOutput:
        return await agent.process(input_data, context) 