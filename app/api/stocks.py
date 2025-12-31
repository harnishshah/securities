import os
from fastapi import APIRouter, Depends, HTTPException
from massive import RESTClient  # The updated SDK for Massive.com
from app.db.snowflake import get_snowflake_conn
#from app.db.snowflake import get_snowflake_conn
from datetime import datetime, timedelta

router = APIRouter()

# Initialize the Massive Client using your API Key
MASSIVE_CLIENT = RESTClient(os.getenv("MASSIVE_API_KEY"))


def apply_custom_formula(price, strike, rating):
    """
    Your Phase 4 Formula:
    Example: (Rating * 10) + (Distance from Strike)
    """
    score = (rating * 15) + (100 - abs(price - strike))
    return round(score, 2)


@router.get("/score/{ticker}")
async def get_stock_intelligence(ticker: str, rating: int, conn=Depends(get_snowflake_conn)):
    # 1. Validation: We only track stocks with Morningstar Rating >= 3
    if rating < 3:
        return {"message": "Rating too low for automated tracking", "score": None}

    try:
        # 2. Pull Weekly Expiry Options from Massive (Polygon)
        # We look for the next Friday expiry
        today = datetime.now()
        next_friday = (today + timedelta((4 - today.weekday()) % 7)).strftime('%Y-%m-%d')

        # Get the 'At The Money' (ATM) price for the stock
        snapshot = MASSIVE_CLIENT.get_snapshot_ticker(ticker)
        current_price = snapshot.day.close if snapshot.day else 0

        # Fetch options contracts for this ticker and expiry
        contracts = MASSIVE_CLIENT.list_options_contracts(
            underlying_ticker=ticker,
            expiration_date=next_friday,
            limit=5
        )

        # 3. Calculate Personalized Score
        # For this example, we take the first available call contract
        results = []
        for contract in contracts:
            score = apply_custom_formula(current_price, contract.strike_price, rating)

            # 4. Store the results in Snowflake for pattern intelligence
            cursor = conn.cursor()
            cursor.execute(f"""
                INSERT INTO SCORES (TICKER, RATING, FORMULA_SCORE, TIMESTAMP)
                VALUES ('{ticker}', {rating}, {score}, CURRENT_TIMESTAMP())
            """)

            results.append({
                "strike": contract.strike_price,
                "expiry": contract.expiration_date,
                "score": score
            })

        return {
            "ticker": ticker,
            "current_price": current_price,
            "weekly_analysis": results
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Data Fetch Error: {str(e)}")