import pandas as pd
import matplotlib.pyplot as plt

#Loading data
df = pd.read_csv('el_tiempo_articles.csv')

#Creating a combined text
df['combined_text'] = df['title'].fillna('') + ' ' + df['keywords'].fillna('')
df['text_lower'] = df['combined_text'].str.lower()

#Searching terms
search_terms = {
    'farc': ['farc', 'farc-ep', 'FARC'],
    'paz': ['paz'],
    'guerrillero': ['guerrillero', 'guerrilleros'],
    'excombatiente': ['excombatiente', 'excombatientes', 'ex combatiente', 'ex combatientes', 'ex-combatiente'],
    'víctima': ['víctima', 'víctimas', 'victima', 'victimas']
}

#Adding binary columns for each term
for term, variations in search_terms.items():
    df[f'has_{term}'] = df['text_lower'].str.contains('|'.join(variations), na=False, regex=True)

#Temporal Analysis
print("Term Frecuency per Year\n")

#Grouping by year and count 
temporal_results = {}
for term in search_terms.keys():
    by_year = df.groupby('year')[f'has_{term}'].sum()
    temporal_results[term] = by_year
    print(f"{term.upper()}:")
    print(by_year)
    print ()

#PERIOD COMPARISON 
# Converting year to string to be safe
df['year'] = df['year'].astype(str)

# Assigning periods
df['period'] = df['year'].apply(lambda x: '2016-2018' if x in ['2016', '2017', '2018'] 
                                          else '2022-2023' if x in ['2022', '2023'] 
                                          else 'other')

# Checking how many articles per period
print("\n=== Articles per period ===")
print(df['period'].value_counts())
print()

print("**Comparison: 2016-2018 vs 2022-2023**\n")

period_comparison = []
for term in search_terms.keys():
    by_period = df[df['period'] != 'other'].groupby('period')[f'has_{term}'].agg(['sum', 'count'])
    by_period['percentage'] = (by_period['sum'] / by_period['count'] * 100).round(1)

    print(f"{term.upper()}:")
    print(by_period)
    print()

    #Storing for visualization
    for period in by_period.index:
        period_comparison.append({
            'term': term,
            'period': period,
            'count': by_period.loc[period, 'sum'],
            'percentage': by_period.loc[period, 'percentage'],
        })
            
                                                                                    

#Saving results
comparison_df = pd.DataFrame(period_comparison)
comparison_df.to_csv('temporal_comparison.csv', index=False)

#VISUALIZATION 1: Terms Over Time
fig, ax = plt.subplots(figsize=(12,6))

for term in search_terms.keys():
    years = temporal_results[term].index.astype(str)
    counts = temporal_results[term].values
    ax.plot(years, counts, marker='o', label=term, linewidth=2)

ax.set_xlabel('Year', fontsize=12)
ax.set_ylabel('Number of Articles', fontsize=12)
ax.set_title('Term Frecuency Over Time (2016-2023)', fontsize=14)
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('temporal_trends.png', dpi=300)
print("Visualization saved")
plt.show()

#VISUALIZATION 2: Period Comparison
comparison_pivot = comparison_df.pivot(index='term', columns='period', values='percentage')

fig, ax = plt.subplots(figsize=(10, 6))
comparison_pivot.plot(kind='bar', ax=ax, color=['steelblue', 'coral'])
ax.set_xlabel('Terms', fontsize=12)
ax.set_ylabel('Percentage of Articles', fontsize=12)
ax.set_title('Term Frequency: Early Post-Accord (2016-2018) vs Petro Era (2022-2023)', fontsize=14)
ax.legend(title='Period')
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
plt.tight_layout()
plt.savefig('period_comparison.png', dpi=300)
print("✓ Visualization saved as 'period_comparison.png'")
plt.show()

#Findings
print("\n Key Observations")
farc_early = comparison_df[(comparison_df['term']=='farc') & (comparison_df['period']=='2016-2018')]['percentage'].values[0]
farc_petro = comparison_df[(comparison_df['term']=='farc') & (comparison_df['period']=='2022-2023')]['percentage'].values[0]

print(f"FARC mentions: {farc_early}% (2016-2018) → {farc_petro}% (2022-2023)")

if 'excombatiente' in comparison_df['term'].values:
    excom_early = comparison_df[(comparison_df['term']=='excombatiente') & (comparison_df['period']=='2016-2018')]['percentage'].values
    excom_petro = comparison_df[(comparison_df['term']=='excombatiente') & (comparison_df['period']=='2022-2023')]['percentage'].values
    if len(excom_early) > 0 and len(excom_petro) > 0:
        print(f"Excombatiente mentions: {excom_early[0]}% (2016-2018) → {excom_petro[0]}% (2022-2023)")