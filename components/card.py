from prefab_ui.components import (
    Card,
    CardHeader,
    CardTitle,
    CardFooter,
    CardContent,
    P,
)

def project_card(
    coffee_name: str = "Untitled",
    price: float = 0.0,
    quantity: int = 0
):
    with Card(): 
        with CardHeader():
            CardTitle(coffee_name)
        with CardContent():
            P(f"Price: {price}")
        with CardFooter():
            P(f"Stock: {quantity}")


