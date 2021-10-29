from selenium_modules import get_table_from_name
from defi_modules import pool_template
import time


async def bulk_run_pools(channel, driver, pool_names):
    for name in pool_names:
        await channel.send(f"```{pool_template(get_table_from_name(driver, name))}```")
        time.sleep(1)
    return
