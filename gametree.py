import numpy as np

PRICE_DIVISOR = 100

SHARE_UNIT = 500


'''
centralize assets + prices -> value. This allows us to change the magic number "20" to something else if we want to change the scale of the game.
'''
def calc_asset_value(assets, prices, indx = None):
    if indx is not None and (indx < 0 or indx >= len(prices) - 1):
        raise ValueError("Index out of bounds for assets/prices array.")
    elif indx is None:
        return np.sum(assets[:-1] * prices) // PRICE_DIVISOR + assets[-1]
    else:
        return assets[indx] * prices[indx] // PRICE_DIVISOR

'''
given an "assets" array (S_1, S_2 ..., S_6, Dollars) and generates a list of all possible other "assets" arrays that can be reached. 
'''
def generate_possible_stocks(assets, prices):
    # For now, generate the total dollar value the player has, and then generate all possible combinations of stocks that can be bought with that amount of money.
    # In reality, the number of stocks is low, and the value of any stock is between 0.05x and 1.95x any other stock, so we should look at removing one to buy another. 


    # Each stock * it's price, plus dollars
    total_dollars = calc_asset_value(assets, prices)

    asset_combos = []

    def calculate_assets(combination, end_value):
        # Initialize an array to hold the new asset values
        new_assets = np.zeros(len(prices) + 1, dtype=int)
        new_assets[:-1] = combination  # Set the stock counts based on the combination

        total_cost = calc_asset_value(new_assets, prices)  # Calculate the total cost of the combination
        
        # Update the dollar amount after purchases
        new_assets[-1] = end_value - total_cost
        assert new_assets[-1] >= 0, "Generated asset combination exceeds available value."
        
        return new_assets

    ### this is an unbounded knapsack problem.
    def backtrack(remaining_capacity, current_combination, first_stock=0):
        # Base case: store a copy of the valid path
        asset_combos.append(calculate_assets(current_combination, total_dollars))
        
        # Add stocks in nondecreasing index order to avoid duplicate purchase orders.
        for i in range(first_stock, len(prices)):
            stock_cost = SHARE_UNIT * prices[i] // PRICE_DIVISOR
            if remaining_capacity >= stock_cost:
                current_combination[i] += SHARE_UNIT
                backtrack(remaining_capacity - stock_cost, current_combination, i)
                current_combination[i] -= SHARE_UNIT

    backtrack(total_dollars, np.zeros(len(prices), dtype=int))
    return asset_combos