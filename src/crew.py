from crewai import Agent, Task, Crew, Process
from src.config.llm_logic import LLMFactory
from src.models.schemas import ProductPage, FAQPage, ComparisonPage

class ContentGenCrew:
    def __init__(self):
        self.llm = LLMFactory.create_llm()

    def run(self, raw_text: str):
        # --- AGENTS ---
        parser_agent = Agent(
            role='Senior Data Analyst',
            goal='Extract structured product data from raw text with 100% accuracy.',
            backstory='You are an expert at structuring messy data. You pay attention to every detail.',
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )

        strategy_agent = Agent(
            role='Content Strategist',
            goal='Brainstorm user questions and competitor analysis based on product data.',
            backstory='You are a marketing genius who knows exactly what customers ask.',
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )

        writer_agent = Agent(
            role='Senior Copywriter',
            goal='Write compelling, SEO-optimized web content.',
            backstory='You write engaging product descriptions that convert visitors into buyers.',
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )

        # --- TASKS ---
        task_product = Task(
            description=f"Analyze text: '{raw_text}'. Extract Name, Price, Ingredients. Write a compelling description. Structure as ProductPage.",
            expected_output="A structured ProductPage object.",
            agent=parser_agent,
            output_pydantic=ProductPage
        )

        task_faq = Task(
            description=f"Based on '{raw_text}', generate 20+ FAQs (Safety, Usage, Results). Structure as FAQPage.",
            expected_output="A structured FAQPage object.",
            agent=strategy_agent,
            output_pydantic=FAQPage
        )

        task_comparison = Task(
            description=f"Based on '{raw_text}', create a competitor comparison table. Structure as ComparisonPage.",
            expected_output="A structured ComparisonPage object.",
            agent=writer_agent,
            output_pydantic=ComparisonPage
        )

        # --- CREW EXECUTION ---
        crew = Crew(
            agents=[parser_agent, strategy_agent, writer_agent],
            tasks=[task_product, task_faq, task_comparison],
            process=Process.sequential,
            verbose=True
        )

        crew.kickoff()

        def get_safe_output(task):
            # 1. Try Pydantic Model (Best case)
            if hasattr(task.output, 'pydantic') and task.output.pydantic is not None:
                return task.output.pydantic
            
            # 2. Try JSON Dict (Second best)
            if hasattr(task.output, 'json_dict') and task.output.json_dict is not None:
                return task.output.json_dict
            
            # 3. Fallback to Raw String (Worst case, but better than crashing)
            return {
                "raw_content": str(task.output.raw),
                "note": "AI generated content but strict parsing failed. Raw text preserved."
            }

        return {
            "product_page": get_safe_output(task_product),
            "faq_page": get_safe_output(task_faq),
            "comparison_page": get_safe_output(task_comparison)
        }