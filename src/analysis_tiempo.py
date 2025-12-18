import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('el_tiempo_articles.csv')

# combining text field from title + keywords
df['combined_text'] = df['title'].fillna('') + ' ' + df['keywords'].fillna('')
df['text_lower'] = df['combined_text'].str.lower()

# search terms and variations
search_terms = {
    'guerrillero': ['guerrillero', 'guerrilleros'],
    'excombatiente': ['excombatiente', 'excombatientes', 'ex combatiente', 'ex-combatiente'],
    'campesino': ['campesino', 'campesinos'],
    'víctima': ['víctima', 'víctimas', 'victima', 'victimas'],
    'paz': ['paz'],
    'violencia': ['violencia', 'violento', 'violenta'],
    'farc': ['farc', 'farc-ep']
}

# counting
results = {}
for term, variations in search_terms.items():
    mask = df['text_lower'].str.contains('|'.join(variations), na=False)
    results[term] = mask.sum()

print(f"Total articles: {len(df)}")
print("\nTerm frequencies:")
for term, count in results.items():
    percentage = (count/len(df))*100
    print(f"{term}: {count} articles ({percentage:.1f}%)")

# visualization
plt.figure(figsize=(10, 6))
plt.bar(results.keys(), results.values())
plt.title('Term Frequency in Colombian Post-Accord Press Discourse (2016-2023)')
plt.xlabel('Terms')
plt.ylabel('Number of Articles')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('term_frequency.png')
plt.show()
