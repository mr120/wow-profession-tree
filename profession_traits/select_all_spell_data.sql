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

from TraitNodeXTraitNodeEntry tntne

 -- fetch the parent node information
 -- must left join as parent nodes themselves are not returned here
left join TraitNodeXTraitCond tntc on tntne.TraitNodeID = tntc.TraitNodeID

-- fetch to get the order of TraitNodes via SpentAmountRequired
left join TraitCond tc on tntc.TraitCondID = tc.ID

-- fetch the number of ranks available
-- 1 rank for traits
-- many ranks for parent nodes
inner join TraitNodeEntry tne on tntne.TraitNodeEntryID = tne.ID

-- fetch trait text labels
inner join TraitDefinition td on tne.TraitDefinitionID = td.ID
inner join ProfessionTrait pt on tne.TraitDefinitionID = pt.TraitDefinitionID

-- fetch all the spells(recipes) this trait is usable on
inner join ProfessionTraitXLabel ptl on pt.ID = ptl.ProfessionTraitID
inner join SpellLabel sl on ptl.LabelID = sl.LabelID

-- fetch the amount of stat awarded per rank
left join ProfessionTraitXEffect pte on pt.ID = pte.ProfessionTraitID
left join ProfessionEffect pe on pte.ProfessionEffectID = pe.ID

-- fetch the stat name
-- left join gets nodes that let you craft new recipes etc..
-- inner join only for stat boosting only
inner join ProfessionEffectType pet on pe.ProfessionEffectTypeEnumID = pet.EnumID

-- fetch the profession ids
left join SkillLineAbility sla on sl.SpellID = sla.Spell

--where sl.SpellID = 435318 -- debugging

group by pt.ID, pte.ID, sl.SpellID
order by sl.SpellID, ParentTraitNodeID, tc.SpentAmountRequired