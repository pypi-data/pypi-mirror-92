from scipy.spatial import cKDTree


def create_kd_tree(df):
    kd_tree = cKDTree([(point.x, point.y) for point in
                       df['geometry']])
    return kd_tree


def calc_pd(voter_row, districts, pd_type='error'):
    '''
    knn_partisanship = knn_partisanship() -
    district_partisanship =
    '''
    geoid = voter_row['GEOID']
    district_ds = districts.query(f"GEOID == '{geoid}'").iloc[0]['dems']
    district_rs = districts.query(f"GEOID == '{geoid}'").iloc[0]['reps']
    if pd_type == 'naive':
        knn_ds = voter_row['knn_dems']
        knn_rs = voter_row['knn_reps']
    elif pd_type == 'adjusted':
        knn_ds = voter_row['dd_dems']
        knn_rs = voter_row['dd_reps']
    else:
        raise ValueError("pd_type should either be naive or adjusted")

    district_percentage = district_ds / (district_rs + district_ds)
    knn_percentage = knn_ds / (knn_ds + knn_rs)

    # Define PD as the gap in Democrats percentage between actual and expected
    pd = district_percentage - knn_percentage

    return pd


def get_knn_partisanship(voter, voter_type, kd_tree, k, voters):
    # is a tuple of ([Float], [Int])
    neighbours = kd_tree.query(voter['geometry'], k)
    # neighbours[1] gives the indices of all neighbouring points
    knn_type_voters = voters.iloc[list(neighbours[1])].query(
        f"party == '{voter_type}'").shape[0]
    # print(f"KNN voters of type {voter_type}: {knn_type_voters}")
    return knn_type_voters


def get_knn_dd_partisanship(voter, voter_type, k, voters, dds):
    # get the index of the voter
    # print(voter.name)
    durations = dds[voter.name]
    durations_and_indices = []
    for idx, duration in enumerate(durations):
        durations_and_indices.append((idx, duration))
    # Zip them up and sort by driving durations
    durations_and_indices.sort(key=lambda voter: voter[1])
    # Get the kNN durations and indices and get their partisanship
    knn_indices = [x[0] for x in durations_and_indices[:k]]
    # TODO: might get performance boost if I sort the knn_indices
    knn_type_voters = voters.iloc[knn_indices].query(
        f"party == '{voter_type}'").shape[0]
    # print(f"KNN voters of type {voter_type}: {knn_type_voters}")
    return knn_type_voters


def get_district_democrats(district_row, voters):
    '''district_partisanship(voter: Row) : (Int, Int)'''
    '''Returns number of Democrats and Republicans in the voter's district'''
    geoid = district_row['GEOID']
    district_D_voters = voters.query(
        f"GEOID == '{geoid}' and party == 'D'").shape[0]
    return district_D_voters


def get_district_republicans(district_row, voters):
    '''district_partisanship(voter: Row) : (Int, Int)'''
    '''Returns number of Democrats and Republicans in the voter's district'''
    geoid = district_row['GEOID']
    district_R_voters = voters.query(
        f"GEOID == '{geoid}' and party == 'R'").shape[0]
    return district_R_voters
