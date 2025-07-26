# ACLIS - Advanced Synthetic EHR Data Generator
# This script produces highly detailed, clinically coherent, and multi-modal synthetic patient records.
# It is designed to generate data for the ACLIS investor and partner demo, showcasing integration
# with AI tools, genomic labs, and medical devices.

import json
import random
import uuid
from datetime import datetime, timedelta

# --- Configuration & Realistic Data Pools ---
# Based on deep research into EHR data structures and clinical realities.

FIRST_NAMES = ["John", "Jane", "Robert", "Emily", "Michael", "Sarah", "William", "Jessica", "David", "Linda"]
LAST_NAMES = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"]

BLOOD_TYPES = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]

# ICD-10 Codes for Realism
DIAGNOSES = {
    "NSCLC": {"code": "C34.11", "description": "Malignant neoplasm of right upper lobe, bronchus or lung"},
    "Hypertension": {"code": "I10", "description": "Essential (primary) hypertension"},
    "Hyperlipidemia": {"code": "E78.5", "description": "Hyperlipidemia, unspecified"},
    "Type 2 Diabetes": {"code": "E11.9", "description": "Type 2 diabetes mellitus without complications"},
    "CAD": {"code": "I25.10", "description": "Atherosclerotic heart disease of native coronary artery without angina pectoris"},
    "Pneumonia": {"code": "J18.9", "description": "Pneumonia, unspecified organism"}
}

# CPT Codes for Procedures
PROCEDURES = {
    "Office Visit": {"code": "99214", "description": "Office or other outpatient visit, established patient, 30-39 minutes"},
    "Chest X-ray": {"code": "71046", "description": "Radiologic examination, chest; 2 views"},
    "Chest CT": {"code": "71260", "description": "Computed tomography, thorax; with contrast material(s)"},
    "Bronchoscopy": {"code": "31622", "description": "Bronchoscopy, rigid or flexible, with or without fluoroscopic guidance"},
    "Biopsy": {"code": "31625", "description": "Bronchoscopy with bronchial or endobronchial biopsy"}
}

# RxNorm Codes for Medications
MEDICATIONS = {
    "Lisinopril": {"rxcui": "203166", "name": "Lisinopril 10 MG Oral Tablet"},
    "Atorvastatin": {"rxcui": "200331", "name": "Atorvastatin 20 MG Oral Tablet"},
    "Osimertinib": {"rxcui": "1732461", "name": "Osimertinib 80 MG Oral Tablet"},
    "Metformin": {"rxcui": "860975", "name": "Metformin hydrochloride 500 MG Extended Release Oral Tablet"}
}

# LOINC Codes for Labs
LAB_TESTS = {
    "Potassium": {"loinc": "2823-3", "unit": "mEq/L", "range": [3.5, 5.2]},
    "HbA1c": {"loinc": "4548-4", "unit": "%", "range": [4.0, 5.6]},
    "Creatinine": {"loinc": "2160-0", "unit": "mg/dL", "range": [0.6, 1.3]},
    "WBC": {"loinc": "6690-2", "unit": "x10^3/uL", "range": [4.5, 11.0]},
    "Hgb": {"loinc": "718-7", "unit": "g/dL", "range": [13.5, 17.5]},
    "EGFR Mutation": {"loinc": "42800-2", "unit": None, "range": None}
}

# --- Object-Oriented Data Models ---

class Patient:
    """Represents a single patient with all their associated data."""
    def __init__(self, patient_id, name, dob, sex):
        self.patient_id = patient_id
        self.name = name
        self.dob = dob
        self.sex = sex
        self.age = (datetime.now().date() - dob).days // 365
        self.blood_type = random.choice(BLOOD_TYPES)
        self.encounters = []
        self.genomic_profile = None
        self.wearable_data = []

    def to_dict(self):
        return {
            "patient_id": self.patient_id,
            "name": self.name,
            "age": self.age,
            "sex": self.sex,
            "dob": self.dob.strftime("%Y-%m-%d"),
            "blood_type": self.blood_type,
            "encounters": [e.to_dict() for e in self.encounters],
            "genomic_profile": self.genomic_profile.to_dict() if self.genomic_profile else None,
            "wearable_data": self.wearable_data
        }

