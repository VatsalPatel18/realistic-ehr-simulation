# Synthetic EHR data generator
# This script produces 10 synthetic patient EHR records with encounters,
# vitals, labs, and wearable summaries and writes them to synthetic_ehr_records.json.

import json
import random
from datetime import datetime, timedelta


def random_name():
    first_names = ["John","Jane","Alice","Bob","Carol","David","Eve","Frank","Grace","Henry","Isabel","Jack","Kara","Liam","Mia"]
    last_names = ["Smith","Johnson","Williams","Brown","Jones","Garcia","Miller","Davis","Rodriguez","Martinez","Hernandez","Lopez","Gonzalez","Wilson","Anderson"]
    return random.choice(first_names) + " " + random.choice(last_names)


def random_blood_type():
    return random.choice(["A+","A-","B+","B-","AB+","AB-","O+","O-"])


def generate_vitals(date, count=2):
    vitals=[]
    for _ in range(count):
        dt = datetime.combine(date, datetime.min.time()) + timedelta(hours=random.randint(0,23), minutes=random.randint(0,59))
        hr=random.randint(60,110)
        systolic=random.randint(90,140)
        diastolic=random.randint(60, min(90, systolic-10))
        temp=round(random.uniform(36.0,38.0),1)
        vitals.append({"Time": dt.strftime("%Y-%m-%dT%H:%M:%SZ"), "HeartRate": hr, "BloodPressure": f"{systolic}/{diastolic}", "Temperature": temp})
    return vitals


def generate_labs():
    return [
        {"Test":"Hemoglobin","Value": round(random.uniform(11,17),1),"Unit":"g/dL","ReferenceRange":"12.0–16.0"},
        {"Test":"White Blood Cell Count","Value": round(random.uniform(4,10),1),"Unit":"x10^9/L","ReferenceRange":"4.0–11.0"},
        {"Test":"Serum Creatinine","Value": round(random.uniform(0.6,1.3),2),"Unit":"mg/dL","ReferenceRange":"0.5–1.1"}
    ]


def generate_encounter(pid, idx):
    base_date=datetime.now()-timedelta(days=random.randint(0,365))
    encounter_date=base_date.date()
    date_str=encounter_date.strftime("%Y-%m-%d")
    types=["Emergency","Inpatient","Outpatient"]
    complaints=["Chest pain","Shortness of breath","Headache","Abdominal pain","Fever","Cough","Fatigue","Dizziness","Nausea","Back pain"]
    diagnoses=[{"Code":"I10","Description":"Essential hypertension"},{"Code":"E11.9","Description":"Type 2 diabetes mellitus"},{"Code":"J18.9","Description":"Pneumonia"},{"Code":"K21.9","Description":"Gastro-esophageal reflux disease"},{"Code":"N39.0","Description":"Urinary tract infection"}]
    procedures=[{"Code":"99123","Description":"Electrocardiogram"},{"Code":"99214","Description":"Office visit"},{"Code":"93010","Description":"Cardiac stress test"},{"Code":"71020","Description":"Chest radiograph"},{"Code":"36415","Description":"Venipuncture"}]
    medications=["Metformin 500 mg","Lisinopril 10 mg","Amoxicillin 500 mg","Aspirin 81 mg","Atorvastatin 20 mg","Acetaminophen 500 mg","Ibuprofen 400 mg","Furosemide 20 mg"]
    return {
        "EncounterID":f"E{pid:03d}{idx:02d}",
        "Date": date_str,
        "Type": random.choice(types),
        "ChiefComplaint": random.choice(complaints),
        "PrimaryDiagnosis": random.choice(diagnoses),
        "Procedures": random.sample(procedures,k=random.randint(0,2)),
        "Medications": random.sample(medications,k=random.randint(1,3)),
        "VitalSigns": generate_vitals(encounter_date,2),
        "LabResults": generate_labs(),
        "Outcome": random.choice(["Admitted to hospital","Discharged home","Transferred to rehab","Discharged with follow‑up appointment"])
    }


def generate_wearable(start_date, days=7):
    data=[]
    for i in range(days):
        d=start_date + timedelta(days=i+1)
        data.append({"Date": d.strftime("%Y-%m-%d"), "Steps": random.randint(3000,10000), "AvgHeartRate": random.randint(60,100), "SleepHours": round(random.uniform(5,8),1)})
    return data


def generate_patient(pid):
    n_enc=random.randint(1,3)
    encounters=[generate_encounter(pid,i) for i in range(n_enc)]
    last_date=max(datetime.strptime(e["Date"],"%Y-%m-%d") for e in encounters)
    return {
        "PatientID": f"P{pid:04d}",
        "Name": random_name(),
        "Age": random.randint(1,90),
        "Sex": random.choice(["M","F"]),
        "Weight": round(random.uniform(40,100),1),
        "BloodType": random_blood_type(),
        "Encounters": encounters,
        "WearableData": generate_wearable(last_date,7)
    }


def generate_records(n=10):
    return [generate_patient(i) for i in range(1,n+1)]


def main():
    records=generate_records(10)
    with open("synthetic_ehr_records.json","w",encoding="utf-8") as f:
        json.dump(records,f,indent=2)
    print(f"Generated {len(records)} synthetic EHR records.")


if __name__=="__main__":
    main()
