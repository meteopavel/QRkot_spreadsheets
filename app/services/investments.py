from datetime import datetime

from app.models.base import Investment


def process_investments(
    target_investment: Investment,
    source_investments: list[Investment],
) -> list[Investment]:
    """
    Распределить имеющиеся средства фонда на инвестиции.
    """
    updated_investments = []
    for source_investment in source_investments:
        investment_amount = min(
            source_investment.full_amount - source_investment.invested_amount,
            target_investment.full_amount - target_investment.invested_amount,
        )
        for updated_object in (source_investment, target_investment):
            updated_object.invested_amount += investment_amount
            if updated_object.full_amount == updated_object.invested_amount:
                updated_object.fully_invested = True
                updated_object.close_date = datetime.now()
        updated_investments.append(source_investment)
        if target_investment.fully_invested:
            break
    return updated_investments
