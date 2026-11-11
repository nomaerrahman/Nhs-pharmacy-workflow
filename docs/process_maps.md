# Process maps

Swimlane maps of how a walk-in prescription moves through a community pharmacy today, and how it moves after the recommended changes (A + B). Each lane is a role.

## Current process (AS-IS)

```mermaid
flowchart LR
    subgraph P[Patient]
        P1([Arrives with prescription<br/>or to collect a repeat]) --> P2{Repeat already<br/>bagged?}
        P9([Leaves with medicine])
    end
    subgraph D[Dispenser]
        D1[Find EPS token,<br/>label items] --> D2[Pick and assemble]
        D5[Hand out and<br/>counsel on use]
    end
    subgraph PH[Pharmacist]
        PH1[Clinical check] --> PH2[Accuracy check]
        PH3[Pharmacy First / NMS /<br/>BP consultations]
    end
    P2 -- No: 40% of repeats --> D1
    P2 -- Yes --> D5
    D2 --> PH1
    PH2 --> D5
    D5 --> P9
    PH3 -. competes for the same<br/>pharmacist time .- PH1
```

**Pain points**

1. **The pharmacist is the bottleneck.** They do the clinical check, the accuracy check and every consultation, so at a busy pharmacy they are busy 99% of the day.
2. **Repeats are assembled on demand.** 40% of patients collecting a repeat prescription wait for it to be made up, adding to the queue at peak times.
3. **Consultations and checking compete.** Every Pharmacy First consultation pauses checking, so prescriptions back up behind it.

## Redesigned process (TO-BE: A + B)

```mermaid
flowchart LR
    subgraph P[Patient]
        P1([Arrives]) --> P2{Repeat already<br/>bagged?}
        P9([Leaves with medicine])
    end
    subgraph D[Dispenser]
        D0[Pre-assemble repeats<br/>in quiet periods]
        D1[Label items] --> D2[Pick and assemble]
        D5[Hand out]
    end
    subgraph ACT[Accuracy checking technician]
        A1[Accuracy check]
    end
    subgraph PH[Pharmacist]
        PH1[Clinical check only]
        PH3[Consultations]
    end
    P2 -- No: 5% of repeats --> D1
    P2 -- Yes: 95% --> D5
    D2 --> PH1 --> A1 --> D5
    D0 --> PH1
    D5 --> P9
```

**What changes**

- **A. Pre-assemble repeats:** repeat prescriptions arrive by EPS days before collection, so they are made up in quiet periods. 95% are ready when the patient arrives.
- **B. Accuracy checking technician (ACT):** a registered pharmacy technician with accuracy-checking accreditation takes over the final accuracy check. The pharmacist keeps the clinical check, so pharmacist time goes to consultations.
