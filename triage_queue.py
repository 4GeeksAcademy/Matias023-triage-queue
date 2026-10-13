#!/usr/bin/env python3

from dataclasses import dataclass, field
from datetime import datetime, timezone
import heapq
from itertools import count


@dataclass
class Patient:
    name: str
    triage_level: int
    arrived_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    def __post_init__(self):
        if not self.name.strip():
            raise ValueError("Patient name cannot be empty.")
        if self.triage_level not in (1, 2, 3):
            raise ValueError("Triage level must be 1, 2, or 3.")


class TriageQueue:
    def __init__(self):
        self._queue = []
        self._sequence = count()

    def enqueue(self, patient: Patient) -> None:
        if not isinstance(patient, Patient):
            raise TypeError("enqueue expects a Patient instance.")

        heapq.heappush(
            self._queue,
            (patient.triage_level, next(self._sequence), patient),
        )

    def dequeue(self) -> Patient:
        if not self._queue:
            raise IndexError("Triage queue is empty.")

        return heapq.heappop(self._queue)[2]

    def peek(self) -> Patient:
        if not self._queue:
            raise IndexError("Triage queue is empty.")

        return self._queue[0][2]

    def list_queue(self) -> list[Patient]:
        return [item[2] for item in sorted(self._queue)]

    def stats(self) -> dict[int, int]:
        result = {1: 0, 2: 0, 3: 0}

        for _, _, patient in self._queue:
            result[patient.triage_level] += 1

        return result


def print_patient(patient: Patient) -> None:
    print(
        f"{patient.name} | "
        f"triage={patient.triage_level} | "
        f"arrived_at={patient.arrived_at.isoformat()}"
    )


def run_cli() -> None:
    queue = TriageQueue()

    while True:
        print(
            "\n=== TRIAGE QUEUE ===\n"
            "1. Add patient\n"
            "2. Call next patient\n"
            "3. Peek next patient\n"
            "4. List queue\n"
            "5. Show statistics\n"
            "6. Exit"
        )

        option = input("Choose an option: ").strip()

        if option == "1":
            name = input("Patient name: ").strip()

            try:
                level = int(input("Triage level (1=critical, 2=urgent, 3=standard): "))
                patient = Patient(name=name, triage_level=level)
                queue.enqueue(patient)
                print("Patient added successfully.")
            except (ValueError, TypeError) as error:
                print(f"Error: {error}")

        elif option == "2":
            try:
                patient = queue.dequeue()
                print("Next patient:")
                print_patient(patient)
            except IndexError as error:
                print(f"Error: {error}")

        elif option == "3":
            try:
                print("Next patient:")
                print_patient(queue.peek())
            except IndexError as error:
                print(f"Error: {error}")

        elif option == "4":
            patients = queue.list_queue()

            if not patients:
                print("The queue is empty.")
                continue

            print("\nWaiting patients:")
            for position, patient in enumerate(patients, start=1):
                print(f"{position}. ", end="")
                print_patient(patient)

        elif option == "5":
            statistics = queue.stats()
            print(
                "\nPatients waiting:\n"
                f"Critical (1): {statistics[1]}\n"
                f"Urgent (2): {statistics[2]}\n"
                f"Standard (3): {statistics[3]}"
            )

        elif option == "6":
            print("Goodbye.")
            break

        else:
            print("Invalid option. Choose a number from 1 to 6.")


if __name__ == "__main__":
    run_cli()
