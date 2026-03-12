# Hackathon Problem Statement: MediGuard AI

## **Project Name: MediGuard AI - Intelligent Healthcare Reception Assistant**

---

## 🎯 **Problem Statement**

### **The Challenge**
Hospital receptionists in Singapore face multiple critical challenges daily:

1. **Patient Identification Crisis**: Patients provide incomplete or varied information (sometimes NRIC + name, sometimes phone + DOB, sometimes just "I came last week"). Current systems lack intelligent matching, leading to:
   - Wrong patient record retrieval (safety risk)
   - Long queues due to manual verification
   - Frustrated patients repeating information

2. **Information Overload**: Receptionists manually navigate 5+ different systems to:
   - Find patient records (EMR)
   - Check medication history (Pharmacy system)
   - View appointment slots (Scheduling system)
   - Verify insurance coverage (Billing system)
   - Access allergy information (Clinical notes)

3. **Language Barriers**: Singapore's multilingual population (English, Mandarin, Malay, Tamil) causes communication gaps, especially with elderly patients.

4. **Critical Information Gaps**: Receptionists lack clinical context to:
   - Identify urgent cases (chest pain patient with cardiac history)
   - Detect medication conflicts (patient on blood thinners scheduling surgery)
   - Spot overdue screenings (diabetic patient due for HbA1c)
   - Prevent duplicate appointments across hospitals

5. **Security & Compliance Risks**: 
   - No foolproof way to prevent unauthorized access
   - Incomplete audit trails
   - PDPA compliance burden

### **The Opportunity**
Build an AI-powered receptionist assistant that transforms hospital front-desk operations from reactive and fragmented to proactive and intelligent.

---

## 🚀 **Proposed Solution: MediGuard AI**

### **Core Innovation**
An **Agentic RAG-powered conversational assistant** leveraging **AWS Bedrock + Elastic OpenSearch** that:
1. **Intelligently matches patients** with 100% accuracy using multi-identifier fuzzy matching
2. **Proactively surfaces critical clinical insights** before the receptionist even asks
3. **Orchestrates multi-system data** into a single conversational interface
4. **Ensures security** through role-based access, anomaly detection, and comprehensive audit trails

### **Key Features**

#### **🔍 1. Hyper-Accurate Patient Matching (Core)**
- **Multi-tier verification algorithm**: NRIC (100%), Phone+DOB (95%), Name+DOB+Phone (90%)
- **Phonetic matching** for name variations: "Tan Ah Kow" = "Tan Ah Kao" = "Than A Cow"
- **Fuzzy logic** handles incomplete data: "91234567" matches "+65-9123-4567"
- **Confidence scoring** with human-in-the-loop verification for <95% matches
- **Real-time disambiguation**: Shows top 3 candidates when multiple matches found

**Elastic Feature**: OpenSearch k-NN vector search + phonetic analyzers + multi-field boolean queries

#### **⚠️ 2. Proactive Clinical Alerts (Novel)**
When patient record is retrieved, AI agent automatically surfaces:
- 🚨 **Critical Alerts**: "Patient is allergic to Penicillin (anaphylaxis risk)"
- 💊 **Medication Warnings**: "Patient on Warfarin - flag for surgical procedures"
- 📅 **Overdue Screenings**: "Diabetic patient - HbA1c test overdue by 2 months"
- 🔄 **Follow-up Reminders**: "Missed cardiology follow-up from Feb 10 visit"
- 📉 **Risk Indicators**: "3 emergency visits in past month - possible chronic condition"

**Elastic Feature**: OpenSearch aggregations + anomaly detection ML + nested queries

#### **🧠 3. Intelligent Triage & Routing (Creative)**
Receptionist describes symptoms → AI classifies urgency and routes appropriately:
- **Emergency**: "Chest pain + cardiac history" → Immediate Emergency Dept alert
- **Urgent**: "High fever 3 days + diabetic" → Same-day appointment
- **Routine**: "Annual checkup" → Normal scheduling

**AWS Feature**: Bedrock Agent with multi-step reasoning + Claude 3.5 Sonnet's clinical understanding