class Encounter:
    """Represents a single clinical encounter."""
    def __init__(self, encounter_id, patient_id, date, encounter_type, chief_complaint):
        self.encounter_id = encounter_id
        self.patient_id = patient_id
        self.date = date
        self.type = encounter_type
        self.chief_complaint = chief_complaint
        self.diagnoses = []
        self.procedures = []
        self.medications = []
        self.vitals = []
        self.labs = []
        self.imaging_studies = []
        self.pathology_reports = []

    def to_dict(self):
        return {
            "encounter_id": self.encounter_id,
            "date": self.date.strftime("%Y-%m-%d"),
            "type": self.type,
            "chief_complaint": self.chief_complaint,
            "diagnoses": self.diagnoses,
            "procedures": self.procedures,
            "medications": self.medications,
            "vitals": self.vitals,
            "labs": [l.to_dict() for l in self.labs],
            "imaging_studies": [i.to_dict() for i in self.imaging_studies],
            "pathology_reports": [p.to_dict() for p in self.pathology_reports]
        }

class LabResult:
    """Represents a single lab result."""
    def __init__(self, test_name, value, unit, ref_range, status):
        self.test_name = test_name
        self.value = value
        self.unit = unit
        self.ref_range = ref_range
        self.status = status  # 'Normal', 'Abnormal', 'Critical'

    def to_dict(self):
        return self.__dict__

class ImagingStudy:
    """Represents an imaging study with integrated AI analysis."""
    def __init__(self, study_id, study_type, date, report, image_url, ai_analysis):
        self.study_id = study_id
        self.type = study_type
        self.date = date
        self.report = report
        self.image_url = image_url
        self.ai_analysis = ai_analysis

    def to_dict(self):
        d = self.__dict__.copy()
        if isinstance(d.get("date"), datetime):
            d["date"] = d["date"].strftime("%Y-%m-%d")
        elif hasattr(d.get("date"), "strftime"):
            d["date"] = d["date"].strftime("%Y-%m-%d")
        return d

class PathologyReport:
    """Represents a pathology report."""
    def __init__(self, report_id, date, specimen, report, ai_analysis=None):
        self.report_id = report_id
        self.date = date
        self.specimen = specimen
        self.report = report
        self.ai_analysis = ai_analysis

    def to_dict(self):
        d = self.__dict__.copy()
        if isinstance(d.get("date"), datetime):
            d["date"] = d["date"].strftime("%Y-%m-%d")
        elif hasattr(d.get("date"), "strftime"):
            d["date"] = d["date"].strftime("%Y-%m-%d")
        return d

class GenomicProfile:
    """Represents a patient's comprehensive genomic profile."""
    def __init__(self, prognosis, mutations, suggested_tests):
        self.prognosis = prognosis
        self.mutations = mutations
        self.suggested_tests = suggested_tests

    def to_dict(self):
        return self.__dict__


# --- Clinical Scenario Generators ---

