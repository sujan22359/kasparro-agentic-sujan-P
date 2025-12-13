from crewai import Agent

class StrategyAgent(Agent):
    def __init__(self, llm):
        super().__init__(
            role='Content Strategist',
            goal='Generate high-value customer FAQs.',
            backstory="You are a marketing expert focused on user intent.",
            llm=llm,  
            verbose=True,
            allow_delegation=False
        )