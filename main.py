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

from selenium_modules import get_table_data

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()


@tasks.loop(minutes=30)
async def test():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    one_address = os.getenv("ONE_ADDRESS")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(f"https://kingdom.watch/personal/{one_address}")

    WebDriverWait(driver, 10).until(
        EC.invisibility_of_element_located((By.CLASS_NAME, 'progress')))

    get_table_data(
        driver, f"/html/body/div/div[2]/div[1]/div[1]/div/div/table")
    # channel = client.get_channel(900841296346886144)
    # await channel.send(file=jewel_table)
    driver.close()


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    test.start()

client.run(TOKEN)
