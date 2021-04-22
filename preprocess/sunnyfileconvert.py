from utils import *
import csv  # https://realpython.com/python-csv/

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
          'georgia', 'hawaii', 'idaho',
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
    'georgia': 9, 'hawaii': 10, 'idaho': 11,
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
    'california',
    'alabama', 'alaska', 'arizona',
    'arkansas',  'colorado',
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


# east = 0 | west = 1
stateToNumberEW = {
    'alabama': 0, 'alaska': 1, 'arizona': 1,
    'arkansas': 0, 'california': 1, 'colorado': 1,
    'conneticut': 0, 'delaware': 0, 'florida': 0,
    'georgia': 0, 'hawaii': 1, 'idaho': 1,
    'illinois': 0, 'indiana': 0, 'iowa': 0,
    'kansas': 1, 'kentucky': 0, 'louisiana': 0,
    'maine': 0, 'maryland': 0, 'massachusets': 0,
    'michigan': 0, 'minnesota': 0, 'mississippi': 0,
    'missouri': 0, 'montana': 1, 'nebraska': 1,
    'nevada': 1, 'new hampshire': 0, 'new jersey': 0,
    'new mexico': 1, 'new york': 0, 'north carolina': 0,
    'north dakota': 1, 'ohio': 0, 'oklahoma': 1,
    'oregon': 1, 'pennsylvania': 0, 'rhode island': 0,
    'south carolina': 0, 'south dakota': 1, 'tennesse': 0,
    'texas': 1, 'utah': 1, 'vermont': 0,
    'virginia': 0, 'washington': 1, 'west virginia': 0,
    'wisconsin': 0, 'wyoming': 1
}
# List
numberToStateEW = [
    'east', 'west'
]

# north = 0 | south = 1
stateToNumberNS = {
    'alabama': 1, 'alaska': 0, 'arizona': 1,
    'arkansas': 1, 'california': 1, 'colorado': 1,
    'conneticut': 0, 'delaware': 1, 'florida': 1,
    'georgia': 1, 'hawaii': 1, 'idaho': 0,
    'illinois': 0, 'indiana': 0, 'iowa': 0,
    'kansas': 1, 'kentucky': 1, 'louisiana': 1,
    'maine': 0, 'maryland': 0, 'massachusets': 0,
    'michigan': 0, 'minnesota': 0, 'mississippi': 1,
    'missouri': 1, 'montana': 0, 'nebraska': 0,
    'nevada': 1, 'new hampshire': 0, 'new jersey': 0,
    'new mexico': 1, 'new york': 0, 'north carolina': 1,
    'north dakota': 0, 'ohio': 0, 'oklahoma': 1,
    'oregon': 0, 'pennsylvania': 0, 'rhode island': 0,
    'south carolina': 1, 'south dakota': 1, 'tennesse': 1,
    'texas': 1, 'utah': 1, 'vermont': 0,
    'virginia': 1, 'washington': 0, 'west virginia': 1,
    'wisconsin': 0, 'wyoming': 0
}
# List
numberToStateNS = [
    'north', 'south'
]
# west = 0 | midwest = 1 | south = 2 | northeast = 3
stateToNumberRegion = {
    'alabama': 2, 'alaska': 0, 'arizona': 0,
    'arkansas': 2, 'california': 0, 'colorado': 0,
    'conneticut': 3, 'delaware': 2, 'florida': 2,
    'georgia': 2, 'hawaii': 0, 'idaho': 0,
    'illinois': 1, 'indiana': 1, 'iowa': 1,
    'kansas': 1, 'kentucky': 2, 'louisiana': 2,
    'maine': 3, 'maryland': 2, 'massachusets': 3,
    'michigan': 1, 'minnesota': 1, 'mississippi': 2,
    'missouri': 1, 'montana': 0, 'nebraska': 1,
    'nevada': 0, 'new hampshire': 3, 'new jersey': 3,
    'new mexico': 0, 'new york': 3, 'north carolina': 2,
    'north dakota': 1, 'ohio': 1, 'oklahoma': 2,
    'oregon': 0, 'pennsylvania': 3, 'rhode island': 3,
    'south carolina': 2, 'south dakota': 1, 'tennesse': 2,
    'texas': 2, 'utah': 0, 'vermont': 3,
    'virginia': 2, 'washington': 0, 'west virginia': 2,
    'wisconsin': 1, 'wyoming': 0
}
# List
numberToStateRegion = [
    'west', 'midwest', 'south', 'northeast'
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
            return stateInitials[token]
        elif token in states:
            # print("--found valid: ", token)
            return token
    return validLocation

def regen():
    """MAIN"""
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
    with open ("raw_data/twitter-data.csv", encoding='utf-8', errors='ignore') as csv_file, open(config(''),mode='w') as outputFile:
        csv_data = csv.reader(csv_file, delimiter=",")
        outWrite = csv.writer(outputFile,delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        outWrite.writerow(['text','location'])
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
                    outWrite.writerow([text,stateToNumber[refinedLocation] ] )

            lineCount += 1
            
if __name__ == "__main__":
    regen()