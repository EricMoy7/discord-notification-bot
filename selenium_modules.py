from selenium.webdriver.common.by import By


def get_table_data(driver, table_xpath):
    """
    Parameters - driver (object: selenium driver), table_xpath (string: xpath to table
    on webpage)

    Returns table in a double string list format
    """

    # Finds all rows in the table to iterate through
    table = driver.find_element(
        By.XPATH, table_xpath)
    table_rows = table.find_elements(By.TAG_NAME, "tr")

    # Initializes final table
    new_table = []

    # Iterates through all table cells
    for table_row in table_rows:
        table_columns = table_row.find_elements(By.TAG_NAME, "td")
        new_row = [item.text for item in table_columns]
        if (new_row):
            new_table.append(new_row)

    return new_table