#### **👨‍👩‍👧‍👦 4. Family Health Context (Innovative)**
- Detect family clusters: "3 members at same address visited with flu symptoms"
- Family medical history: "Father has diabetes, patient at high risk - recommend screening"
- Shared allergies: "Mother allergic to penicillin - verify for child"
- Appointment coordination: "Book all 3 children for vaccination same day"

**Elastic Feature**: Graph-based relationships + aggregations across patient records

#### **🌐 5. Multilingual Voice Support (Accessibility)**
- Real-time speech-to-text in 4 languages (English, Mandarin, Malay, Tamil)
- Accent-aware transcription for Singapore context
- Auto-translation: Receptionist speaks English → Patient hears Mandarin
- Elderly-friendly: Dictate NRIC instead of typing

**AWS Feature**: Amazon Transcribe + Amazon Translate + Bedrock

#### **📊 6. Predictive Analytics Dashboard (Data-Driven)**
- **No-show prediction**: "Patient has 70% likelihood of missing appointment"
- **Wait time forecasting**: "Current wait: 45 min | Expected in 30 min: 20 min"
- **Resource optimization**: "Expected 200 walk-ins tomorrow - recommend +2 staff"
- **Seasonal trends**: "Flu cases up 40% this week - alert infection control"

**Elastic Feature**: OpenSearch ML anomaly detection + time-series analysis + forecasting

#### **🔐 7. Foolproof Security & Compliance (Critical)**
- **Role-based access control**: Receptionists see demographics only, not clinical notes
- **Field-level security**: OpenSearch FLS masks sensitive data (lab results, imaging)
- **Purpose-based access**: Every query requires justification ("Appointment scheduling")
- **Real-time anomaly detection**: Alert if receptionist accesses >30 patients/hour
- **Comprehensive audit trail**: Every access logged with user, timestamp, purpose, fields viewed
- **NRIC masking**: Display S1234***A instead of full NRIC

**Elastic Feature**: OpenSearch security (RBAC, FLS, DLS) + anomaly detection + audit logging

#### **💊 8. Medication Interaction Checker (Safety)**
- Cross-hospital medication reconciliation
- Drug-drug interaction warnings: "Aspirin + Warfarin = bleeding risk"
- Allergy cross-check: "Patient allergic to Penicillin - proposed Amoxicillin is contraindicated"
- Pre-procedure alerts: "Patient on blood thinner - consult surgeon before operation"

**Integration**: NEHR medication database + clinical decision support rules

#### **📅 9. Conversational Appointment Scheduling (UX)**
Natural language booking:
- Receptionist: "Book follow-up with Dr. Lim next week Tuesday afternoon"
- AI: Checks availability, patient history, insurance coverage, conflicts
- AI: "Dr. Lim available 2pm Tuesday. Patient has active insurance. Booking confirmed."

**AWS Feature**: Bedrock Agent tool orchestration + function calling

#### **🔍 10. Fraud & Abuse Detection (Governance)**
- Detect duplicate appointments across hospitals: "Patient has 3 appointments same day different hospitals"
- Insurance fraud patterns: "10 same-diagnosis claims from this patient in 1 month"
- Unusual access patterns: "Receptionist A accessed all cardiology VIP patients today"
- Staff collusion detection: "3 staff members accessed same patient within 5 minutes"

**Elastic Feature**: OpenSearch ML anomaly detection + correlation queries

---

## 🏗️ **Technical Architecture**

### **Technology Stack**
```
Frontend:    React.js + TailwindCSS (conversational UI)
Backend:     AWS Lambda (serverless functions)
AI/Agent:    AWS Bedrock (Claude 3.5 Sonnet) - Agentic RAG orchestration
Search:      Amazon OpenSearch Service - Patient records + vector search
Database:    Amazon Aurora PostgreSQL - Structured medical records
Integration: NEHR API (simulated for hackathon)
Security:    AWS WAF, Cognito, KMS, CloudTrail
Monitoring:  CloudWatch + OpenSearch Dashboards
```

### **Data Flow**
```
Patient Call → Receptionist → Web Interface → API Gateway
    ↓
AWS Bedrock Agent (Orchestrator)
    ↓
┌─────────────┬──────────────┬─────────────┐
│  Lambda     │  OpenSearch  │   Aurora    │
│  (Tools)    │  (RAG KB)    │  (Records)  │
└─────────────┴──────────────┴─────────────┘
    ↓
Response with:
- Patient record (masked NRIC)
- Clinical alerts
- Medication list
- Appointment history
- Proactive recommendations
```

