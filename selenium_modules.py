from selenium.webdriver.common.by import By
import json
import base64
from PIL import Image


def get_table_data(driver, table_xpath):
    """
    Parameters - driver (object: selenium driver), table_xpath (string: xpath to table
    on webpage)

    Returns table in a double string list format
    """

    # Finds all rows in the table to iterate through
    if isinstance(table_xpath, str):
        table = driver.find_element(
            By.XPATH, table_xpath)
    else:
        table = table_xpath

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


def get_table_from_name(driver, name):
    header_name = driver.find_element(
        By.XPATH, f"//*[contains(text(), '{name}')]")
    header_parent = header_name.find_element(By.XPATH, "./..")

    return(get_table_data(driver, header_parent))


def chrome_takeFullScreenshot(driver):
    """
    From https://stackoverflow.com/questions/45199076/take-full-page-screenshot-in-chrome-with-selenium
    """

    def send(cmd, params):
        resource = "/session/%s/chromium/send_command_and_get_result" % driver.session_id
        url = driver.command_executor._url + resource
        body = json.dumps({'cmd': cmd, 'params': params})
        response = driver.command_executor._request('POST', url, body)
        return response.get('value')

    def evaluate(script):
        response = send('Runtime.evaluate', {
                        'returnByValue': True, 'expression': script})
        return response['result']['value']

    metrics = evaluate(
        "({" +
        "width: Math.max(window.innerWidth, document.body.scrollWidth, document.documentElement.scrollWidth)|0," +
        "height: Math.max(innerHeight, document.body.scrollHeight, document.documentElement.scrollHeight)|0," +
        "deviceScaleFactor: window.devicePixelRatio || 1," +
        "mobile: typeof window.orientation !== 'undefined'" +
        "})")
    send('Emulation.setDeviceMetricsOverride', metrics)
    screenshot = send('Page.captureScreenshot', {
                      'format': 'png', 'fromSurface': True})
    send('Emulation.clearDeviceMetricsOverride', {})

    return base64.b64decode(screenshot['data'])
