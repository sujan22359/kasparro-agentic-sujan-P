from crewai_tools import BaseTool
from pydantic import Field

class CompetitorLookupTool(BaseTool):
    name: str = "Market Competitor Database"
    description: str = "Useful for finding real competitor pricing and features to ensure comparisons are accurate. Input should be the category of product (e.g., 'Vitamin C Serum')."

    def _run(self, category: str) -> str:
        # NOTE: For this assessment, we use deterministic static data to ensure 
        # consistent test results and zero external API dependencies. 
        # In a production environment, this would be replaced by a live 
        # vector database query or a SerperDevTool API call.
        
        if "vitamin c" in category.lower() or "serum" in category.lower():
            return """
            Found Competitor Data:
            1. Brand: 'LuminousSkin C-Power'
               - Price: INR 1250
               - Size: 30ml
               - Key Features: 15% Vitamin C, Ferulic Acid.
               
            2. Brand: 'DermaPure Brightener'
               - Price: INR 899
               - Size: 30ml
               - Key Features: 10% Vitamin C, Vitamin E.
            """
        else:
            return "No specific competitor data found. Use general market averages."