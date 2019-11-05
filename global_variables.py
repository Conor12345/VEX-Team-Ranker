import pycountry

def text(size=20):
    return ("Verdana", size)

def seasons():
    return reversed(["Skyrise", "Toss Up", "Sack Attack", "Gateway", "Round Up", "Clean Sweep",
            "Elevation", "Bridge Battle", "Nothing But Net", "Starstruck", "In The Zone", "Turning Point", "Tower Takeover"])

def countries():
    data = []
    for country in pycountry.countries:
        data.append(country.name)
    return tuple(data)