import logging
from typing import Annotated

from langchain_core.language_models.chat_models import agenerate_from_stream

from fastmcp import FastMCP

logging.basicConfig(level=logging.WARNING, format="%(asctime)s - %(message)s")
logger = logging.getLogger("PlantShop")
logger.setLevel(logging.INFO)

mcp = FastMCP("StoreMCP")


INVENTORY = {
    "Ethiopian Yirgacheffe": { "price" : 3.50, "quantity": 40},
    "Colombian Supremo": {"price": 4.0, "quantity": 30},
    "Ca Phe Sai Gon": {"price": 4.0, "quantity": 30}
}

@mcp.tool
async def list_products() -> Annotated:
    results = []
    for i in INVENTORY:
        results.append(i)
    return results

@mcp.tool 
async def buy_product(
        product_name: Annotated[str, "Coffee name"],
        amount: Annotated[int, "Number of order"]
) -> str:
    if amount <= 0:
        return "Error: Number of order should be positive"
    if product_name in INVENTORY and INVENTORY[product_name]["quantity"] >= amount:
        INVENTORY[product_name]["quantity"] -= amount
        return "Buying Successfully!!!"
    return "Error: We don't sell that coffee, please choose another one"
        

 
if __name__ == "__main__":
    logger.info("Store MCP server starting (HTTP mode on port 8420)")
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8420)



