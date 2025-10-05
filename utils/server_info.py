# utils/server_info.py

import aiohttp
import logging
import asyncio
import json

async def get_server_location_info() -> dict:
    # ... (эта функция остается без изменений) ...
    info = {"ip": "Не определен", "country": "Не определена"}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('http://ip-api.com/json/') as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get("status") == "success":
                        info["ip"] = data.get("query", info["ip"])
                        info["country"] = data.get("country", info["country"])
    except Exception as e:
        logging.error(f"Ошибка при получении информации о сервере: {e}")
    return info

# --- ОБНОВЛЕННАЯ ФУНКЦИЯ ---
async def get_speedtest_results() -> dict:
    """
    Запускает Speedtest CLI с принудительным принятием лицензий
    и возвращает результаты в виде словаря.
    """
    results = {
        "ping": "Ошибка",
        "download": "Ошибка",
        "upload": "Ошибка"
    }
    
    # Команда с флагами для неинтерактивного режима
    command = "speedtest --format=json --accept-license --accept-gdpr"
    
    try:
        logging.info("Запускаю Speedtest CLI...")
        process = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE # Ловим ошибки отдельно
        )
        
        stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=90.0)
        output = stdout.decode('utf-8').strip()
        error_output = stderr.decode('utf-8').strip()

        if process.returncode == 0 and output:
            try:
                data = json.loads(output)
                
                # Пинг в миллисекундах
                ping_ms = data.get("ping", {}).get("latency", 0)
                results["ping"] = f"{ping_ms:.2f} мс"
                
                # Скорость загрузки в Мбит/с
                download_mbps = data.get("download", {}).get("bandwidth", 0) * 8 / 1_000_000
                results["download"] = f"{download_mbps:.2f} Мбит/с"
                
                # Скорость выгрузки в Мбит/с
                upload_mbps = data.get("upload", {}).get("bandwidth", 0) * 8 / 1_000_000
                results["upload"] = f"{upload_mbps:.2f} Мбит/с"
                
                logging.info(f"Speedtest завершен: {results}")

            except json.JSONDecodeError as e:
                logging.error(f"Ошибка парсинга JSON из вывода Speedtest: {e}\nВывод: {output}")
        else:
            # Если что-то пошло не так, логируем и stdout, и stderr
            logging.error(
                f"Speedtest CLI завершился с ошибкой или пустым выводом.\n"
                f"Код возврата: {process.returncode}\n"
                f"STDOUT: {output}\n"
                f"STDERR: {error_output}"
            )
            
    except asyncio.TimeoutError:
        logging.error("Speedtest CLI превысил тайм-аут в 90 секунд.")
    except Exception as e:
        logging.error(f"Критическая ошибка при запуске Speedtest CLI: {e}", exc_info=True)
        
    return results