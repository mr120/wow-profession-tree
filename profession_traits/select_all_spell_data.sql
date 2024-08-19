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
    skl.ParentSkillLineID as ProfessionID,
    skl.ID as ProfessionExpansionID
    --pte.ID as pteID, -- debugging
    --pt.ID as ptID -- debugging

from SkillLineXTraitTree sltt

inner join TraitNode tn on sltt.TraitTreeID = tn.TraitTreeID
inner join TraitNodeXTraitNodeEntry tntne on tn.ID = tntne.TraitNodeID

-- fetch the profession ids
left join SkillLine skl on sltt.SkillLineID = skl.ID

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

-- fetch the amount of stat awarded per rank
left join ProfessionTraitXEffect pte on pt.ID = pte.ProfessionTraitID
left join ProfessionEffect pe on pte.ProfessionEffectID = pe.ID

-- fetch the stat name
-- left join gets nodes that let you craft new recipes etc..
-- inner join only for stat boosting only
inner join ProfessionEffectType pet on pe.ProfessionEffectTypeEnumID = pet.EnumID

-- fetch all the spells(recipes) this trait is usable on
inner join ProfessionTraitXLabel ptl on pt.ID = ptl.ProfessionTraitID
inner join SpellLabel sl on ptl.LabelID = sl.LabelID

--where sl.SpellID = 435318 -- debugging

where sltt.SkillLineID in (
    2822,
    2830,
    2823,
    2831,
    2827,
    2825,
    2829,
    2828,

    2872,
    2880,
    2871,
    2883,
    2875,
    2874,
    2879,
    2878
)

group by pt.ID, pte.ID, sl.SpellID
order by ProfessionExpansionID, sl.SpellID, ParentTraitNodeID, tc.SpentAmountRequired
