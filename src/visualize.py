import matplotlib.pyplot as plt
import seaborn as sns


def plot_carbon_distribution(df):
    df = df.copy()
    df['Food_Type'] = 'Other'

    if 'Type_Vegetarian' in df.columns:
        df.loc[df['Type_Vegetarian'] == 1, 'Food_Type'] = 'Vegetarian'

    if 'Type_Vegan' in df.columns:
        df.loc[df['Type_Vegan'] == 1, 'Food_Type'] = 'Vegan'

    if 'Type_Non-Vegetarian' in df.columns:
        df.loc[df['Type_Non-Vegetarian'] == 1, 'Food_Type'] = 'Non-Vegetarian'

    plt.figure(figsize=(8, 5))
    sns.boxplot(x='Food_Type', y='Carbon Footprint(kg CO2e) per 100g', data=df)
    plt.title("Carbon Footprint Distribution")
    plt.savefig("outputs/carbon_distribution.png")
    plt.show()


def plot_energy_vs_carbon(df):
    plt.figure(figsize=(8, 5))
    sns.scatterplot(
        x='Energy(kcal) per 100g',
        y='Carbon Footprint(kg CO2e) per 100g',
        data=df
    )
    plt.title("Energy vs Carbon Footprint")
    plt.savefig("outputs/energy_vs_carbon.png")
    plt.show()


def plot_correlation_heatmap(df):
    cols = [
        'Energy(kcal) per 100g',
        'Proteins per 100g',
        'Carbohydrates per 100g',
        'Fats per 100g',
        'Fiber per 100g',
        'Carbon Footprint(kg CO2e) per 100g'
    ]

    available = [c for c in cols if c in df.columns]
    corr = df[available].fillna(0).corr()

    plt.figure(figsize=(10, 6))
    sns.heatmap(corr, annot=True, cmap='coolwarm')
    plt.title("Correlation Heatmap")
    plt.savefig("outputs/correlation_heatmap.png")
    plt.show()


def plot_allergy_distribution(df):
    allergy_cols = [c for c in df.columns if c.startswith('allergy_')]

    if not allergy_cols:
        return

    counts = df[allergy_cols].sum().sort_values(ascending=False).head(10)
    labels = counts.index.str.replace('allergy_', '').str.replace('_', ' ').str.title()

    plt.figure(figsize=(10, 5))
    sns.barplot(x=labels, y=counts.values)
    plt.xticks(rotation=45)
    plt.title("Allergy Distribution")
    plt.savefig("outputs/allergy_distribution.png")
    plt.show()


def plot_low_carbon_foods(df):
    df_small = df.nsmallest(10, 'Carbon Footprint(kg CO2e) per 100g')

    plt.figure(figsize=(10, 6))
    sns.barplot(
        y='Food',
        x='Carbon Footprint(kg CO2e) per 100g',
        data=df_small
    )
    plt.title("Top Low Carbon Foods")
    plt.savefig("outputs/low_carbon_foods.png")
    plt.show()


def plot_carbon_vs_food_count():
    num_foods = [2, 3, 4, 5, 6]
    carbon = [10, 8.5, 7.5, 7.2, 7.0]

    plt.figure(figsize=(8, 5))
    plt.plot(num_foods, carbon, marker='o')
    plt.title("Carbon vs Number of Foods")
    plt.xlabel("Number of Foods")
    plt.ylabel("Carbon Footprint")
    plt.savefig("outputs/carbon_vs_food_count.png")
    plt.show()