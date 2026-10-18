import numpy as np
import gametree


def test_generate_possible_stocks(output_count = False, output_combos = False):
    assets = np.array([2500, 1500, 1500, 1500, 500, 2000, 0])  # Example asset counts and whole-dollar cash
    prices = np.array([100, 150, 110, 105, 50, 25])  # Raw prices; divide by 100 for dollar cost

    possible_stocks = gametree.generate_possible_stocks(assets, prices)

    # Check that the output is a list of numpy arrays
    assert isinstance(possible_stocks, list), "Output should be a list."
    for combo in possible_stocks:
        assert isinstance(combo, np.ndarray), "Each combination should be a numpy array."

    # Check that the total dollar value is consistent
    total_dollars = gametree.calc_asset_value(assets, prices)
    assert isinstance(total_dollars, (int, np.integer)), "Total value should be an integer."
    if(output_count):
        print(f"Total Combos: {len(possible_stocks)}")
        print(f"Total Value: {total_dollars}")
              
    for combo in possible_stocks:
        if(output_combos):
            print(f"Combination: {combo}, Total Value: {gametree.calc_asset_value(combo, prices)}")
        assert np.issubdtype(combo.dtype, np.integer), "Generated assets and dollars should be integers."
        assert combo[-1] >= 0, "Leftover dollars cannot be negative."
        assert np.isclose(gametree.calc_asset_value(combo, prices), total_dollars), "Total dollar value should match."

if __name__ == "__main__":
    test_generate_possible_stocks(output_count=True, output_combos=False)
    print("All tests passed.")