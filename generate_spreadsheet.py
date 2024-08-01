import sqlite3
import csv
from prettytable import PrettyTable

conn = sqlite3.connect('wow_profession_tree.db')
cur = conn.cursor()

#professioneffect
#professiontraitXeffect
#traitnodeXtraitnodeentry
#professioneffecttype
#professiontraitXlabel
#traitnodeentry
#professiontrait
#traitdefinition
#spelllabel

query = '''
	select 
		sl.SpellID, 
		ptl.LabelID, 
		ptl.ID, 
		ptl.ProfessionTraitID, 
		pt.TraitDefinitionID, 
		td.OverrideDescription_lang, 
		--tne.ID as TraitNodeEntryID, 
		tntne.TraitNodeID, 
		pte.ID as pteID, 
		pte._Index,
		tne.MaxRanks,
		pe.Amount, 
		pet.Name_lang

	from spelllabel sl
	inner join professiontraitXlabel ptl on ptl.LabelID = sl.LabelID
	inner join professiontrait pt on pt.ID = ptl.ProfessionTraitID
	inner join traitdefinition td on td.ID = pt.TraitDefinitionID
	inner join traitnodeentry tne on tne.TraitDefinitionID = pt.TraitDefinitionID
	inner join traitnodeXtraitnodeentry tntne on tntne.TraitNodeEntryID = tne.ID

	-- join trait x effect
	-- on professiontraitID
	-- this will be many to one
	-- order by _index

	join professiontraitXeffect pte on pte.ProfessionTraitID = ptl.ProfessionTraitID

	-- join professioneffect
	-- on id

	join professioneffect pe on pe.ID = pte.ProfessionEffectID

	-- join professioneffectype
	-- on id or enumID

	inner join professioneffecttype pet on pet.EnumID = pe.ProfessionEffectTypeEnumID

	--where sl.SpellID = 367615
	order by sl.SpellID, ptl.LabelID, pte.ID, pte._Index
	--limit 20
'''

cur.execute(query)
rows = cur.fetchall()

column_names = [description[0] for description in cur.description]

conn.close()

table = PrettyTable()

table.field_names = column_names
for row in rows:
	table.add_row(row)

#print(table)

csv_file_path = 'profTalentData.csv'
with open(csv_file_path, 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(column_names)  # Write the header
    writer.writerows(rows)         # Write the data

print(f'The query results have been exported to {csv_file_path}.')