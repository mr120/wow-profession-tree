import sqlite3
import csv
from prettytable import PrettyTable

if __name__ == '__main__':
    conn = sqlite3.connect('wow_profession_tree.db')
    cur = conn.cursor()

    query = '''
        select
            sl.SpellID as SpellID,
            tntne.TraitNodeID,
            COALESCE(tc.TraitNodeID, tntne.TraitNodeID) as ParentTraitNodeID,
            td.OverrideName_lang as NodeName,
            td.OverrideDescription_lang as TraitDescrip,
            tne.MaxRanks,
            pe.Amount,
            pet.Name_lang as Stat,
            pe.ModifiedCraftingReagentSlotID,
            sla.SkillLine as ProfessionID,
            sla.SkillupSkillLineId as ProfessionExpansionID
            --pte.ID as pteID, -- debugging
            --pt.ID as ptID -- debugging

        from traitnodeXtraitnodeentry tntne

        -- fetch the parent node information
        -- must left join as parent nodes themselves are not returned here
        left join traitnodeXtraitcond tntc on tntne.TraitNodeID = tntc.TraitNodeID

        -- fetch to get the order of TraitNodes via SpentAmountRequired
        left join traitcond tc on tntc.TraitCondID = tc.ID

        -- fetch the number of ranks available
        -- 1 rank for traits
        -- many ranks for parent nodes
        inner join traitnodeentry tne on tntne.TraitNodeEntryID = tne.ID

        -- fetch trait text labels
        inner join traitdefinition td on tne.TraitDefinitionID = td.ID
        inner join professiontrait pt on tne.TraitDefinitionID = pt.TraitDefinitionID

        -- fetch all the spells(recipes) this trait is usable on
        inner join professiontraitXlabel ptl on pt.ID = ptl.ProfessionTraitID
        inner join spelllabel sl on ptl.LabelID = sl.LabelID

        -- fetch the amount of stat awarded per rank
        left join professiontraitXeffect pte on pt.ID = pte.ProfessionTraitID
        left join professioneffect pe on pte.ProfessionEffectID = pe.ID

        -- fetch the stat name
        -- left join gets nodes that let you craft new recipes etc..
        -- inner join only for stat boosting only
        inner join professioneffecttype pet on pe.ProfessionEffectTypeEnumID = pet.EnumID

        -- fetch the profession ids
        left join skilllineability sla on sl.SpellID = sla.Spell

        --where sl.SpellID = 435318 -- debugging

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