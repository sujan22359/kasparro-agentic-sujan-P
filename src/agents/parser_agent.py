from crewai import Agent

class ParserAgent(Agent):
    def __init__(self, llm):
        super().__init__(
            role='Senior Data Analyst',
            goal='Extract factual product data with 100% schema compliance.',
            backstory="You are a rigid data analyst. You never guess.",
            llm=llm, 
            verbose=True,
            allow_delegation=False
        )