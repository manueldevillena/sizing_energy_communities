import pandas as pd

if __name__ == "__main__":

    paths = ['hauts_sarts/datfiles/datscenario{}.dat'.format(i) for i in range(25)]
    production_profiles = pd.DataFrame()
    for file in paths:
        p_profile = pd.read_csv(file, header=None, sep=' ', squeeze=True)[2]
