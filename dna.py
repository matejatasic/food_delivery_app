import csv
import sys


def main():
    if len(sys.argv) != 3:
        print("Usage: dna.py data.csv sequence.txt")
        sys.exit()

    database_file = open(sys.argv[1], "r")
    database_dict = csv.DictReader(database_file)
    database_headers = database_dict.fieldnames

    dna_file = open(sys.argv[2], "r")

    longest_match_dict = {}
    for row in dna_file:
        for header in database_headers:
                if header != "name":
                    longest_match_dict[header] = longest_match(row, header)
    # TODO: Check database for matching profiles

    for person in database_dict:
        matching_strs = 0

        for key in longest_match_dict.keys():
            if longest_match_dict[key] == int(person[key]):
                matching_strs += 1

            if matching_strs == len(longest_match_dict.keys()):
                print(person["name"])
                return

    print("No match")
    return


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()