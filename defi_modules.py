from table2ascii import table2ascii as t2a, PresetStyle


def jewels_template(table_data):
    """
    Parameters
    table_data: 2D List

    Returns
    string
    """

    final = t2a(
        header=["Type", "Jewels", "USD"],
        body=table_data,
        first_col_heading=True
    )

    return final


# jewels_template([["Pending Unlocked Jewels", "something", "something"],
#                 ["something", "something", "something"]])
