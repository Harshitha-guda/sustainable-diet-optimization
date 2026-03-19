from pulp import LpProblem, LpVariable, lpSum, LpMinimize, value, LpStatus

def get_user_input():
    return {
        'calories': 1500,
        'protein': 50,
        'carbs': 250,
        'fats': 55,
        'fiber': 30,
        'allergies': ['nut'],
        'diet_type': 'vegan',
        'preferred_regions': ['south']
    }

def apply_constraints(df, user):
    filtered_df = df.copy()

    for allergy in user['allergies']:
        col = f'allergy_{allergy}'
        if col in filtered_df.columns:
            filtered_df = filtered_df[filtered_df[col] == 0]

    if user['diet_type']:
        col = f'Type_{user["diet_type"].capitalize()}'
        if col in filtered_df.columns:
            filtered_df = filtered_df[filtered_df[col] == 1]

    return filtered_df

def rank_by_nutrition(df, user, top_n=50):
    df = df.copy()
    df['nutrition_score'] = (
        abs(df['Energy(kcal) per 100g'] - user['calories']) +
        abs(df['Proteins per 100g'] - user['protein']) +
        abs(df['Carbohydrates per 100g'] - user['carbs']) +
        abs(df['Fats per 100g'] - user['fats']) +
        abs(df['Fiber per 100g'] - user['fiber'])
    )
    return df.sort_values('nutrition_score').head(top_n)

def optimize_meal(df, user):
    prob = LpProblem("Meal_Optimization", LpMinimize)

    foods = df['Food'].tolist()
    food_vars = {f: LpVariable(f'choose_{i}', cat='Binary') for i, f in enumerate(foods)}

    energy = dict(zip(df['Food'], df['Energy(kcal) per 100g']))
    protein = dict(zip(df['Food'], df['Proteins per 100g']))
    carbs = dict(zip(df['Food'], df['Carbohydrates per 100g']))
    fats = dict(zip(df['Food'], df['Fats per 100g']))
    fiber = dict(zip(df['Food'], df['Fiber per 100g']))
    carbon = dict(zip(df['Food'], df['Carbon Footprint(kg CO2e) per 100g']))

    prob += lpSum([food_vars[f] * carbon[f] for f in foods])

    prob += lpSum([food_vars[f] * energy[f] for f in foods]) >= user['calories']
    prob += lpSum([food_vars[f] * protein[f] for f in foods]) >= user['protein']
    prob += lpSum([food_vars[f] * carbs[f] for f in foods]) >= user['carbs']
    prob += lpSum([food_vars[f] * fats[f] for f in foods]) >= user['fats']
    prob += lpSum([food_vars[f] * fiber[f] for f in foods]) >= user['fiber']

    prob += lpSum([food_vars[f] for f in foods]) <= 5

    prob.solve()

    if LpStatus[prob.status] != "Optimal":
        return [], 0, 0

    selected = [f for f in foods if food_vars[f].varValue == 1]

    total_carbon = sum(carbon[f] for f in selected)
    total_energy = sum(energy[f] for f in selected)

    return selected, total_carbon, total_energy