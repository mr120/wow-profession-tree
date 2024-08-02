import sqlite3
import csv
from prettytable import PrettyTable

conn = sqlite3.connect('wow_profession_tree.db')
cur = conn.cursor()

# query = '''
# 	select 
# 		sl.SpellID, 
# 		ptl.LabelID, 
# 		ptl.ID, 
# 		ptl.ProfessionTraitID, 
# 		pt.TraitDefinitionID, 
# 		td.OverrideName_lang, 
# 		td.OverrideDescription_lang, 
# 		--tne.ID as TraitNodeEntryID, 
# 		tntne.TraitNodeID, 
# 		pte.ID as pteID, 
# 		pte._Index,
# 		tne.MaxRanks,
# 		pe.Amount, 
# 		pet.Name_lang

# 	from spelllabel sl
# 	inner join professiontraitXlabel ptl on ptl.LabelID = sl.LabelID
# 	inner join professiontrait pt on pt.ID = ptl.ProfessionTraitID
# 	inner join traitdefinition td on td.ID = pt.TraitDefinitionID
# 	inner join traitnodeentry tne on tne.TraitDefinitionID = pt.TraitDefinitionID
# 	inner join traitnodeXtraitnodeentry tntne on tntne.TraitNodeEntryID = tne.ID

# 	-- join trait x effect
# 	-- on professiontraitID
# 	-- this will be many to one
# 	-- order by _index

# 	join professiontraitXeffect pte on pte.ProfessionTraitID = ptl.ProfessionTraitID

# 	-- join professioneffect
# 	-- on id

# 	join professioneffect pe on pe.ID = pte.ProfessionEffectID

# 	-- join professioneffectype
# 	-- on id or enumID

# 	inner join professioneffecttype pet on pet.EnumID = pe.ProfessionEffectTypeEnumID

# 	--where sl.SpellID = 367615
# 	order by sl.SpellID, ptl.LabelID, pte.ID, pte._Index
# 	--limit 20
# '''

query = '''
	select
		sl.SpellID as SpellID,
        tntne.TraitNodeID,
		COALESCE(tc.TraitNodeID, tntne.TraitNodeID) as ParentTraitNodeID,
		--tntne.ID as tntneID,
		--tne.ID as tneID,
		--tc.ID as tcID,
		--td.ID as tdID,
		--pt.ID as ptID,
		--ptl.ID as ptlID,
		--pte.ID as pteID,
		--tngtn.TraitNodeGroupID,
		--tntne._Index as tntneIndex,
		--pte._Index as pteIndex,
		--tngtn._Index as tngtnIndex,
		td.OverrideName_lang as NodeName,
		--substr(td.OverrideDescription_lang, 0, 125) as TraitDescrip,
		td.OverrideDescription_lang as TraitDescrip,
		tne.MaxRanks,
		pe.Amount,
		pet.Name_lang as Stat

	from traitnodeXtraitnodeentry tntne
	inner join traitnodegroupXtraitnode tngtn on tntne.TraitNodeID = tngtn.TraitNodeID

	left join traitnodeXtraitcond tntc on tntne.TraitNodeID = tntc.TraitNodeID
	left join traitcond tc on tntc.TraitCondID = tc.ID

	left join traitnodeentry tne on tntne.TraitNodeEntryID = tne.ID
	inner join traitdefinition td on tne.TraitDefinitionID = td.ID

	inner join professiontrait pt on tne.TraitDefinitionID = pt.TraitDefinitionID
	inner join professiontraitXlabel ptl on pt.ID = ptl.ProfessionTraitID
	inner join spelllabel sl on ptl.LabelID = sl.LabelID

	left join professiontraitXeffect pte on pt.ID = pte.ProfessionTraitID
	left join professioneffect pe on pte.ProfessionEffectID = pe.ID
	inner join professioneffecttype pet on pe.ProfessionEffectTypeEnumID = pet.EnumID

	--where sl.SpellID = 435382
	group by pt.ID, pte.ID, sl.SpellID
	order by sl.SpellID, ParentTraitNodeID, tc.SpentAmountRequired
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
    writer.writerow(column_names)
    writer.writerows(rows)

print(f'The query results have been exported to {csv_file_path}.')