def format_currency_rule(amount_str: str) -> str:
    """Ensures price is consistently formatted."""
    if "Rs." not in amount_str:
        return f"Rs.{amount_str}"
    return amount_str

def generate_comparison_matrix(product_a: dict, product_b: dict) -> list:
    """
    Logic block to ensure A and B have matching keys for comparison.
    """
    common_keys = ["price", "key_ingredients", "benefits"]
    matrix = []
    
    for key in common_keys:
        row = {
            "feature": key.replace("_", " ").title(),
            "product_a": str(product_a.get(key, "N/A")),
            "product_b": str(product_b.get(key, "N/A"))
        }
        matrix.append(row)
    return matrix