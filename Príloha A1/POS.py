import json
import pandas as pd

df = pd.read_excel('vstup.xlsx')

with open ('vstup_GT.json', "r",encoding="utf8") as f:
	data= json.load(f)

for x in data:
	for col in df.columns:
		if x["wordtype"]["slovakName"] in col:
			df[col] += 1
print(df)
df_transposed = df.T
df_transposed.to_excel('vystup2.xlsx')
# Closing file
f.close()