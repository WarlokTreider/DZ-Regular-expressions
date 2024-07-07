import re
import csv
from pprint import pprint

with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)
    # pprint(contacts_list)


def process_contact(contact):
    fullname = " ".join(contact[:3]).split()
    lastname = fullname[0]
    firstname = fullname[1] if len(fullname) > 1 else ""
    surname = fullname[2] if len(fullname) > 2 else ""
    organization = contact[3]
    position = contact[4]
    phone = normalize_phone(contact[5])
    email = contact[6]
    processed_contact = [lastname, firstname, surname, organization, position, phone, email]
    return processed_contact


def normalize_phone(phone):
    phone_pattern = re.compile(
        r'(\+7|8)?\s*\(?(\d{3})\)?[\s\-]?(\d{3})[\s\-]?(\d{2})[\s\-]?(\d{2})(\s*доб\.\s*(\d+))?'
    )
    match = phone_pattern.search(phone)
    if match:
        formatted_phone = f"+7({match.group(2)}){match.group(3)}-{match.group(4)}-{match.group(5)}"
        if match.group(6):
            formatted_phone += f" доб.{match.group(7)}"
        return formatted_phone
    return phone


processed_contacts = []
for contact in contacts_list:
    processed_contacts.append(process_contact(contact))

unique_contacts = []
seen = {}
for contact in processed_contacts:
    key = (contact[0], contact[1])
    if key not in seen:
        seen[key] = contact
    else:
        existing_contact = seen[key]
        for i in range(2, 7):
            if not existing_contact[i]:
                existing_contact[i] = contact[i]
unique_contacts = list(seen.values())


with open("processed_contacts.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerows(unique_contacts)

# pprint(unique_contacts)