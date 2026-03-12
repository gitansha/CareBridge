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

<img width="601" height="386" alt="image" src="https://github.com/user-attachments/assets/a7785744-57b7-432b-ba61-5b3581952e46" />


## **Future Scope**

### **Advanced Features**
- **Department Routing**:
  - Route emergency cases to appropriate departments.
- **Summarization**:
  - Summarize patient records using **AWS Bedrock**.
- **Multilingual Support**:
  - Add support for Mandarin and other languages.

---
