#!/usr/bin/env -S uv run --script

import csv
import sys
from datetime import datetime

from icalendar import Calendar, Event


# Function to parse the CSV from stdin and extract relevant data
def parse_contacts_csv(input):
    contacts = []
    reader = csv.DictReader(input)
    for row in reader:
        # Extract first name, last name, and birthday
        first_name = row.get('First Name', '').strip()
        last_name = row.get('Last Name', '').strip()
        birthday = row.get('Birthday', '').strip()

        if birthday and (first_name or last_name):
            contacts.append(dict(
                first_name=first_name,
                last_name=last_name,
                birthday=birthday)
            )
    return contacts

# Function to create an iCal file and write it to stdout
def create_ical_file(contacts):
    cal = Calendar()

    for contact in contacts:
        if contact['birthday']:
            try:
                # Parse the birthday date (assuming format: YYYY-MM-DD or MM/DD/YYYY)
                birthday = contact['birthday']
                if birthday.startswith('--'):
                    birthday_str = f"2000-{birthday[2:]}"  # Add 2000 as the year
                    birthday_date = datetime.strptime(birthday_str, '%Y-%m-%d')
                elif '-' in birthday:
                    birthday_date = datetime.strptime(birthday, '%Y-%m-%d')
                else:
                    birthday_date = datetime.strptime(birthday, '%m/%d/%Y')

                # Create an event for the birthday
                event = Event()
                event.add('summary', f"{contact['first_name']} {contact['last_name']}'s Birthday")
                event.add('dtstart', birthday_date.date())
                event.add('rrule', {'freq': 'yearly'})
                event.add('transp', 'TRANSPARENT')  # Marks the event as free time

                cal.add_component(event)
            except ValueError:
                print(f"Skipping invalid birthday format for {contact['first_name']} {contact['last_name']}: {contact['birthday']}", file=sys.stderr)

    # Write the calendar to stdout
    sys.stdout.buffer.write(cal.to_ical())

# Main function
def main():
    stream = sys.stdin

    if len(sys.argv) > 1:
        stream = open(sys.argv[1], 'r')

    # Parse the CSV from stdin
    contacts = parse_contacts_csv(stream)

    # Create the iCal file and write it to stdout
    create_ical_file(contacts)

    if stream is not sys.stdin:
        stream.close()

if __name__ == '__main__':
    main()
