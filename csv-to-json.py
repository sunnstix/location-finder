import os
import sys
import csv  # https://realpython.com/python-csv/
import json # https://stackabuse.com/reading-and-writing-json-to-a-file-in-python/
import re # to remove non-alphanumerics from strings
# USAGE: python3 ./csv-to-json.py <valid csv file>
# for us: python3 ./csv-to-json.py twitter-data.csv

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

# TIPs: 
#  1. you may need to format your JSON file after running for clarity.
#       ON VSCode for Mac: CMD + SHIFT + P, then type "Format Document", then enter
#  2. I also had to allow my JSON file to be longer than 5000 lines. I set mine to 30,000



# Result:
#   There are 25,000 lines in the csv file. By running this, I was able to
#   identify 20,000 lines by location.  These are more than enough to train
#   and test our program.

# globals
states = ['alabama', 'alaska', 'arizona',
          'arkansas', 'california', 'colorado',
          'conneticut', 'delaware', 'florida',
          'georgia', 'hiwaii', 'idaho',
          'illinois', 'indiana', 'iowa',
          'kansas', 'kentucky', 'louisiana',
          'maine', 'maryland', 'massachusets',
          'michigan', 'minnesota', 'mississippi',
          'missouri', 'montana', 'nebraska',
          'nevada', 'new hampshire', 'new jersey',
          'new mexico', 'new york', 'north carolina',
          'north dakota', 'ohio', 'oklahoma',
          'oregon', 'pennsylvania', 'rhode island',
          'south carolina', 'south dakota', 'tennesse',
          'texas', 'utah', 'vermont',
          'virginia', 'washington', 'west virginia',
          'wisconsin', 'wyoming']
stateInitials = {
    'al': states[0], 'ak': states[1], 'az': states[2],
    'ar': states[3], 'ca': states[4], 'co': states[5],
    'ct': states[6], 'de': states[7], 'fl': states[8],
    'ga': states[9], 'hi': states[10], 'id': states[11],
    'il': states[12], 'in': states[13], 'ia': states[14],
    'ks': states[15], 'ky': states[16], 'la': states[17],
    'me': states[18], 'md': states[19], 'ma': states[20],
    'mi': states[21], 'mn': states[22], 'ms': states[23],
    'mo': states[24], 'mt': states[25], 'ne': states[26],
    'nv': states[27], 'nh': states[28], 'nj': states[29],
    'nm': states[30], 'ny': states[31], 'nc': states[32],
    'nd': states[33], 'oh': states[34], 'ok': states[35],
    'or': states[36], 'pa': states[37], 'ri': states[38],
    'sc': states[39], 'sd': states[40], 'tn': states[41],
    'tx': states[42], 'ut': states[43], 'vt': states[44],
    'va': states[45], 'wa': states[46], 'wv': states[47],
    'wi': states[48], 'wy': states[49]
}
# dictionary mimicing 0 indexed list below
stateToNumber = {
    'alabama': 0, 'alaska': 1, 'arizona': 2,
    'arkansas': 3, 'california': 4, 'colorado': 5,
    'conneticut': 6, 'delaware': 7, 'florida': 8,
    'georgia': 9, 'hiwaii': 10, 'idaho': 11,
    'illinois': 12, 'indiana': 13, 'iowa': 14,
    'kansas': 15, 'kentucky': 16, 'louisiana': 17,
    'maine': 18, 'maryland': 19, 'massachusets': 20,
    'michigan': 21, 'minnesota': 22, 'mississippi': 23,
    'missouri': 24, 'montana': 25, 'nebraska': 26,
    'nevada': 27, 'new hampshire': 28, 'new jersey': 29,
    'new mexico': 30, 'new york': 31, 'north carolina': 32,
    'north dakota': 33, 'ohio': 34, 'oklahoma': 35,
    'oregon': 36, 'pennsylvania': 37, 'rhode island': 38,
    'south carolina': 39, 'south dakota': 40, 'tennesse': 41,
    'texas': 42, 'utah': 43, 'vermont': 44,
    'virginia': 45, 'washington': 46, 'west virginia': 47,
    'wisconsin': 48, 'wyoming': 49
}
# List
numberToState = [
    'alabama', 'alaska', 'arizona',
    'arkansas', 'california', 'colorado',
    'conneticut', 'delaware', 'florida',
    'georgia', 'hiwaii', 'idaho',
    'illinois', 'indiana', 'iowa',
    'kansas', 'kentucky', 'louisiana',
    'maine', 'maryland', 'massachusets',
    'michigan', 'minnesota', 'mississippi',
    'missouri', 'montana', 'nebraska',
    'nevada', 'new hampshire', 'new jersey',
    'new mexico', 'new york', 'north carolina',
    'north dakota', 'ohio', 'oklahoma',
    'oregon', 'pennsylvania', 'rhode island',
    'south carolina', 'south dakota', 'tennesse',
    'texas', 'utah', 'vermont',
    'virginia', 'washington', 'west virginia',
    'wisconsin', 'wyoming'
]

def validateLocation(location: str) -> str:
    """ensures tweet has valid location. 
    if true, return long form of state name
    if not, return string "NULL" """
    # check location
    validLocation = "NULL"  # init to "NULL" incase no valid location is found
    locationTokens = location.split()
    for token in locationTokens:
        # token = re.compile("[^a-zA-Z]") # removes all non-alpha chars
        token = str(token)
        # print("token = ", token)
        if token in stateInitials:
            # print("--found valid: ", stateInitials[token])
            validLocation = stateInitials[token]
            break
        elif token in states:
            # print("--found valid: ", token)
            validLocation = token
            break
    return validLocation

def main():
    """MAIN"""
    # check args
    if len(sys.argv) != 2:
        print("USAGE: python3 ./csv-to-json.py <valid csv file>\nExiting now")
        exit(1)

    if not os.path.exists(sys.argv[1]):
        print("Path: ", sys.argv[1], ", does not exist\nExiting now")
        exit(1)
    
    # output file management
    outputFileLocation = "data.json"
    if os.path.exists(outputFileLocation):
        os.remove(outputFileLocation)
    outputFile = open(outputFileLocation, "x")
    
    # vars for csv
    number = -1
    desc = "empty"
    text = "empty"
    location = "empty"
    refinedLocation = "empty" 
    lineCount = 0

    # vars for output
    data = []
    # tempTweet = {"number": number, "description": desc, "text": text, "location": refinedLocation}

    # process csv
    with open ("twitter-data.csv", encoding='utf-8', errors='ignore') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=",")
        # -- number , description, text, location --
        for row in csv_data:
            # first line is headers and we should ignore this.
            if lineCount != 0:
                # print("line number: ", lineCount)
                number = int(row[0])
                desc = row[1].lower()
                text = row[2].lower()
                location = row[3].lower()

                refinedLocation = validateLocation(location)

                # we only want to keep VALID location tweets
                if refinedLocation != "NULL":
                    
                    # append the new tweet
                    data.append({"number": number, "description": desc, "text": text, "location": refinedLocation})

            lineCount += 1
            
    # write data to output file
    json.dump(data,outputFile)

    # close files
    csv_file.close()
    outputFile.close()

if __name__ == "__main__":
    main()