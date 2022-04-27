import event
import math
import file

MODELTYPES = file.readJSONFile("assets/modelTypes.json")
G = 6.6743e-11  # N*m^2*kg^-2


def calcAccelerationOnObject(objectID, World):  # retourne l'acceleration dans un tableau
    # todo
    currentObject = {}
    for i in range(len(World)):
        if World[i]["id"] == objectID:
            currentObject["x"] = World[i]["x"]
            currentObject["y"] = World[i]["y"]
            currentObject["mass"] = MODELTYPES[World[i]["type"]]["mass"]
            currentObject["type"] = World[i]["type"]
            # if pour les non-spheriques ^ todo
    for i in range(len(World)):
        # NE PAS OUBLIER DE FAIRE X2 SI L'OBJET EST IMMOBILE => en fait non
        # math.sqrt((currentObject["x"] - [World[i]["x"]])**2+(currentObject["y"] - World[i]["y"])**2)
        # todo
        pass


def isColliding(World, x1, y1, r1):
    for i in range(len(World)):
        # todo : check collisions avec carré
        if World[i]["positionType"] == 0:
            x2, y2 = World[i]["x"], World[i]["y"]
            d = math.sqrt((x2 - x1) ** 2 + ((y2 - y1) ** 2))
            r2 = MODELTYPES[World[i]["type"]]["r"]
            if d < r2 + r1:
                return [x2, y2, r2]
    return []  # pas de collision


def calcCollision(x1, y1, r1, vx, vy, x2, y2, r2, fric, ms):  # fric = friction
    collisionT = calcCollisionMoment(x1, y1, r1, vx, vy, x2, y2, r2)  # return time of collision (in ms)
    if collisionT > ms:
        # si la collision est pas dans le scope (ne doit pas arriver mais en pratique BON...)
        return [x1 + vx * ms / 1000, y1 + vy * ms / 1000, vx, vy]  # on touche a rien
    xc, yc = x1 + vx * collisionT / 1000, y1 + vy * collisionT / 1000
    # ^ x and y for ball1 when collision occur
    alpha = (mesureAngle(x2, y2, xc, yc) + 0.5 * math.pi) % (2*math.pi)  # angle of normal vector
    # ox, oy = xc + ((x2 - xc) * (r1 / (r1 + r2))), yc + ((y2 - yc) * (r1 / (r1 + r2)))
    # ^ coords of the point where colision occur => useless
    remainingTravelTime = ms - collisionT
    # vecteur normal
    nx, ny = math.sin(alpha), -math.cos(alpha)
    dotProduct = (vx * nx) + (vy * ny)
    newVX, newVY = ((-2 * nx * dotProduct)+vx)*fric, ((-2 * ny * dotProduct)+vy)*fric
    newX, newY = xc + newVX * (remainingTravelTime / 1000), yc + newVY * (remainingTravelTime / 1000)
    return [newX, newY, newVX, newVY]


def calcCollisionMoment(xi, yi, r1, vx, vy, x2, y2, r2):
    vx, vy = vx / 1000, vy / 1000  # on remet en ms => ou pas
    # On resout le polynome de deg2 franchement horrible.
    a = vx ** 2 + vy ** 2
    b = 2 * vx * (xi - x2) + 2 * vy * (yi - y2)
    c = xi * (xi - 2 * x2) + yi * (yi - 2 * y2) + x2 ** 2 + y2 ** 2 - (r1 + r2) ** 2
    delta = b ** 2 - 4 * a * c
    if delta > 0:
        t1, t2 = (-b + math.sqrt(delta)) / (2 * a), (-b - math.sqrt(delta)) / (2 * a)
        if isinstance(t1, type(None)) or isinstance(t2, type(None)):
            return 0
        if 0 < t1 and (t1 < t2 or t2 < 0):
            return t1
        elif 0 < t2 and (t2 < t1 or t1 < 0):
            return t2
    else:
        event.error(f"No rac found for polynome. DEBUG infos : {xi, yi, r1, vx, vy, x2, y2, r2}")
        return 0


def mesureAngle(originX, originY, pointToMesureX, pointToMesureY):
    pointToMesureX -= originX
    pointToMesureY -= originY
    angle = 0
    # cas de l'égalité à 0
    if pointToMesureY == 0 or pointToMesureX == 0:  # opti
        if pointToMesureY == 0 and pointToMesureX == 0:
            event.error("mesureAngle got same coordinates for origin and pointToMesure")
        elif pointToMesureX == 0:
            angle = math.pi / 2 if pointToMesureY < 0 else math.pi * 3 / 2
        else:
            angle = 0 if pointToMesureX > 0 else math.pi
    elif pointToMesureX > 0 and pointToMesureY < 0:
        angle = math.atan(pointToMesureY / pointToMesureX)
    elif pointToMesureX < 0 and pointToMesureY < 0:
        angle = math.pi - math.atan(pointToMesureY / abs(pointToMesureX))
    elif pointToMesureX < 0 and pointToMesureY > 0:
        angle = math.pi + math.atan(pointToMesureY / pointToMesureX)
    elif pointToMesureX > 0 and pointToMesureY > 0:
        angle = math.atan(pointToMesureY / pointToMesureX)
    return angle


def radToDeg(rad):
    return 180 * rad / math.pi
