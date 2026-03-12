# **AI Chatbot for Hospital Departments**

## **Overview**
This project aims to build an AI-powered chatbot for hospital departments to retrieve patient history, allergies, medical records, and other critical information. The chatbot will include department-specific workflows, voice support, and scalable architecture to allow future expansion.

---

## **MVP Features**

### **Core Features**
1. **Patient Search**:
   - Search by `FIN`, `name`, or `DOB`.
   - Example: "Find a patient with the last 4 digits of FIN 1234."
2. **Medical Records Retrieval**:
   - Fetch visit history, allergies, and prescriptions.
   - Example: "What allergies does John Doe have?"
3. **Voice Support**:
   - **Speech-to-Text (STT)**: Convert voice input to text using **Amazon Transcribe**.
   - **Text-to-Speech (TTS)**: Convert chatbot responses to speech using **Amazon Polly**.
4. **Department-Specific Quick Actions**:
   - Tailored workflows for Emergency, Pharmacy, Radiology, etc.

---

## **Additional Features**
5. **Appointment Management**:
   - Book and view appointments.
   - Example: "Book an appointment for John Doe with Dr. Smith on March 15th at 10 AM."
6. **Drug Interaction Queries**:
   - Check interactions between two drugs.
   - Example: "What are the interactions between Drug A and Drug B?"
7. **ICD Code Mapping**:
   - Map conditions to ICD-10/11 codes.
   - Example: "What is the ICD-10 code for diabetes?"
8. **Analytics Dashboard**:
   - Visualize patient data and trends (e.g., number of patients by department).

---

## **Architecture**

### **Frontend**
- **Streamlit**:
  - Chat interface for text and voice interactions.
  - Analytics dashboard for visual insights.

### **Backend**
- **Amazon Lex**:
  - Handles conversational AI with intents for:
    - Patient search.
    - Medical record retrieval.
    - Appointment management.
    - Drug interaction queries.
    - ICD code mapping.
  - Slots for capturing user input (e.g., `PatientID`, `DrugName`, `Date`).
- **AWS Lambda**:
  - Executes backend logic for:
    - Querying ElasticSearch.
    - Booking appointments.
    - Fetching drug interactions and ICD codes.
- **ElasticSearch**:
  - Stores:
    - Patient data.
    - Medical records.
    - Appointments.
  - Provides analytics via aggregations.
- **External APIs**:
  - WHO ICD-10/11 API.
  - Drug Interaction API.

### **Voice Support**
- **Amazon Transcribe**:
  - Converts voice input into text.
- **Amazon Polly**:
  - Converts chatbot responses into speech.

---

## **Implementation Timeline (3 Hours)**

### **Hour 1: Backend Setup**
1. Set up **ElasticSearch** indices:
   - `patients`, `medical_records`, `appointments`.
2. Create Lambda functions:
   - `search_patient`: Queries ElasticSearch for patient data.
   - `fetch_records`: Retrieves visit history, allergies, and prescriptions.
   - `book_appointment`: Handles appointment booking.
   - `check_drug_interaction`: Queries the Drug Interaction API.
   - `get_icd_code`: Queries the WHO API.
3. Configure **Amazon Lex** intents and slots.

---

### **Hour 2: Frontend and Voice Integration**
1. Build a **Streamlit** chat interface:
   - Add text input and microphone button.
   - Display chatbot responses and analytics.
2. Integrate **Amazon Transcribe** for voice input.
3. Integrate **Amazon Polly** for voice output.

---

### **Hour 3: Testing and Deployment**
1. Test chatbot functionality:
   - Validate intents and slot filling in Amazon Lex.
   - Test API responses for all features.
2. Deploy backend on **AWS Lambda** and **API Gateway**.
3. Deploy frontend on **Streamlit Cloud**.

---

## **Future Scope**

### **Advanced Features**
- **Department Routing**:
  - Route emergency cases to appropriate departments.
- **Summarization**:
  - Summarize patient records using **AWS Bedrock**.
- **Multilingual Support**:
  - Add support for Mandarin and other languages.

### **Scalability**
- **Deployment Enhancements**:
  - Migrate to a containerized architecture (e.g., ECS or EKS).
  - Use **CloudFront** for global content delivery.
- **AI/ML Integration**:
  - Deploy models for predictive analytics (e.g., risk scoring).

---

## **Final Architecture Diagram**

```
Frontend (Streamlit)
    |
    |---> Amazon Lex (Chatbot)
              |
              |---> AWS Lambda (Backend Logic)
                        |
                        |---> ElasticSearch (Data Storage)
                        |
                        |---> Amazon Polly (TTS)
                        |
                        |---> Amazon Transcribe (STT)
```
