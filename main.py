# bot.py
import os
import time

import discord
from dotenv import load_dotenv
from discord.ext import tasks

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium_modules import get_table_data, chrome_takeFullScreenshot
from defi_modules import jewels_template
from bulkrun_modules import bulk_run_pools

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()


@tasks.loop(minutes=10)
async def test():
    # Get Discord client
    channel = client.get_channel(900841296346886144)

    # Setup ENV vars and Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    one_address = os.getenv("ONE_ADDRESS")

    capabilities = {
        'browserName': 'chrome',
        'chromeOptions':  {
            'useAutomationExtension': False,
            'args': ['--disable-infobars']
        }
    }
    driver = webdriver.Chrome(options=chrome_options,
                              desired_capabilities=capabilities)
    driver.get(f"https://kingdom.watch/personal/{one_address}")

    WebDriverWait(driver, 60).until(
        EC.invisibility_of_element_located((By.CLASS_NAME, 'progress')))
    time.sleep(2)

    # Get Jewel table data and send to Discord
    table_data = get_table_data(
        driver, f"/html/body/div/div[2]/div[1]/div[1]/div/div/table")
    total_jewel_msg = jewels_template(table_data)
    await channel.send(f"```{total_jewel_msg}```")

    # Get all pool data and send to discord
    await bulk_run_pools(channel, driver,
                         ["JEWEL / WONE", "JEWEL / BUSD", "JEWEL / MIS"])

    # Send mobile Image
    png = chrome_takeFullScreenshot(driver)
    screenshot_name = "jewelInfo.png"
    with open(screenshot_name, 'wb') as f:
        f.write(png)
    channel2 = client.get_channel(903409838401417216)
    await channel2.send(file=discord.File(screenshot_name))

    # Clean up all functions
    driver.close()
    if os.path.exists(screenshot_name):
        os.remove(screenshot_name)
    else:
        print("Screenshot info for Jewel was not found")


@ client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    test.start()

client.run(TOKEN)
