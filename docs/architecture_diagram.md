# Architecture Diagram

This diagram shows the Work Agent system flow.

~~~mermaid
flowchart TD
    A[Message variable or WhatsApp message] --> B[Automate writes work_inbox.txt]
    B --> C[Automate creates run_work_parser.flag]
    C --> D[Termux:Tasker runs run_reminder_check.sh]

    D --> E[import_work_inbox.py]
    E --> F[imported_messages.txt]

    F --> G[process_imported_work.py]
    G --> H[pending_job.json]
    G --> I[pending_job_display.txt]

    I --> J[Automate confirmation dialog]

    J -->|Confirm| K[confirm.flag]
    J -->|Reject| L[reject.flag]
    J -->|Edit| M[edit_request.txt]

    K --> N[process_job_confirmations.py]
    L --> N
    M --> N

    N --> O[jobs.json]
    N --> P[travel_time.py]

    P --> Q[location_overrides.json]
    P --> R[travel_cache.json]
    P --> S[Google Routes API]

    N --> T[travel_review.txt]
    T --> U[Automate travel review dialog]

    U -->|Travel looks good| V[alarm_request.txt]
    U -->|Wrong destination| W[Plus Code input]
    W --> X[edit_request.txt with location_override]
    X --> Y[confirm.flag]
    Y --> N

    V --> Z[Automate reads alarm_request.txt]
    Z --> AA[Automate creates Android alarm]
    AA --> AB[Cleanup temporary shared files]
~~~

## Summary

Automate controls Android interaction.

Python controls parsing, memory, travel calculations, and alarm request generation.

Shared files connect the two systems.
