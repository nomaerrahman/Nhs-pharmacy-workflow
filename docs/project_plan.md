# Project plan

A three-month pilot at one busy branch, then a decision on wider rollout.

## Pilot timeline

```mermaid
gantt
    title Pilot plan: pre-assembled repeats + accuracy checking technician
    dateFormat  YYYY-MM-DD
    axisFormat  %d %b
    section Prepare
    Baseline: time 50 prescriptions       :a1, 2027-01-04, 1w
    Update SOP and get superintendent sign-off :a2, after a1, 1w
    Recruit or second an accredited ACT   :a3, 2027-01-04, 6w
    section Pilot
    Pre-assembly of repeats live          :b1, after a2, 10w
    ACT accuracy checking live            :b2, after a3, 6w
    section Review
    Weekly wait-time report               :c1, after a2, 10w
    Re-run simulation with measured times :c2, after b2, 1w
    Go / no-go decision                   :milestone, c3, after c2, 0d
```

## Stakeholder map (power / interest)

| | Low interest | High interest |
| --- | --- | --- |
| **High power** | Area manager, NHS England commissioners (keep satisfied) | Superintendent pharmacist, pharmacy manager (manage closely) |
| **Low power** | Suppliers, head office IT (monitor) | Pharmacists, dispensers, patients (keep informed) |

## RAID log

| Type | Item | Owner | Response |
| --- | --- | --- | --- |
| Risk | ACT accuracy checks increase dispensing errors | Superintendent | Only GPhC-registered pharmacy technicians with ACT accreditation; pharmacist clinical check is never removed; error log reviewed monthly |
| Risk | Pre-assembled repeats are not collected, tying up stock | Manager | 14-day uncollected flag (user story 8) |
| Risk | Simulation assumptions don't match a real branch | Analyst | Time 50 real prescriptions at a pilot branch and re-run the model with measured times |
| Assumption | 55% of prescription forms are collected in person; 25% of those are new prescriptions waited for | Analyst | Validate during pilot |
| Assumption | One pharmacist on duty during all opening hours | Manager | Confirm against branch rota |
| Issue | London ICBs restructured on 1 Apr 2026, breaking trends by ICB | Analyst | Mapped all months to the current four-ICB structure |
| Dependency | Patient medication record system must record who did each check | IT | Confirm with system supplier before go-live |
