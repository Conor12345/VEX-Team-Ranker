import re

def text(size=20):
    return ("Verdana", size)

def seasons():
    return reversed(["Skyrise", "Toss Up", "Sack Attack", "Gateway", "Round Up", "Clean Sweep",
            "Elevation", "Bridge Battle", "Nothing But Net", "Starstruck", "In The Zone", "Turning Point", "Tower Takeover"])

def countries():
    data = ["United States", "Australia", "Canada", "China", "Colombia", "Hong Kong", "Mexico", "New Zealand", "Singapore", "United Kingdom"]
    #for country in pycountry.countries:
    #    data.append(country.name)
    return tuple(data)

def longestStringInArray(array):
    longest = 0
    for item in array:
        if len(str(item)) > longest:
            longest = len(str(item))
    return longest

def isOnlySpaces(listIn):
    for item in listIn:
        if not bool(re.match("^ +$", item)):
            return False
    return True

def remap(x, in_min, in_max, out_min, out_max):
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min