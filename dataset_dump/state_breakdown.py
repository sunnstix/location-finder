numberToState = [
    'alabama', 'alaska', 'arizona',
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
    'wisconsin', 'wyoming'
]
total = 0
counts = {}
fin = open("mydata.csv", "r")
for line in fin.readlines():
    try:
        parts = line.split(",")
        if len(parts) == 0:
            continue
        num = int(parts[-1].replace("\n", ""))
        if not numberToState[num] in counts:
            counts[numberToState[num]] = 1
        else:
            counts[numberToState[num]] += 1
        total += 1
    except:
        print(line)
print("Total number of Tweets: " + str(total))
for state in counts:
    print(state + ": " + str(float(counts[state] / total)) + " (" + str(counts[state]) + " / " + str(total) + ")")
fin.close()