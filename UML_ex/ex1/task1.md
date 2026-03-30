```mermaid

classDiagram
    class Patient {
        +String patientId
        +String name
        +String password
        +String email
        +submitProblem(description: String)
        +payBill(amount: Float)
    }

    class Organizer {
        +String organizerId
        +String name
        +String password
        +maintainDatabase()
        +issueCredentials(userType: String)
        +forwardPrescription()
    }

    class Doctor {
        +String doctorId
        +String name
        +String password
        +String specialty
        +reviewProblem(problemId: String)
        +providePrescription()
    }

    Patient "1" --> "1..*" Organizer : Submits problem to
    Organizer "1" --> "1..*" Doctor : Consults
    Doctor "1" --> "1..*" Organizer : Returns prescription to
    Organizer "1" --> "1..*" Patient : Forwards prescription to

```
