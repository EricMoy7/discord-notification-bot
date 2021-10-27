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

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()


@tasks.loop(minutes=30)
async def test():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    address = os.getenv("ONE_ADDRESS")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(f"https://kingdom.watch/personal/{address}")

    WebDriverWait(driver, 10).until(
        EC.invisibility_of_element_located((By.CLASS_NAME, 'progress')))

    jewel_table = driver.find_element(
        By.XPATH, "/html/body/div/div[2]/div[1]/div[1]/div/div/table")
    jewel_table_rows = jewel_table.find_elements(By.TAG_NAME, "tr")
    for jewel_table_row in jewel_table_rows:
        jewel_table_columns = jewel_table_row.find_elements(By.TAG_NAME, "td")
        for jewel_table_column in jewel_table_columns:
            print(jewel_table_column.text)

    # channel = client.get_channel(900841296346886144)
    # await channel.send(file=jewel_table)
    driver.close()


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    test.start()

client.run(TOKEN)
