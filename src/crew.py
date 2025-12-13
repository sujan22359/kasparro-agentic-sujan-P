from crewai import Crew, Task, Process
from src.config.llm_logic import LLMFactory
from src.agents.parser_agent import ParserAgent
from src.agents.strategy_agent import StrategyAgent
from src.agents.writer_agent import WriterAgent
from src.models.schemas import ProductPage, FAQPage, ComparisonPage

class ContentGenCrew:
    def __init__(self):
        self.llm = LLMFactory.create_llm()

    def run(self, raw_text: str):
        parser = ParserAgent(self.llm)
        strategist = StrategyAgent(self.llm)
        writer = WriterAgent(self.llm)

        task_product = Task(
            description=f"Analyze text: {raw_text}. Extract Name, Price, Ingredients.",
            expected_output="A valid ProductPage JSON object.",
            agent=parser,
            output_pydantic=ProductPage 
        )

        task_faq = Task(
            description=f"Generate 20+ FAQs based on: {raw_text}.",
            expected_output="A valid FAQPage JSON object.",
            agent=strategist,
            output_pydantic=FAQPage
        )

        task_comparison = Task(
            description=f"Use the 'Market Competitor Database' tool to find competitors for: {raw_text}. Create a comparison table.",
            expected_output="A valid ComparisonPage JSON object.",
            agent=writer,
            output_pydantic=ComparisonPage
        )

        
        crew = Crew(
            agents=[parser, strategist, writer],
            tasks=[task_product, task_faq, task_comparison],
            process=Process.sequential,
            verbose=True,
            memory=False 
        )

        crew.kickoff()

        # --- THE FIX ---
        # If Pydantic is None (strict validation failed), return the RAW output.
        # This prevents the "NoneType" crash in app.py.
        return {
            "product_page": task_product.output.pydantic if task_product.output.pydantic else task_product.output.raw,
            "faq_page": task_faq.output.pydantic if task_faq.output.pydantic else task_faq.output.raw,
            "comparison_page": task_comparison.output.pydantic if task_comparison.output.pydantic else task_comparison.output.raw
        }