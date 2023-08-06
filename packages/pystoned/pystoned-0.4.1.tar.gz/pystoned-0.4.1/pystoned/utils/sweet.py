import numpy as np


def sweet(x):
    """Sweet spot approach, return active concavity constraint"""

    # transform data
    df = np.asmatrix(x)

    # calculate distance matrix
    distance = np.zeros((len(df), len(df)))
    for i in range(len(df)):
        for j in range(len(df)):
            if i != j:
                distance[i, j] = np.sqrt(
                    np.sum(np.square(df[i, :] - df[j, :])))

    # calculate distance cut
    distcut = np.asmatrix(np.percentile(distance, 3, axis=0))

    # find concavity constraint in sweet spot
    Cutactive = np.zeros((len(distance), len(distance)))
    for i in range(len(distance)):
        for j in range(len(distance)):
            if distance[i, j] <= distcut[:, i]:
                Cutactive[i, j] = 1

    return Cutactive