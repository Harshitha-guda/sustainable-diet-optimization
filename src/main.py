import pandas as pd

from src.optimize import (
    get_user_input,
    apply_constraints,
    rank_by_nutrition,
    optimize_meal
)

from src.visualize import (
    plot_carbon_distribution,
    plot_energy_vs_carbon,
    plot_correlation_heatmap,
    plot_allergy_distribution,
    plot_low_carbon_foods,
    plot_carbon_vs_food_count
)


def main():
    try:
        # Load dataset
        df = pd.read_csv("data/nutrition_cf_preprocessed.csv")

        # Get user input
        user = get_user_input()

        # Apply constraints
        filtered_df = apply_constraints(df, user)

        if filtered_df.empty:
            print("No foods available after applying constraints.")
            return

        # Rank foods
        ranked_df = rank_by_nutrition(filtered_df, user)

        # Optimize
        selected_foods, total_carbon, total_energy = optimize_meal(ranked_df, user)

        if not selected_foods:
            print("No optimal solution found.")
            return

        # Print results
        print("\nOptimized Meal Plan:")
        for food in selected_foods:
            print(f"- {food}")

        print(f"\nTotal Carbon Footprint: {total_carbon:.2f} kg CO2e")
        print(f"Total Energy: {total_energy:.2f} kcal")

        # Visualizations (ALL)
        plot_carbon_distribution(df)
        plot_energy_vs_carbon(df)
        plot_correlation_heatmap(df)
        plot_allergy_distribution(df)
        plot_low_carbon_foods(df)
        plot_carbon_vs_food_count()

    except FileNotFoundError:
        print("Dataset not found. Check data folder.")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()