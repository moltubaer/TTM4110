# ----- Lab II ----- #
# ----- II.A.2 ----- #

def calculate_mos_score(bandwidth):
    thresholds = [0, 0.2, 0.5, 0.7, 1]
    mos_values = [1, 2, 3, 4, 5]

    mos_score = None
    for i in range(len(thresholds)):
        if bandwidth <= thresholds[i]:
            if i == 0:
                mos_score = mos_values[0]
            else:
                mos_score = mos_values[i-1]
            break

    return mos_score

bandwidth = 0.9
mos = calculate_mos_score(bandwidth)
print(f"MOS Score: {mos}")





