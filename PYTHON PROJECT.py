import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ------------------------------
# Person / Patient / Doctor Classes
# ------------------------------
class Person:
    def __init__(self, person_id, name, age):
        self.person_id = person_id
        self.name = name
        self.age = age

    def display_info(self):
        print(f"ID: {self.person_id}, Name: {self.name}, Age: {self.age}")


class Patient(Person):
    def __init__(self, patient_id, name, age, condition):
        super().__init__(patient_id, name, age)
        self.condition = condition

    def display_info(self):
        super().display_info()
        print(f"Condition: {self.condition}")


class Doctor(Person):
    def __init__(self, doctor_id, name, age, specialization):
        super().__init__(doctor_id, name, age)
        self.specialization = specialization

    def display_info(self):
        super().display_info()
        print(f"Specialization: {self.specialization}")


# ------------------------------
# Hospital System
# ------------------------------
class HospitalSystem:
    def __init__(self):
        # Appointments table: Patient, Doctor, Date, Time, Status
        self.appointments = pd.DataFrame(
            columns=["PatientID", "DoctorID", "Date", "Time", "Status"]
        )

    def add_appointment(self, patient_id, doctor_id, date, time, status="Scheduled"):
        new_app = pd.DataFrame({
            "PatientID": [patient_id],
            "DoctorID": [doctor_id],
            "Date": [date],
            "Time": [time],
            "Status": [status]
        })
        self.appointments = pd.concat(
            [self.appointments, new_app], ignore_index=True
        )

    def next_available_appointment(self):
        if self.appointments.empty:
            print("No appointments scheduled yet!")
            return None
        # Example: pick earliest by Date + Time
        df = self.appointments.copy()
        df["DateTime"] = pd.to_datetime(df["Date"] + " " + df["Time"])
        idx = np.argmin(df["DateTime"])
        best_app = df.iloc[idx]
        print("\nNext Appointment:")
        print(best_app[["PatientID", "DoctorID", "Date", "Time", "Status"]])
        return best_app

    def visualize_appointments_per_doctor(self):
        if self.appointments.empty:
            print("No data to visualize!")
            return
        counts = self.appointments["DoctorID"].value_counts()
        plt.figure(figsize=(8, 5))
        plt.bar(counts.index.astype(str), counts.values, color='lightgreen')
        plt.title("Number of Appointments per Doctor")
        plt.xlabel("Doctor ID")
        plt.ylabel("Appointments")
        plt.tight_layout()
        plt.show()


# ------------------------------
# Safe Input Functions
# ------------------------------
def safe_int_input(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a valid integer.")


def safe_str_input(prompt):
    while True:
        s = input(prompt).strip()
        if s:
            return s
        print("Input cannot be empty.")


# ------------------------------
# Main Program (User Input Mode)
# ------------------------------
def main():
    # --- Patients Input ---
    patients = []
    n_patients = safe_int_input("Enter number of patients: ")
    for i in range(n_patients):
        print(f"\nPatient {i+1}:")
        pid = safe_str_input("Enter Patient ID: ")
        name = safe_str_input("Enter Patient Name: ")
        age = safe_int_input("Enter Age: ")
        condition = safe_str_input("Enter Condition: ")
        p = Patient(pid, name, age, condition)
        patients.append(p)

    if patients:
        print("\nPatient Details:")
        for p in patients:
            p.display_info()

    # --- Doctors Input ---
    doctors = []
    n_doctors = safe_int_input("\nEnter number of doctors: ")
    for i in range(n_doctors):
        print(f"\nDoctor {i+1}:")
        did = safe_str_input("Enter Doctor ID: ")
        name = safe_str_input("Enter Doctor Name: ")
        age = safe_int_input("Enter Age: ")
        spec = safe_str_input("Enter Specialization: ")
        d = Doctor(did, name, age, spec)
        doctors.append(d)

    if doctors:
        print("\nDoctor Details:")
        for d in doctors:
            d.display_info()

    # --- Appointments Input ---
    system = HospitalSystem()
    n_apps = safe_int_input("\nEnter number of appointments: ")
    for i in range(n_apps):
        print(f"\nAppointment {i+1}:")
        patient_id = safe_str_input("Enter Patient ID: ")
        doctor_id = safe_str_input("Enter Doctor ID: ")
        date = safe_str_input("Enter Date (YYYY-MM-DD): ")
        time = safe_str_input("Enter Time (HH:MM): ")
        system.add_appointment(patient_id, doctor_id, date, time)

    # --- Operations ---
    system.next_available_appointment()
    system.visualize_appointments_per_doctor()


if __name__ == "__main__":
    main()