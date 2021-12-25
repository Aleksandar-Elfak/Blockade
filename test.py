matrix = 2


def getState():
    return {
        "m": matrix,
    }


def pr():
    print(matrix)


def c():

    getState()["m"] = 0


pr()
c()
pr()