### **Elastic OpenSearch Usage**
1. **Patient Index**: Multi-field search with k-NN vectors for semantic matching
2. **Visit Index**: Nested documents for historical visit analysis
3. **Medication Index**: Real-time medication interaction checking
4. **Audit Index**: Comprehensive access logging with anomaly detection
5. **Analytics**: ML-powered dashboards for wait time prediction, no-show forecasting

### **AWS Bedrock Agent Role**
- **Orchestration**: Decides which tools to call based on user query
- **Reasoning**: Multi-step logic (e.g., "find patient → check allergies → warn about proposed medication")
- **Context Management**: Maintains conversation state across multiple queries
- **Safety**: Enforces security rules (minimum 2 identifiers, confidence thresholds)

---

## 🎨 **What Makes This Creative & Novel?**

### **1. Agentic RAG - Not Just RAG**
- Traditional RAG: Query → Retrieve docs → Generate answer
- **Our Agentic RAG**: Query → Reason → Plan → Execute tools → Verify → Respond
- Example: "Find patient with chest pain last week" → Agent plans: (1) Parse time reference, (2) Search by symptom + date, (3) Retrieve matches, (4) Rank by relevance, (5) Ask for verification

### **2. Proactive Intelligence - Not Reactive Search**
- Doesn't wait for receptionist to ask about allergies/medications
- Automatically surfaces critical information: "⚠️ Patient on blood thinner - flag for surgery"
- Predictive insights: "70% likelihood patient will no-show - send reminder SMS"

### **3. Multi-Modal Context - Not Single Patient View**
- Family health context: "Father diabetic → Flag child for screening"
- Cross-hospital patterns: "Patient visited 3 hospitals with same complaint this week"
- Temporal patterns: "3 emergency visits past month → Suggest care coordinator"

