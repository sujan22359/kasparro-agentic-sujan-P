from src.agents.parser_agent import ParserAgent
from src.agents.strategy_agent import StrategyAgent
from src.agents.content_agent import ContentAgent
import json
import os

class ContentAutomationGraph:
    def __init__(self):
        # Initialize Agents
        self.parser = ParserAgent("Parser-Agent")
        self.strategist = StrategyAgent("Strategy-Agent")
        self.writer = ContentAgent("Content-Agent")

    def run(self, raw_text: str, output_dir: str = "output"):
        """
        Executes the DAG (Directed Acyclic Graph) flow.
        Flow: Raw Text -> Parser -> Strategy -> Content -> JSON Files
        """
        print("--- Starting Automation Graph ---")
        
        # Node 1: Parse Data
        product_model = self.parser.execute(raw_text)
        
        # Node 2: Develop Strategy (Questions & Competitor)
        strategy_data = self.strategist.execute(product_model)
        
        # Node 3: Generate Content Pages
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        pages = ["product_page", "faq_page", "comparison_page"]
        
        for page_type in pages:
            # Node 4: Write Content
            page_content = self.writer.execute(product_model, strategy_data, page_type)
            
            # Save to File
            file_path = os.path.join(output_dir, f"{page_type}.json")
            with open(file_path, "w") as f:
                json.dump(page_content.dict(), f, indent=4)
            print(f"✔ Generated: {file_path}")
            
        print("--- Automation Graph Complete ---")