def create_nsclc_patient_journey():
    """Generates a complete, multi-encounter journey for a patient diagnosed with NSCLC."""
    patient = Patient(
        patient_id=f"ACLIS-{uuid.uuid4().hex[:8]}",
        name="John Doe",
        dob=datetime.now().date() - timedelta(days=45*365),
        sex="M"
    )

    # --- ENCOUNTER 1: Primary Care Visit ---
    enc1_date = datetime.now().date() - timedelta(days=30)
    enc1 = Encounter(
        encounter_id=f"E-{patient.patient_id[-4:]}-01",
        patient_id=patient.patient_id,
        date=enc1_date,
        encounter_type="Outpatient",
        chief_complaint="Persistent cough and shortness of breath for 3 weeks."
    )
    enc1.diagnoses.append(DIAGNOSES["Hypertension"])
    enc1.medications.append(MEDICATIONS["Lisinopril"])
    enc1.procedures.append(PROCEDURES["Office Visit"])
    enc1.vitals.append({"timestamp": (enc1_date - timedelta(hours=1)).isoformat(), "hr": 85, "bp": "138/88", "spo2": 97})
    # Order a chest X-ray
    enc1.imaging_studies.append(ImagingStudy(
        study_id=f"IMG-{uuid.uuid4().hex[:6]}",
        study_type="Chest X-ray",
        date=enc1_date,
        image_url="https://via.placeholder.com/400x300/111827/6B7280?text=Chest+X-ray",
        report="A 1.5 cm nodule is noted in the right upper lobe. Recommend follow-up with CT.",
        ai_analysis={
            "provider": "Qure.ai qXR",
            "logo": "https://via.placeholder.com/80x20/10B981/FFFFFF?text=Qure.ai",
            "findings": [{"finding": "Pulmonary Nodule (RUL)", "confidence": 87, "coordinates": [{'top': '40%', 'left': '60%'}]}],
            "contradiction_alert": None
        }
    ))
    patient.encounters.append(enc1)

    # --- ENCOUNTER 2: Pulmonology Consult & CT Scan ---
    enc2_date = datetime.now().date() - timedelta(days=15)
    enc2 = Encounter(
        encounter_id=f"E-{patient.patient_id[-4:]}-02",
        patient_id=patient.patient_id,
        date=enc2_date,
        encounter_type="Outpatient",
        chief_complaint="Follow-up on abnormal chest X-ray."
    )
    enc2.procedures.append(PROCEDURES["Chest CT"])
    enc2.imaging_studies.append(ImagingStudy(
        study_id=f"IMG-{uuid.uuid4().hex[:6]}",
        study_type="Chest CT",
        date=enc2_date,
        image_url="https://via.placeholder.com/400x300/111827/6B7280?text=Chest+CT",
        report="Confirms 1.5 cm spiculated nodule in the RUL, highly suspicious for malignancy. Recommend bronchoscopy with biopsy.",
        ai_analysis={
            "provider": "Aidoc Radiology",
            "logo": "https://via.placeholder.com/80x20/3B82F6/FFFFFF?text=Aidoc",
            "findings": [{"finding": "Spiculated Nodule (RUL)", "confidence": 94, "coordinates": [{'top': '35%', 'left': '55%'}]}],
            "contradiction_alert": "Global research agent notes a new study suggesting nodules with these characteristics have a 15% higher risk of metastasis than previously thought. [View Study]"
        }
    ))
    patient.encounters.append(enc2)

    # --- ENCOUNTER 3: Inpatient for Biopsy ---
    enc3_date = datetime.now().date() - timedelta(days=7)
    enc3 = Encounter(
        encounter_id=f"E-{patient.patient_id[-4:]}-03",
        patient_id=patient.patient_id,
        date=enc3_date,
        encounter_type="Inpatient",
        chief_complaint="Scheduled bronchoscopy and biopsy."
    )
    enc3.procedures.append(PROCEDURES["Bronchoscopy"])
    enc3.procedures.append(PROCEDURES["Biopsy"])
    enc3.diagnoses.append(DIAGNOSES["NSCLC"])
    enc3.pathology_reports.append(PathologyReport(
        report_id=f"PATH-{uuid.uuid4().hex[:6]}",
        date=enc3_date + timedelta(days=2),
        specimen="Right upper lobe bronchial biopsy",
        report="Findings consistent with non-small cell lung carcinoma, adenocarcinoma subtype.",
        ai_analysis={
            "provider": "Paige.AI",
            "logo": "https://via.placeholder.com/80x20/8B5CF6/FFFFFF?text=Paige",
            "findings": [{"finding": "Adenocarcinoma cells detected", "confidence": 99}],
            "prognostic_insight": "Morphology suggests high likelihood of EGFR mutation."
        }
    ))
    # Add some labs for this encounter
    enc3.labs.append(LabResult("Potassium", 4.1, "mEq/L", "3.5-5.2", "Normal"))
    enc3.labs.append(LabResult("HbA1c", 6.8, "%", "4.0-5.6", "Critical"))
    enc3.labs.append(LabResult("WBC", 9.5, "x10^3/uL", "4.5-11.0", "Normal"))
    patient.encounters.append(enc3)

    # --- Add Genomic Profile (Post-Biopsy) ---
    patient.genomic_profile = GenomicProfile(
        prognosis={
            "model": "TabPFN Prognostic Model",
            "risk_score": 34,
            "stage_prediction": "Stage IIIB",
            "confidence": 89,
            "key_factors": ["EGFR L858R Mutation", "Tumor Size > 1cm", "Age > 40"]
        },
        mutations=[
            {"gene": "EGFR", "variant": "L858R", "significance": "Pathogenic", "type": "Somatic"},
            {"gene": "TP53", "variant": "R273H", "significance": "Likely Pathogenic", "type": "Somatic"}
        ],
        suggested_tests=[
            {"name": "FoundationOne CDx", "provider": "Foundation Medicine", "logo": "https://via.placeholder.com/80x20/8B5CF6/FFFFFF?text=Foundation", "description": "324-gene panel for solid tumors, FDA-approved companion diagnostic."},
            {"name": "Guardant360 CDx", "provider": "Guardant Health", "logo": "https://via.placeholder.com/80x20/EF4444/FFFFFF?text=Guardant", "description": "Liquid biopsy for comprehensive genomic profiling of 74 genes."}
        ]
    )

    # --- Add Wearable Data ---
    for i in range(30):
        date = datetime.now().date() - timedelta(days=30-i)
        patient.wearable_data.append({
            "date": date.strftime("%Y-%m-%d"),
            "steps": random.randint(2000, 8000) - (i*50),  # Simulating declining activity
            "avg_hr": random.randint(70, 90),
            "sleep_hours": round(random.uniform(5.5, 7.5), 1)
        })

    return patient

