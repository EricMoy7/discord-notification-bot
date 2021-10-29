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


def pool_template(table_data):
    """
    Parameters
    table_data: 2D list

    Returns
    string ASCII
    """

    first_section = t2a(
        body=table_data[0:4],
        first_col_heading=True
    )

    second_section = t2a(
        header=[" ", "Day", "Week", "Year"],
        body=table_data[5:],
        first_col_heading=False
    )

    return(first_section + "\n" + second_section)

# jewels_template([["Pending Unlocked Jewels", "something", "something"],
#                 ["something", "something", "something"]])
