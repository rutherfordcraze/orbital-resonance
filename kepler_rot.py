# Kepler Spirograph (incl. eccentricity models, non-constant velocity)

background = .9
w = 600
h = 400

resolution = 144
cycles = 6000
clarity = 10

object1 = { # Venus
    "apoapsis":108.939,
    "periapsis":107.477,
    "GM":3248.6,
    "w":54.884
}
    
object2 = { # Earth
    "apoapsis":152.100,
    "periapsis":147.095,
    "GM":3986.0,
    "w":114.207
}


# ——————————————————————————————————————————————————————————————————————


# PRESETS

Mercury = { # Mercury
    "apoapsis":69.816,
    "periapsis":46.001,
    "GM":220.3,
    "w":29.124
}

Venus = { # Venus
    "apoapsis":108.939,
    "periapsis":107.477,
    "GM":3248.6,
    "w":54.884
}

Earth = { # Earth
    "apoapsis":152.100,
    "periapsis":147.095,
    "GM":3986.0,
    "w":114.207
}

Mars = { # Mars
    "apoapsis":249.200,
    "periapsis":206.700,
    "GM":4282.8,
    "w":286.502
}

Jupiter = { # Jupiter
    "apoapsis":816.620,
    "periapsis":740.520,
    "GM":1266865.3,
    "w":273.867
}


# ——————————————————————————————————————————————————————————————————————


def Setup(body):
    body["semimajorAxis"] = (body.get("apoapsis") + body.get("periapsis")) / 2
    body["eccentricity"] = (body.get("apoapsis") - body.get("periapsis")) / (body.get("apoapsis") + body.get("periapsis"))
    body["semiminorAxis"] = sqrt(pow(body.get("semimajorAxis"), 2) * (1 - pow(body.get("eccentricity"), 2)))
    body["mm"] = sqrt(body.get("GM") / pow(body.get("semimajorAxis"), 3))
    body["period"] = 2 * pi * sqrt(pow(body.get("semimajorAxis"), 3) / body.get("GM"))
    body["focalOffset"] = body.get("apoapsis") - body.get("periapsis")

Setup(object1)
Setup(object2)

# Set up canvas
newPage(w, h)
fill(background, background, background, 1)
rect(0, 0, w, h)


# ——————————————————————————————————————————————————————————————————————


def hypot(x, y):
    a = w / 2
    b = h / 2
    return sqrt((a - x)**2 + (b - y)**2)

def rotate(origin, point, angle):
    ox, oy = origin
    px, py = point

    qx = ox + cos(angle) * (px - ox) - sin(angle) * (py - oy)
    qy = oy + sin(angle) * (px - ox) + cos(angle) * (py - oy)
    return qx, qy

def Evaluate (phase, body):
    angle = radians(phase) * 360
    x = sin(angle) * body.get("semimajorAxis")
    y = cos(angle) * body.get("semiminorAxis")
    r = rotate((0, 0), (x + body.get("focalOffset") / 2, y), radians(body.get("w")))
    return (r[0] + w / 2, r[1] + h / 2)

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
    
    
# ——————————————————————————————————————————————————————————————————————


# Trace lines for actual orbital speeds (slower)
cursor1 = 0
cursor2 = 0

for i in range(cycles):

    evald1 = Evaluate(1 - cursor1 / clarity, object1)
    evald2 = Evaluate(1 - cursor2 / clarity, object2)

    body1speed = sqrt( object1.get("GM") * ((2 / hypot(evald1[0], evald1[1])) - (1 / object1.get("semimajorAxis"))))
    body2speed = sqrt( object2.get("GM") * ((2 / hypot(evald2[0], evald2[1])) - (1 / object2.get("semimajorAxis"))))
    cursor1 += .1 / body1speed
    cursor2 += .1 / body2speed

    strokeWidth(0.5)
    stroke(0, 0, 0, .05)
    line((evald1[0], evald1[1]), (evald2[0], evald2[1]))

DrawOrbit(object1)
DrawOrbit(object2)

#saveImage("rot_Venus-Earth.png", imageResolution=150)
#saveImage("Mars-Earth_Organic.gif")
