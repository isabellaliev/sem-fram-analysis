import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('el_tiempo_articles.csv')
df['combined_text'] = df['title'].fillna('') + ' ' + df['keywords'].fillna('')
df['text_lower'] = df['combined_text'].str.lower()

search_terms = {
    'farc': ['farc', 'farc-ep'],
    'paz': ['paz'],
    'guerrillero': ['guerrillero', 'guerrilleros'],
    'excombatiente': ['excombatiente', 'excombatientes', 'ex combatiente', 'ex-combatiente'],
    'víctima': ['víctima', 'víctimas', 'victima', 'victimas']
}

# counting
results = {}
for term, variations in search_terms.items():
    mask = df['text_lower'].str.contains('|'.join(variations), na=False, regex=True)
    results[term] = mask.sum()

print(f"Total articles analyzed: {len(df)}")
print("\nTerm Frequency")
for term, count in results.items():
    percentage = (count/len(df))*100
    print(f"{term}: {count} articles ({percentage:.1f}%)")

# visualization
plt.figure(figsize=(10, 6))
plt.bar(results.keys(), results.values(), color='steelblue')
plt.title('Term Frequency in Colombian Peace Process Coverage\nEl Tiempo (2016-2023)', fontsize=14)
plt.xlabel('Terms', fontsize=12)
plt.ylabel('Number of Articles (n=31)', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('term_frequency.png', dpi=300)
print("\n✓ Visualization saved as 'term_frequency.png'")
plt.show()

# findings
print("\nKey Observations")
farc_pct = (results['farc']/len(df))*100
excom_pct = (results['excombatiente']/len(df))*100
print(f"'FARC' dominates coverage ({farc_pct:.1f}%), while reintegration")
print(f"terminology ('excombatiente') appears in only {excom_pct:.1f}% of articles.")