def create_simple_patient(patient_id, name, diagnosis_key, age):
    """Generates a simpler patient record for the list view."""
    patient = Patient(
        patient_id=f"ACLIS-{uuid.uuid4().hex[:8]}",
        name=name,
        dob=datetime.now().date() - timedelta(days=age*365),
        sex=random.choice(["M", "F"])
    )
    enc_date = datetime.now().date() - timedelta(days=random.randint(5, 50))
    encounter = Encounter(
        encounter_id=f"E-{patient.patient_id[-4:]}-01",
        patient_id=patient.patient_id,
        date=enc_date,
        encounter_type="Inpatient",
        chief_complaint=DIAGNOSES[diagnosis_key]['description']
    )
    encounter.diagnoses.append(DIAGNOSES[diagnosis_key])
    patient.encounters.append(encounter)
    return patient

# --- Main Generation Logic ---

def main():
    """Main function to generate and write records."""
    print("Generating advanced synthetic EHR data for ACLIS demo...")

    records = []

    # 1. Create the detailed showcase patient
    john_doe = create_nsclc_patient_journey()
    records.append(john_doe.to_dict())

    # 2. Create a few other simpler patients for the list view
    other_patients_data = [
        ("Jane Smith", "Type 2 Diabetes", 68),
        ("Robert Brown", "CAD", 72),
        ("Emily Jones", "Pneumonia", 55)
    ]
    for i, (name, diag_key, age) in enumerate(other_patients_data):
        p = create_simple_patient(i+2, name, diag_key, age)
        records.append(p.to_dict())

    # 3. Write to JSON file
    output_filename = "synthetic_aclis_records.json"
    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=4)

    print(f"Successfully generated {len(records)} synthetic patient records.")
    print(f"Detailed NSCLC journey created for '{records[0]['name']}'.")
    print(f"Output saved to '{output_filename}'.")

if __name__ == "__main__":
    main()
