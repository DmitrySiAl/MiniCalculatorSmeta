from pydantic import BaseModel, Field, computed_field, ConfigDict

class EstimateItemCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    quantity: float = Field(gt=0)
    unit_price: float = Field(gt=0)

class EstimateItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    quantity: float
    unit_price: float

    @computed_field
    def total_item_price(self) -> float:
        return round(self.quantity * self.unit_price, 2)

class EstimateResponse(BaseModel):
    items: list[EstimateItemResponse]
    markup_percent: float
    subtotal: float
    grand_total: float