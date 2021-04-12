import os
import sys

# USAGE: python3 ./csv-to-json.py <valid csv file>
# Tasks:
# 1. takes as input a .csv file and outputs a .json
#    valid csv file has the following columns: tweet number, description, text, location
#    there should be NO COMMAS in the input file, as this uses commas to seperate data into colums
#    
# 2. only keeps data with valid location identifiers
#       - methods used to validate location:
#           1. makes entire location string lower case
#           2. adds a space after any commas
#           3. will tokenize all location data
#           4. if either full state name OR suffix is provided, 
#              this will be accepted as a valid location. (US only)
#              EX: "mi" or "michigan" --> valid location
#                   "london" --> invalid
#                   "vmi" --> invalid
#                   "88.925" --> invalid

def main():
    """MAIN"""
    # check args
    if len(sys.argv) != 2:
        print("USAGE: python3 ./csv-to-json.py <valid csv file>\nExiting now")
        exit(1)

    if not os.path.exists(sys.argv[1]):
        print("Path: ", sys.argv[1], ", does not exist\nExiting now")
        exit(1)
    
    # file management
    curDir = os.getcwd()
    outputFile = os.path.join(curDir, "data.json")  # needs to open still
    inputFile = os.open(sys.argv[1])


if __name__ == "__main__":
    main()