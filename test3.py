
deg = 22

for m in range(60 * 24):
    loc_h = m * 0.5
    loc_m = m * 6

    if loc_h >= 360:
        loc_h %= 360
    if loc_m >= 360:
        loc_m %= 360

    degree1 = abs(loc_h - loc_m)
    degree2 = abs(360 - loc_h - loc_m)

    if degree1 == deg or degree2 == deg:
        print(m // 60, ":", m % 60)


