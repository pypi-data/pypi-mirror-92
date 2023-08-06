from collections import defaultdict
import pandas as pd


def get_net_migration_from_od_matrix(od_matrix_file_path, origin_col_name, dest_col_name, count_col_name, adm_name):
    df = pd.read_csv(od_matrix_file_path)

    outflow = defaultdict(int, dict(df.groupby(origin_col_name)[count_col_name].sum()))
    inflow = defaultdict(int, dict(df.groupby(dest_col_name)[count_col_name].sum()))

    admins = set(outflow.keys()).union(set(inflow.keys()))

    net_mvmt = {}

    for admin in admins:
        net_mvmt[admin] = inflow[admin] - outflow[admin]

    result = pd.DataFrame(net_mvmt.items(), columns=[adm_name, 'net_mvmt'])
    result['total'] = result[adm_name].map(outflow)

    return result
