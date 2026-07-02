import logging
from typing import Annotated
from langchain_core.language_models.chat_models import agenerate_from_stream
from fastmcp import FastMCP
from fastmcp import Context
from pydantic import BaseModel, Field
from prefab_ui.app import PrefabApp
from prefab_ui.components import Column, Heading
from prefab_ui.components.charts import BarChart, ChartSeries
from prefab_ui.components import (
    Grid,
)
from components.card import project_card





logging.basicConfig(level=logging.WARNING, format="%(asctime)s - %(message)s")
logger = logging.getLogger("PlantShop")
logger.setLevel(logging.INFO)

mcp = FastMCP("StoreMCP")


class PurchaseConfirmation(BaseModel):
    confirm: bool = Field(title="Confirm Purchase", description="Approve this transaction?")


INVENTORY = {
    "Ethiopian Yirgacheffe": { "price" : 3.50, "quantity": 40},
    "Colombian Supremo": {"price": 4.0, "quantity": 30},
    "Ca Phe Sai Gon": {"price": 4.0, "quantity": 30}
}




##################################################
# TOOLS
##################################################


@mcp.tool(app=True)
async def list_products() -> PrefabApp:
    with Grid(columns=3,gap=4) as view:
        for coffee_name in INVENTORY:
            project_card(coffee_name, price = INVENTORY[coffee_name]["price"],quantity= INVENTORY[coffee_name]["quantity"])         
    return PrefabApp(view=view)





@mcp.tool 
async def buy_product(
        product_name: Annotated[str, "Coffee name"],
        amount: Annotated[int, "Number of order"],
        ctx: Context,
) -> str:
    if amount <= 0:
        return "Error: Number of order should be positive"
    if product_name not in INVENTORY or INVENTORY[product_name]["quantity"] < amount:
        return "Error: We don't sell that coffee, please choose another one"

    total = amount * INVENTORY[product_name]["price"]
    response = await ctx.elicit(
        message=f"Buy {amount} x {product_name} for {total}?",
        response_type=PurchaseConfirmation
    )
    if response.action != "accept" or not response.data.confirm:
        return "Purchase Cancelled."
    INVENTORY[product_name]["quantity"] -= amount
    
    return "Buying Successfully!!!"

        



@mcp.tool(app=True)
async def show_inventory_chart() -> PrefabApp:
    data = []
    for i in INVENTORY:
        data.append({"product": i, "quantity": INVENTORY[i]["quantity"]})
    
    with Column(gap=4, css_class="p-6") as view:
        Heading("Inventory Levels")
        BarChart(
            data=data,
            series=[ChartSeries(data_key="quantity", label="In stock")],
            x_axis="product"
        )
    return PrefabApp(view=view)

if __name__ == "__main__":
    logger.info("Store MCP server starting (HTTP mode on port 8420)")
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8420)



