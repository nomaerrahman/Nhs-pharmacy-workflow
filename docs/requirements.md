# Requirements: user stories

Twelve user stories for the redesigned workflow, prioritised with MoSCoW. Acceptance criteria use Given / When / Then.

| # | Priority | User story | Acceptance criteria |
| --- | --- | --- | --- |
| 1 | Must | As a **dispenser**, I want a daily list of repeat prescriptions due for collection in the next 3 days, so that I can pre-assemble them in quiet periods. | Given EPS repeats with an expected collection date, when the pharmacy opens, then a list of items due within 3 days is shown, sorted by collection date. |
| 2 | Must | As a **patient collecting a repeat**, I want my medicine ready when I arrive, so that I don't have to wait. | Given a repeat flagged as assembled and checked, when I give my name at the counter, then it is handed out without re-assembly. |
| 3 | Must | As a **pharmacist**, I want the accuracy check done by an accredited technician, so that I have time for clinical checks and consultations. | Given an item has passed clinical check, when it reaches the checking bench, then an ACT can sign off the accuracy check and the record shows who checked it. |
| 4 | Must | As a **superintendent pharmacist**, I want every accuracy check by an ACT logged against a clinically checked prescription, so that the process stays within the pharmacy's standard operating procedure. | Given an ACT accuracy check, when it is recorded, then the system blocks sign-off unless a pharmacist clinical check exists for that prescription. |
| 5 | Must | As a **pharmacist**, I want consultation bookings visible alongside the dispensing queue, so that I can plan checking around them. | Given booked Pharmacy First consultations, when I view the workload screen, then both the consultation slots and the number of items waiting for clinical check are shown. |
| 6 | Should | As a **patient**, I want a text message when my prescription is ready, so that I only come in once. | Given a prescription marked ready, when it is bagged, then the patient receives a message within 5 minutes if they opted in. |
| 7 | Should | As a **pharmacy manager**, I want a daily report of average and 95th-percentile waiting time, so that I can see if the change is working. | Given waiting times recorded at hand-in and hand-out, when the day ends, then the report shows both measures by hour. |
| 8 | Should | As a **dispenser**, I want uncollected bagged repeats flagged after 14 days, so that stock isn't tied up. | Given a bag ready for 14 days, when the daily list runs, then it appears on a returns-to-stock list. |
| 9 | Should | As a **pharmacy manager**, I want staff rotas to show ACT cover for every opening hour, so that accuracy checks never fall back to the pharmacist. | Given the weekly rota, when an hour has no ACT cover, then it is highlighted before the rota is published. |
| 10 | Could | As a **patient**, I want to choose a collection time slot online, so that I avoid the busiest hours. | Given online ordering, when I pick a slot, then busy hours show as limited availability. |
| 11 | Could | As an **area manager**, I want the waiting-time report compared across branches, so that I can roll the process out where it helps most. | Given reports from several branches, when I open the dashboard, then branches are ranked by 95th-percentile wait. |
| 12 | Won't (this phase) | As a **pharmacist**, I want automated dispensing robots for fast-moving lines. | Out of scope: capital cost and floor space need a separate business case. |
