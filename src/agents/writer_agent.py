from crewai import Agent
from src.tools.search_tools import CompetitorLookupTool

class WriterAgent(Agent):
    def __init__(self, llm):
        super().__init__(
            role='Senior Copywriter',
            goal='Create objective product comparisons.',
            backstory="You write honest comparison tables.",
            llm=llm, 
            verbose=True,
            allow_delegation=False,
            tools=[CompetitorLookupTool()]
        )