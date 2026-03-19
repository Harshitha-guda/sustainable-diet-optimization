import pandas as pd
import numpy as np

def preprocess_data(input_path, output_path):
    df = pd.read_csv(input_path)
    df.columns = df.columns.str.strip()

    df['Total Weight (gms)'] = df['Total Weight (gms)'].replace(0, np.nan)

    nutrients = ['Energy(kcal)', 'Proteins', 'Carbohydrates', 'Fats', 'Fiber', 'Carbon Footprint(kg CO2e)']

    for nutrient in nutrients:
        df[f'{nutrient} per 100g'] = np.where(
            df['Total Weight (gms)'] > 0,
            (df[nutrient] / df['Total Weight (gms)']) * 100,
            0
        )

    df.fillna(0, inplace=True)

    df = pd.get_dummies(df, columns=['Region', 'Type', 'Category'])

    df['Allergy'] = df['Allergy'].fillna('').str.lower()

    allergy_set = set()
    for entry in df['Allergy']:
        for item in entry.split(','):
            allergy_set.add(item.strip())

    allergy_set.discard('no-allergies')

    for allergy in allergy_set:
        col_name = f'allergy_{allergy.replace(" ", "_")}'
        df[col_name] = df['Allergy'].str.contains(allergy).astype(int)

    drop_cols = ['Serving', 'Total Weight (gms)', 'Energy(kcal)', 'Proteins',
                 'Carbohydrates', 'Fats', 'Fiber', 'Carbon Footprint(kg CO2e)',
                 'Allergy', 'Ingredients']

    df.drop([col for col in drop_cols if col in df.columns], axis=1, inplace=True)

    df.to_csv(output_path, index=False)
    print("Preprocessing complete!")

if __name__ == "__main__":
    preprocess_data("data/nutrition_cf.csv", "data/nutrition_cf_preprocessed.csv")