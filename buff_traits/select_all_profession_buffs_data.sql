select
    se.SpellID as SpellID,
    se.EffectAura as EffectAura,
    sm.SpellID as AffectedSpellID,
    case
        when se.EffectAura = 511 then pe.Amount * se.EffectBasePointsF
        when se.EffectAura = 98 then se.EffectBasePointsF
    end as Amount,
    case
        when se.EffectAura = 511 then pet.Name_lang
        when se.EffectAura = 98 then sl.DisplayName_lang
    end as Stat,
    --when the hex value contains IS_TRADESKILL, is a recipe
    case
        WHEN CAST(substr(printf('0x%X', sm.Attributes_0), -2) AS INTEGER) - 20 = 0 THEN 1
        WHEN (CAST(substr(printf('0x%X', sm.Attributes_0), -2) AS INTEGER) - 10) - 20 = 0 THEN 1
        ELSE 0
    end as FlagCondition


from spelleffect se
left join professioneffect pe on se.EffectMiscValue_0 = pe.ID
left join professioneffecttype pet on pe.ProfessionEffectTypeEnumID = pet.EnumID
left join skillline sl on se.EffectMiscValue_0 = sl.ID


inner join spelllabel spl on se.SpellID = spl.SpellID
inner join spelllabel spl2 on spl.LabelID = spl2.LabelID
inner join spellmisc sm on spl2.SpellID = sm.spellID and FlagCondition = 1

-- if aura = 511,
-- its a prof stat increase,
-- value is pe.Amount * se.EffectBasePointsF
-- EffectMiscValue_0 is ID of ProfessionEffect
-- stat is pet.Name_lang
where se.EffectAura = 511 or se.EffectAura = 98
-- if aura = 98,
-- its a prof skill increase,
-- value is se.EffectBasePointsF
-- EffectMiscValue_0 is ID of SkillLine
-- skill is sl.DisplayName_lang

order by se.SpellID, se.EffectIndex