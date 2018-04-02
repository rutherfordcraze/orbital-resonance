# Kepler Spirograph

background = 0.9
w = 800
h = 600

resolution = 144
cycles = 1000

object1 = { # Mercury
    "apoapsis":69.816,
    "periapsis":46.001,
    "GM":2203
}
    
object2 = { # Venus
    "apoapsis":108.939,
    "periapsis":107.477,
    "GM":32486
}


# PRESETS

Mercury = { # Mercury
    "apoapsis":69.816,
    "periapsis":46.001,
    "GM":2203
}

Venus = { # Venus
    "apoapsis":108.939,
    "periapsis":107.477,
    "GM":32486
}

Earth = { # Earth
    "apoapsis":152.100,
    "periapsis":147.095,
    "GM":39860
}

Mars = { # Mars
    "apoapsis":249.200,
    "periapsis":206.700,
    "GM":42828
}

Jupiter = { # Jupiter
    "apoapsis":816.620,
    "periapsis":740.520,
    "GM":12668653
}


# ——————————————————————————————————————————————————————————————————————

    
def Setup(body):
    body["semimajorAxis"] = (body.get("apoapsis") + body.get("periapsis")) / 2
    body["eccentricity"] = (body.get("apoapsis") - body.get("periapsis")) / (body.get("apoapsis") + body.get("periapsis"))
    body["semiminorAxis"] = sqrt(pow(body.get("semimajorAxis"), 2) * (1 - pow(body.get("eccentricity"), 2)))
    body["mm"] = sqrt(body.get("GM") / pow(body.get("semimajorAxis"), 3))
    body["period"] = 2 * pi * sqrt(pow(body.get("semimajorAxis"), 3) / body.get("GM"))
    
Setup(object1)
Setup(object2)

# Set up canvas
newPage(w, h)
fill(background, background, background, 1)
rect(0, 0, w, h)

def Evaluate (phase, body):
    angle = radians(phase) * 360
    x = sin(angle) * body.get("semimajorAxis")
    y = cos(angle) * body.get("semiminorAxis")
    return (x + w / 2, y + h / 2)

def DrawOrbit (body):
    fill(0, 0, 0, 0)
    if(body == object1): stroke(1, 1, 1, 1)
    if(body == object2): stroke(1, 1, 1, 1)
    strokeWidth(0.5)
    newPath()
    moveTo(Evaluate(0, body))
    
    for i in range(resolution + 1):
        lineTo(Evaluate(i / resolution, body))

    closePath()
    drawPath()
    
for i in range(cycles):
    
    evald1 = Evaluate(i / object1.get("period") / 2, object1)
    evald2 = Evaluate(i / object2.get("period") / 2, object2)
    
    strokeWidth(0.5)
    stroke(0, 0, 0, .2)
    line((evald1[0], evald1[1]), (evald2[0], evald2[1]))
    
DrawOrbit(object1)
DrawOrbit(object2)

#saveImage("output.png", imageResolution=150)
