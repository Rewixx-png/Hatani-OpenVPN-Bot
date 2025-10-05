# utils/vpn_script.py

import asyncio
import logging
from config import VPN_SCRIPT_PATH

async def run_script_command(command: str) -> tuple[int, str]:
    """
    Запускает команду в оболочке асинхронно и возвращает (код_выхода, вывод).
    """
    process = await asyncio.create_subprocess_shell(
        command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    output = (stdout.decode().strip() + "\n" + stderr.decode().strip()).strip()
    
    if process.returncode != 0:
        logging.error(f"Скрипт '{command}' завершился с кодом {process.returncode}. Вывод:\n{output}")
    else:
        logging.info(f"Скрипт '{command}' завершился успешно. Вывод:\n{output}")
        
    return process.returncode, output

async def create_vpn_config(client_name: str) -> bool:
    """
    Вызывает наш новый скрипт для создания конфига.
    Возвращает True в случае успеха (код выхода 0).
    """
    command = f"bash {VPN_SCRIPT_PATH} add {client_name}"
    return_code, _ = await run_script_command(command)
    return return_code == 0

async def revoke_vpn_config(client_name: str) -> bool:
    """
    Вызывает наш новый скрипт для отзыва конфига.
    Возвращает True в случае успеха (код выхода 0).
    """
    command = f"bash {VPN_SCRIPT_PATH} revoke {client_name}"
    return_code, _ = await run_script_command(command)
    return return_code == 0