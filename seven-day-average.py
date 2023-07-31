import csv
import requests


def main():
    # Read NYTimes Covid Database
    download = requests.get(
        "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv"
    )
    decoded_content = download.content.decode("utf-8")
    file = decoded_content.splitlines()
    reader = csv.DictReader(file)

    # Construct 14 day lists of new cases for each states
    new_cases = calculate(reader)

    # Create a list to store selected states
    states = []
    print("Choose one or more states to view average COVID cases.")
    print("Press enter when done.\n")

    while True:
        state = input("State: ")
        if state in new_cases:
            states.append(state)
        if len(state) == 0:
            break

    print(f"\nSeven-Day Averages")

    # Print out 7-day averages for this week vs last week
    comparative_averages(new_cases, states)


# Create a dictionary to store 14 most recent days of new cases by state
def calculate(reader):
    # Dictionary to store new cases in last 14 days
    new_cases = {}
    # Dictionary to store total number of cases registered per state
    cases = {}

    for line in reader:
        state = line["state"]
        if state not in new_cases:
            # Create a list for each state to store new cases in last 14 days
            new_cases[state] = list()
            new_cases[state].append(int(line["cases"]))
        else:
            if len(new_cases[state]) == 14:
                new_cases[state].pop(0)
            # new cases = total number of cases now - total number of previously known cases
            new_cases[state].append(int(line["cases"]) - cases[state])
        cases[state] = int(line["cases"])

    return new_cases


# Calculate and print out seven day average for given state
def comparative_averages(new_cases, states):
    # this_week = last_week = 0
    for state in states:
        last_week = sum(new_cases[state][:7]) / 7
        this_week = sum(new_cases[state][7:]) / 7

        try:
            percent = abs(last_week - this_week) / last_week * 100
            if last_week < this_week:
                msg = f"and an increase of {percent:.2f}%."
            else:
                msg = f"and a decrease of {percent:.2f}%."
        except ZeroDivisionError:
            msg = "while it had no cases in the previous week."
        print(f"{state} had a 7-day average of {int(this_week)}", msg)


if __name__ == "__main__":
    main()