### **4. Security as Feature - Not Afterthought**
- Real-time anomaly detection using Elastic ML
- Purpose-based access (can't just browse, must justify)
- Audit trail visualization dashboard for compliance officers

### **5. Conversational UX - Not Form-Filling**
- Natural language: "Show me the elderly Chinese patient who came for diabetes checkup last Tuesday"
- Disambiguation: "I found 3 patients - which department: Cardiology, Endocrinology, or Emergency?"
- Multi-turn conversation with context retention

---

## 📈 **Impact & Value Proposition**

### **For Receptionists**
- ⏱️ **70% faster** patient lookup (3 min → 50 sec)
- 🧠 **Zero cognitive load**: One interface replaces 5+ systems
- 🌐 **Language barrier eliminated**: Real-time translation
- ✅ **Confidence boost**: AI validates patient match before proceeding

### **For Patients**
- ⚡ **Shorter wait times**: Faster check-in process
- 🔒 **Privacy protection**: Strong security prevents unauthorized access
- 🏥 **Safer care**: Proactive alerts catch medication conflicts
- 💬 **Better communication**: Speak native language

### **For Hospital Administration**
- 💰 **Cost savings**: Reduce duplicate tests, optimize staffing
- 📊 **Data-driven decisions**: Predictive analytics for resource allocation
- ✅ **Compliance**: 100% audit trail for PDPA/HIPAA
- 🚫 **Fraud prevention**: Detect abuse patterns early

### **For Healthcare System (Singapore)**
- 🏥 **Cross-hospital coordination**: Prevent duplicate appointments
- 📈 **Population health**: Detect disease outbreaks via cluster analysis
- 🎯 **Preventive care**: Identify high-risk patients for early intervention

---

## 🏆 **Hackathon Success Metrics**

### **Functionality** (40%)
- ✅ Patient search with 100% accuracy using multi-identifier matching
- ✅ Proactive clinical alerts surfaced automatically
- ✅ Role-based access control with audit logging
- ✅ Conversational UI with natural language queries
- ✅ Real-time anomaly detection for security

### **Creativity** (30%)
- 🌟 Agentic RAG with multi-step reasoning (not just retrieval)
- 🌟 Family health context and cross-patient pattern detection
- 🌟 Intelligent triage with urgency classification
- 🌟 Predictive analytics (no-show, wait times, disease trends)

### **Novelty** (30%)
- 💡 First healthcare receptionist assistant with proactive clinical intelligence
- 💡 Multi-modal context (patient + family + temporal + cross-hospital)
- 💡 Security as core feature with real-time anomaly detection
- 💡 Purpose-based access control (not just RBAC)

---

## ⚙️ **6-Hour Hackathon Implementation Plan**

### **Hour 1: Infrastructure Setup**
- Deploy AWS CloudFormation stack (OpenSearch + Aurora + Lambda + Bedrock)
- Use pre-configured templates from AWS Serverless Application Repository
- Seed Aurora with synthetic Singapore patient data (50 patients, 200 visits)
- Configure OpenSearch indices with mappings

### **Hour 2: Core Patient Search**
- Implement patient search Lambda function with scoring algorithm
- Configure OpenSearch queries (exact, fuzzy, phonetic, vector)
- Test multi-identifier matching (NRIC, phone+DOB, name+DOB+phone)
- Build simple disambiguation logic

### **Hour 3: Bedrock Agent Setup**
- Create Bedrock Agent with Claude 3.5 Sonnet
- Define 4 tools: search_patient, get_visit_history, get_medications, check_appointments
- Write agent instructions with security rules
- Test agent orchestration with sample queries

### **Hour 4: Proactive Features**
- Implement clinical alerts Lambda (allergies, medication warnings, overdue screenings)
- Add anomaly detection rules in OpenSearch (access patterns, duplicate appointments)
- Build medication interaction checker with basic rules
- Test alert triggering workflow

### **Hour 5: Frontend & Demo Scenarios**
- Build React conversational UI with chat interface
- Integrate with API Gateway + Bedrock Agent
- Implement NRIC masking and confidence display
- Create 5 demo scenarios (exact match, ambiguous, multiple matches, clinical alert, security alert)

### **Hour 6: Polish & Presentation**
- Add OpenSearch dashboard for analytics (access logs, wait time predictions)
- Record demo video showing all features
- Prepare pitch deck highlighting creativity and novelty
- Test end-to-end flows

### **MVP Feature Priority**
**Must-Have (Core)**:
1. ✅ Multi-identifier patient search with scoring
2. ✅ Bedrock Agent orchestration
3. ✅ Proactive clinical alerts (allergies, medications)
4. ✅ Role-based access control
5. ✅ Conversational UI

**Nice-to-Have (Stretch)**:
6. 🎯 Family health context
7. 🎯 Intelligent triage
8. 🎯 Anomaly detection dashboard
9. 🎯 Multilingual support (if time permits)

---

## 🎬 **Demo Script**

### **Scenario 1: Perfect Match**
**Receptionist**: "Find patient S1234567A"
**AI**: ✅ "Patient found: Tan Ah Kow (S1234***A), DOB: 15 May 1980
⚠️ **ALERT**: Patient is allergic to Penicillin (severe - anaphylaxis)
💊 Current medications: Aspirin 100mg, Atorvastatin 20mg
📅 Last visit: 10 Feb 2026 - Cardiology - Dr. Lim Kim Seng"

### **Scenario 2: Ambiguous Query**
**Receptionist**: "Looking for John Tan who came last week"
**AI**: "🔍 I found 3 patients named John Tan with recent visits:
1. John Tan Wei Ming (S9876***B) - Visited 12 Feb, Cardiology
2. John Tan Keng Seng (S5432***C) - Visited 14 Feb, Orthopedics  
3. John Tan Hock Seng (S3210***D) - Visited 15 Feb, Emergency
Can you provide phone number or date of birth to confirm?"

### **Scenario 3: Proactive Alert**
**Receptionist**: "Patient is here for surgery consultation"
**AI**: "🚨 **CRITICAL ALERT**: Patient is on Warfarin (blood thinner)
❗ Surgical risk - recommend consulting surgeon before scheduling
📋 Last prescription: 10 Feb 2026 by Dr. Lim Kim Seng
🩺 Reason: Post-cardiac event anticoagulation"

### **Scenario 4: Intelligent Triage**
**Receptionist**: "Patient calling about chest pain, has cardiac history"
**AI**: "🚨 **EMERGENCY - IMMEDIATE ACTION REQUIRED**
Patient has unstable angina diagnosis (10 Feb 2026)
Current medications include cardiac drugs
→ Recommend: Direct to Emergency Department immediately
→ Alerting: ED team of incoming high-risk patient"

### **Scenario 5: Security Alert**
**Dashboard**: "⚠️ Anomaly Detected: User REC-12345 accessed 35 patient records in past hour (normal: 8-12)
Access pattern: All cardiology VIP patients
Recommendation: Flag for supervisor review"

---

## 📊 **Expected Outcomes**

### **Quantifiable Improvements**
- **Patient lookup time**: 3 minutes → 50 seconds (70% reduction)
- **Identification accuracy**: 85% → 100% (zero wrong patient incidents)
- **Systems accessed per query**: 5 systems → 1 unified interface
- **Security incidents**: Historical 2-3/month → 0 (proactive anomaly detection)
- **Language barrier incidents**: 20/week → 0 (multilingual support)

### **Qualitative Benefits**
- Receptionist satisfaction: Reduced stress, clearer workflow
- Patient safety: Fewer medication errors, allergy incidents
- Compliance: Complete audit trail, PDPA-ready
- Innovation: First AI agent specifically for healthcare reception

---

## 🌟 **Why This Will Win**

### **Functionality**: ⭐⭐⭐⭐⭐
- Working end-to-end demo with real patient search, alerts, security
- Multiple complex features integrated seamlessly
- Addresses real-world hospital pain points

### **Creativity**: ⭐⭐⭐⭐⭐
- Agentic RAG (not just basic retrieval)
- Proactive intelligence (not reactive search)
- Multi-modal context (family, temporal, cross-hospital)
- Security as feature (anomaly detection, purpose-based access)

### **Novelty**: ⭐⭐⭐⭐⭐
- First healthcare receptionist assistant with clinical intelligence
- Combines Elastic OpenSearch + AWS Bedrock in unique way
- Innovative patient matching algorithm with confidence scoring
- Purpose-based access control (beyond traditional RBAC)

### **Technical Excellence**
- Showcases Elastic's strengths: k-NN search, anomaly detection, aggregations, security
- Demonstrates AWS Bedrock Agents with real-world orchestration
- Production-ready architecture (scalable, secure, compliant)

### **Real-World Impact**
- Solves actual problem faced by Singapore hospitals daily
- Quantifiable improvements (70% faster, 100% accuracy)
- Scalable to entire healthcare system
- Clear path to production deployment

---

## 🚀 **Next Steps Post-Hackathon**

### **Phase 1: Pilot (Month 1-3)**
- Deploy to 1 hospital outpatient clinic
- Gather receptionist feedback
- Measure KPIs (lookup time, accuracy, satisfaction)

### **Phase 2: Integration (Month 4-6)**
- Connect to real NEHR API (coordinate with Synapxe)
- Integrate with hospital EMR systems
- Add voice interface for elderly patients

### **Phase 3: Scale (Month 7-12)**
- Roll out to all SingHealth hospitals
- Expand to other healthcare clusters (NUHS, NHG)
- Add advanced features (predictive analytics, preventive care recommendations)

---

## 📞 **Contact & Team**

**Team Name**: [Your Team Name]
**Team Members**: [Your Names]
**Primary Contact**: [Your Email]
**GitHub**: [Repository Link]

---

## 🔗 **References**

1. National Electronic Health Record (NEHR) - https://www.nehr.sg
2. AWS Bedrock Agents - https://aws.amazon.com/bedrock/agents/
3. Amazon OpenSearch k-NN - https://opensearch.org/docs/latest/search-plugins/knn/
4. Singapore PDPA Compliance - https://www.pdpc.gov.sg
5. Healthcare AI Safety Guidelines - WHO Digital Health Standards

---

## 💡 **Tagline**

**"MediGuard AI: Where Patient Safety Meets Intelligent Automation"**

*Transforming hospital reception from data entry to intelligent care coordination - one conversation at a time.*

---

**Prepared for**: Elastic + AWS Hackathon 2026
**Date**: February 16, 2026
**Duration**: 6-hour sprint
**Theme**: Healthcare Innovation with AI + Search
