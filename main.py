# --- НАЧАЛО ФАЙЛА automation_relative_paths_ru.py ---

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoSuchElementException, TimeoutException, NoAlertPresentException,
    ElementClickInterceptedException, StaleElementReferenceException
)

import time
import os
import json
import base64
import random
import platform
import urllib.parse
import subprocess
import re

# --- Настройки ---
TARGET_URL = 'https://perchance.org/ai-furry-generator'
PAGE_LOAD_TIMEOUT = 30
WAIT_TIMEOUT = 25
IMAGE_APPEARANCE_TIMEOUT = 360
DOWNLOAD_DIR = "generated_images"

# --- ОТНОСИТЕЛЬНЫЕ ПУТИ (относительно папки со скриптом) ---
PROFILE_DIR_NAME = "chrome_profile_data"  # Имя папки для профиля
# Относительный путь к исполняемому файлу браузера
BROWSER_RELATIVE_PATH = os.path.join("Application","chrome.exe")

# Получаем абсолютный путь к папке, где лежит скрипт
script_dir = os.path.dirname(os.path.abspath(__file__))

# Строим АБСОЛЮТНЫЕ пути на основе относительных
CHROME_PROFILE_PATH = os.path.join(script_dir, PROFILE_DIR_NAME)
BROWSER_EXECUTABLE_PATH = os.path.join(script_dir, BROWSER_RELATIVE_PATH)

# Создаем папку профиля, если ее нет
os.makedirs(CHROME_PROFILE_PATH, exist_ok=True)
print(f"Используется папка профиля: {CHROME_PROFILE_PATH}")

# Проверяем наличие браузера
if not os.path.isfile(BROWSER_EXECUTABLE_PATH):
    print("="*50); print(f"!!! ОШИБКА: Браузер НЕ НАЙДЕН:"); print(BROWSER_EXECUTABLE_PATH); print(f"Поместите браузер в папку '{os.path.dirname(BROWSER_RELATIVE_PATH)}' относительно скрипта."); print("="*50); exit()
else:
    print(f"Используется браузер: {BROWSER_EXECUTABLE_PATH}")

print("INFO: undetected-chromedriver будет автоматически искать chromedriver.")

# --- Параметры генерации ---
PROMPT = "Loona,вид всего тела, заря позади Loona,Детализованное аниме"
NEGATIVE_PROMPT = "blurry, low quality, deformed, mutated, ugly, disfigured, text, words, watermark, signature, username, lowres, bad anatomy, clothes, clothing"
ART_STYLE = "Random Style ⚄"
ASPECT_RATIO = "All ⚄"
BATCH_SIZE = "8"  # Можно изменить на большее значение, например "8" или "12" и тд кр что есть на самом сайте
MAX_IMAGES_TO_WAIT = 12  # Максимальное количество изображений для ожидания (если BATCH_SIZE > 4)
FURRY_MODE = True
CONTENT_LABEL = False # Установите False, если нужно PG-13 True если 18

# Функция для получения версии Chrome
def get_chrome_version():
    try:
        # Прямое указание версии 135, так как из ошибки известно, что версия Chrome 135
        print("Используем версию Chrome 135")
        return 135  # Возвращаем число, а не строку
    except Exception as e:
        print(f"Ошибка при определении версии Chrome: {e}. Используем версию 135.")
        return 135

# Получаем версию Chrome
chrome_version = get_chrome_version()

# --- Инициализация Chrome с относительными путями ---
chrome_options = uc.ChromeOptions()
chrome_options.add_argument('--start-maximized')
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
chrome_options.add_argument("--log-level=3")
chrome_options.add_argument('--disable-infobars')
# Используем АБСОЛЮТНЫЙ путь к профилю
chrome_options.add_argument(f'--user-data-dir={CHROME_PROFILE_PATH}')

driver = None
try:
    print("Инициализация undetected_chromedriver (авто-поиск драйвера)...")
    # Используем АБСОЛЮТНЫЙ путь к браузеру и версию Chrome
    driver = uc.Chrome(
        options=chrome_options,
        browser_executable_path=BROWSER_EXECUTABLE_PATH,
        version_main=chrome_version  # Используем определённую выше версию
    )
    print("OK: Undetected chromedriver инициализирован.")
except Exception as e:
     print(f"ERR: Ошибка инициализации uc:"); print(e)
     print("\nПричины:\n- Браузер недоступен.\n- Не найден совместимый chromedriver.\n- Профиль используется.")
     exit()

# --- Остальной код (Wait'ы, функции, основной блок try/except/finally) ---
# --- БЕЗ ИЗМЕНЕНИЙ --- (Скопируйте из предыдущего ответа)
page_wait = WebDriverWait(driver, PAGE_LOAD_TIMEOUT)
element_wait = WebDriverWait(driver, WAIT_TIMEOUT)
image_wait = WebDriverWait(driver, IMAGE_APPEARANCE_TIMEOUT)
os.makedirs(DOWNLOAD_DIR, exist_ok=True)
def random_delay(min_sec=0.4, max_sec=1.2): time.sleep(random.uniform(min_sec, max_sec))
def human_like_typing(element, text):
    print(f"Ввод: '{text[:30]}...'");
    for char in text: element.send_keys(char); time.sleep(random.uniform(0.02, 0.08))
    print("OK: Ввод завершен."); random_delay(0.3, 0.6)
def scroll_to_element_smooth(element):
    try:
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
        print(f"Скролл к: {element.tag_name}({element.get_attribute('data-name') or element.get_attribute('id') or ''})")
        random_delay(0.6, 1.1)
    except Exception as e:
        print(f"Warn: Плавный скролл fail ({e}). Стандартный.");
        try: driver.execute_script("arguments[0].scrollIntoView(true);", element); random_delay(0.4, 0.7)
        except Exception as e2: print(f"ERR: Стандартный скролл fail: {e2}")
def click_element_robust(element_or_locator, wait_time=WAIT_TIMEOUT):
    print(f"Клик: {element_or_locator}"); element=None
    try:
        if isinstance(element_or_locator, tuple): element = WebDriverWait(driver, wait_time).until(EC.presence_of_element_located(element_or_locator))
        else: element = element_or_locator
        scroll_to_element_smooth(element)
        element = WebDriverWait(driver, wait_time).until(EC.element_to_be_clickable(element))
        random_delay(0.3, 0.7)
        try: print("JS-клик..."); driver.execute_script("arguments[0].click();", element); print("OK: JS-клик."); return True
        except Exception as js_e:
            print(f"JS-клик fail: {js_e}. Стандартный.");
            try: element.click(); print("OK: Стандартный клик."); return True
            except ElementClickInterceptedException as ice:
                print(f"Перехвачен: {ice}. Повтор JS."); random_delay(1.0, 2.0)
                try: driver.execute_script("arguments[0].click();", element); print("OK: Повтор JS-клик."); return True
                except Exception as js_e2: print(f"Повтор JS fail: {js_e2}")
            except Exception as e: print(f"Стандартный клик fail: {e}")
        print("ERR: Все клики fail."); return False
    except TimeoutException: print(f"ERR: Элемент не найден/кликабелен за {wait_time} сек."); return False
    except StaleElementReferenceException: print("ERR: Элемент устарел."); return False
    except Exception as e: print(f"ERR: Ошибка клика: {e}"); return False
def set_select_by_visible_text(element, text):
    try: scroll_to_element_smooth(element); select = Select(element); select.select_by_visible_text(text); print(f"Выбрано '{text}'.")
    except NoSuchElementException: print(f"Warn: Опция '{text}' не найдена.")
    except Exception as e: print(f"ERR: Ошибка выбора '{text}': {e}")
def set_select_by_value(element, value):
    try: scroll_to_element_smooth(element); select = Select(element); select.select_by_value(value); print(f"Выбрана опция '{value}'.")
    except NoSuchElementException:
        option_text = f"value '{value}'"; options = select.options; found_option = next((opt for opt in options if opt.get_attribute('value') == value), None)
        if found_option: option_text = f"'{found_option.text}' (value: {value})"
        print(f"Warn: Опция {option_text} не найдена.")
    except Exception as e: print(f"ERR: Ошибка выбора опции '{value}': {e}")
def save_base64_image(base64_str, filename):
    try:
        if ';base64,' in base64_str: header, encoded = base64_str.split(';base64,', 1)
        else: print(f"Warn: Не base64 формат {filename}."); encoded = base64_str
        missing_padding = len(encoded) % 4
        if missing_padding: encoded += '=' * (4 - missing_padding)
        img_data = base64.b64decode(encoded)
        with open(filename, 'wb') as f: f.write(img_data)
        print(f"OK: Сохранено: {filename}")
    except base64.binascii.Error as b64_err: print(f"ERR: Ошибка Base64 {filename}: {b64_err}")
    except Exception as e: print(f"ERR: Ошибка сохранения {filename}: {e}")
def save_screenshot_safe(driver_instance, filename):
    if driver_instance:
        try: driver_instance.save_screenshot(filename)
        except Exception as e: print(f"Warn: Ошибка скриншота ({filename}): {e}")

# Функция для медленной прокрутки вниз по 1 пикселю
def slow_scroll_down(total_pixels=200, delay=0.05):
    print(f"Медленная прокрутка вниз на {total_pixels}px (по 1px)...")
    for i in range(total_pixels):
        driver.execute_script("window.scrollBy(0, 1);")
        if i % 20 == 0:  # Выводим сообщение каждые 20 пикселей
            print(f"Прокручено {i}px из {total_pixels}...")
        time.sleep(delay)  # Маленькая задержка между прокрутками
    print(f"Медленная прокрутка завершена.")
    random_delay(0.5, 1.0)

# Функция для прокрутки, чтобы активировать генерацию
def scroll_to_activate_generation():
    print("Прокрутка для активации генерации...")
    
    # Прокрутка к summary
    try:
        # Сначала пробуем найти специфический summary
        summary_elements = driver.find_elements(*summary_locator)
        if summary_elements:
            print("Прокрутка к summary с правилами...")
            scroll_to_element_smooth(summary_elements[0])
            random_delay(1.0, 2.0)
        else:
            # Если не нашли, пробуем любой summary
            any_summary = driver.find_elements((By.CSS_SELECTOR, 'summary'))
            if any_summary:
                print("Прокрутка к первому summary...")
                scroll_to_element_smooth(any_summary[0])
                random_delay(1.0, 2.0)
    except Exception as e:
        print(f"Warn: Ошибка прокрутки к summary: {e}")
    
    # Прокрутка к prompt
    try:
        prompt_element = driver.find_element(*prompt_locator)
        print("Прокрутка к prompt...")
        scroll_to_element_smooth(prompt_element)
        random_delay(1.0, 2.0)
    except Exception as e:
        print(f"Warn: Ошибка прокрутки к prompt: {e}")
    
    # Прокрутка к существующим изображениям
    try:
        current_iframes = driver.find_elements(*image_iframe_locator)
        if current_iframes:
            # Прокручиваем к первому и последнему изображению, 
            # чтобы активировать генерацию остальных
            print(f"Прокрутка к первому изображению...")
            scroll_to_element_smooth(current_iframes[0])
            random_delay(0.8, 1.5)
            
            if len(current_iframes) > 1:
                print(f"Прокрутка к последнему изображению...")
                scroll_to_element_smooth(current_iframes[-1])
                random_delay(0.8, 1.5)
                
            # Если ожидается много изображений, прокручиваем к каждому третьему
            if len(current_iframes) > 4:
                for i in range(2, len(current_iframes), 3):
                    if i < len(current_iframes):
                        print(f"Прокрутка к изображению {i+1}...")
                        scroll_to_element_smooth(current_iframes[i])
                        random_delay(0.6, 1.0)
                
                # Добавляем медленную прокрутку по 1 пикселю для больших генераций
                slow_scroll_down(200, 0.03)
    except Exception as e:
        print(f"Warn: Ошибка прокрутки к изображениям: {e}")
    
    # Случайная прокрутка вверх-вниз
    for _ in range(2):
        try:
            scroll_dir = random.choice([-1, 1])
            scroll_dist = random.randint(100, 300)
            driver.execute_script(f"window.scrollBy(0, {scroll_dir * scroll_dist});")
            print(f"Скролл {scroll_dir * scroll_dist}px")
            random_delay(0.5, 1.0)
        except Exception as e:
            print(f"Warn: Ошибка случайной прокрутки: {e}")

try:
    print(f"URL: {TARGET_URL}")
    driver.get(TARGET_URL)
    page_wait.until(lambda d: d.execute_script('return document.readyState') == 'complete')
    print("OK: Страница загружена."); random_delay(1.0, 2.0)

    # --- Переключение в Iframe ---
    try:
        print("Переключение в iframe 'outputIframeEl'..."); iframe_main = element_wait.until(EC.presence_of_element_located((By.ID, 'outputIframeEl')))
        driver.switch_to.frame(iframe_main); print("OK: в основном iframe.")
        element_wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'textarea[data-name="description"]'))); print("OK: содержимое iframe готово."); random_delay(0.8, 1.5)
    except TimeoutException: print("ERR: Не найден iframe 'outputIframeEl'."); save_screenshot_safe(driver, 'error_iframe_main_not_found.png'); raise

    # --- Окно согласия ---
    try:
        print("Кнопка согласия..."); consent_button_locator = (By.ID, 'consent-btn')
        if not click_element_robust(consent_button_locator, wait_time=15): print("Не нажата/нет.")
        else: print("OK: Кнопка согласия нажата."); random_delay(0.8, 1.5)
    except Exception as e: print(f"Warn: Ошибка согласия: {e}")

    # --- Заполнение полей ---
    print("Заполнение полей v3...");
    try:
        # Промпт
        prompt_field=element_wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'textarea[data-name="description"]')))
        scroll_to_element_smooth(prompt_field); prompt_field.click(); random_delay(0.1, 0.4)
        prompt_field.clear(); random_delay(0.4, 0.8); human_like_typing(prompt_field, PROMPT)
        # Alert
        try: WebDriverWait(driver, 2).until(EC.alert_is_present()); alert = driver.switch_to.alert; print(f"Alert: {alert.text}"); alert.accept(); print("Alert закрыт."); random_delay(0.8, 1.5)
        except TimeoutException: print("Alert не найден (таймаут).")
        except NoAlertPresentException: print("Alert не найден (NoAlert).")
        # Негативный промпт
        negative_field=element_wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'textarea[data-name="negative"]')))
        scroll_to_element_smooth(negative_field); negative_field.click(); random_delay(0.1, 0.4)
        negative_field.clear(); random_delay(0.4, 0.8); human_like_typing(negative_field, NEGATIVE_PROMPT)
        # Селекты
        art_style_select=element_wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'select[data-name="artStyle"]')))
        set_select_by_visible_text(art_style_select, ART_STYLE); random_delay(0.2,0.5)
        furry_select=element_wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'select[data-name="furry"]')))
        set_select_by_value(furry_select, ", (anthro:0.1)" if FURRY_MODE else ""); random_delay(0.2,0.5)
        aspect_select=element_wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'select[data-name="shape"]')))
        set_select_by_value(aspect_select, ASPECT_RATIO); random_delay(0.2,0.5)
        batch_select=element_wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'select[data-name="numImages"]')))
        set_select_by_value(batch_select, BATCH_SIZE); random_delay(0.2,0.5)
        if CONTENT_LABEL:
            try: label_select=element_wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'select[data-name="sensitive"]'))); set_select_by_visible_text(label_select, "⚠︎ 18+"); random_delay(0.2,0.5)
            except Exception as e: print(f"Warn: Не удалось 18+: {e}")
        # Скроллинг
        print("Скроллинг..."); scroll_amount = 80
        for _ in range(random.randint(1, 3)):
            scroll_dir=random.choice([-1, 1]); scroll_dist=random.randint(int(scroll_amount*0.4), int(scroll_amount*1.2)); driver.execute_script(f"window.scrollBy(0, {scroll_dir * scroll_dist});"); print(f"Скролл {scroll_dir * scroll_dist}px"); random_delay(0.3, 0.6)
    except TimeoutException as e: print(f"ERR: Элемент формы не найден."); save_screenshot_safe(driver, 'error_form_element_not_found.png'); raise
    except Exception as e: print(f"ERR: Ошибка заполнения: {e}"); save_screenshot_safe(driver, 'error_filling_fields.png'); raise

    # --- Запуск генерации ---
    try:
        print("Кнопка генерации..."); generate_button_locator = (By.ID, 'generateButtonEl')
        print("Пауза..."); random_delay(2.0, 4.0)
        print("Клик кнопки генерации...")
        if not click_element_robust(generate_button_locator): raise Exception("Не удалось кликнуть кнопку генерации.")
        print("OK: Кнопка генерации нажата.")
    except Exception as e: print(f"ERR: Ошибка клика генерации: {e}"); save_screenshot_safe(driver, 'error_clicking_generate.png'); raise

    # --- ОЖИДАНИЕ ПОЯВЛЕНИЯ IFRAMES ---
    expected_image_count = int(BATCH_SIZE)
    max_images_to_wait = min(expected_image_count, MAX_IMAGES_TO_WAIT)  # Ограничиваем максимальное количество
    print(f"Ожидание до {max_images_to_wait} iframe(ов) (таймаут: {IMAGE_APPEARANCE_TIMEOUT} сек)...")
    image_iframe_locator = (By.CSS_SELECTOR, '#outputAreaEl .t2i-image-ctn iframe')
    # Специфический селектор для summary с подсказкой о правилах
    summary_locator = (By.CSS_SELECTOR, 'summary[style="cursor:pointer;"]')
    prompt_locator = (By.CSS_SELECTOR, 'textarea[data-name="description"]')
    image_iframes = []

    try:
        # Сначала ждем хотя бы одно изображение
        print("Ожидание первого изображения...")
        image_wait.until(lambda drv: len(drv.find_elements(*image_iframe_locator)) > 0)
        print("OK: Первое изображение обнаружено")
        
        # Затем ждем все остальные с периодической прокруткой
        start_time = time.time()
        last_scroll_time = start_time
        last_slow_scroll_time = start_time
        scroll_interval = 15  # секунд между прокрутками
        slow_scroll_interval = 7  # секунд между медленными прокрутками
        
        while time.time() - start_time < IMAGE_APPEARANCE_TIMEOUT:
            current_iframes = driver.find_elements(*image_iframe_locator)
            current_count = len(current_iframes)
            
            if current_count >= max_images_to_wait:
                print(f"OK: Обнаружено {current_count} iframe(ов) - все готовы!")
                break
            
            # Если прошло более N секунд с последней прокрутки, прокручиваем
            if time.time() - last_scroll_time > scroll_interval:
                print(f"Сгенерировано {current_count} из {max_images_to_wait} изображений. Активируем генерацию...")
                scroll_to_activate_generation()
                last_scroll_time = time.time()
                last_slow_scroll_time = time.time()  # Сбрасываем и таймер медленной прокрутки
            
            # Медленная прокрутка для активации скрытых изображений
            elif time.time() - last_slow_scroll_time > slow_scroll_interval and current_count > 4:
                print(f"Выполняем медленную прокрутку для активации генерации (текущее кол-во: {current_count})...")
                slow_scroll_down(100, 0.02)  # Меньшее количество пикселей и меньшая задержка
                last_slow_scroll_time = time.time()
            
            # Короткое ожидание перед следующей проверкой
            time.sleep(1)
        
        # Получаем все найденные iframes
        all_iframes = driver.find_elements(*image_iframe_locator)
        if len(all_iframes) >= max_images_to_wait:
            image_iframes = all_iframes[:max_images_to_wait]  # Берем только нужное количество
            print(f"OK: Обнаружено {len(all_iframes)} iframe(ов), обрабатываем {max_images_to_wait}.")
        else:
            print(f"Warn: Найдено только {len(all_iframes)} из {max_images_to_wait} iframe(ов).")
            image_iframes = all_iframes
        
        random_delay(1.0, 2.0)
        print(f"Обработка {len(image_iframes)} iframe(ов).")
        
    except TimeoutException:
        print(f"ERR: Не дождались ни одного iframe за {IMAGE_APPEARANCE_TIMEOUT} сек.")
        current_iframes = driver.find_elements(*image_iframe_locator)
        print(f"(Найдено {len(current_iframes)})")
        image_iframes = current_iframes
        save_screenshot_safe(driver, 'error_image_iframes_timeout.png')
        if not image_iframes: raise Exception("Генерация не удалась: изображения не появились.")
    except Exception as e: 
        print(f"ERR: Ошибка ожидания/поиска iframes: {e}")
        save_screenshot_safe(driver, 'error_finding_image_iframes.png')
        current_iframes = driver.find_elements(*image_iframe_locator)
        image_iframes = current_iframes

    # --- Извлечение и сохранение ---
    saved_count = 0
    if image_iframes:
        print("Извлечение из iframes...");
        for idx, iframe_element in enumerate(image_iframes, 1):
            seed = "unknown_seed"
            try:
                print(f"Iframe #{idx}...");
                retry_count = 0
                max_retries = 3
                
                # Извлекаем seed
                try:
                    iframe_src = iframe_element.get_attribute('src');
                    if iframe_src and '#' in iframe_src:
                        encoded_json_part = iframe_src.split('#', 1)[1]; decoded_json_str = urllib.parse.unquote(encoded_json_part)
                        iframe_data = json.loads(decoded_json_str); seed = iframe_data.get('seed', seed); print(f"  Seed: {seed}")
                    else: print("  Warn: Нет JSON в src.")
                except Exception as seed_err: print(f"  Warn: Ошибка извлечения seed: {seed_err}")

                # Пробуем получить изображение с повторными попытками
                while retry_count < max_retries:
                    try:
                        driver.switch_to.frame(iframe_element); random_delay(0.1, 0.4)
                        
                        # Ждем появления изображения с коротким таймаутом
                        wait_time = 8 if retry_count == 0 else 15  # Увеличиваем время ожидания с каждой попыткой
                        img_tag = WebDriverWait(driver, wait_time).until(EC.presence_of_element_located((By.TAG_NAME, 'img')))
                        
                        # Проверяем, что изображение загружено
                        is_complete = driver.execute_script("return arguments[0].complete && typeof arguments[0].naturalWidth != 'undefined' && arguments[0].naturalWidth > 0", img_tag)
                        
                        if not is_complete:
                            print(f"  Warn: Изображение #{idx} еще загружается, ожидание...")
                            # Дополнительное ожидание для загрузки
                            time.sleep(2)
                            is_complete = driver.execute_script("return arguments[0].complete && typeof arguments[0].naturalWidth != 'undefined' && arguments[0].naturalWidth > 0", img_tag)
                        
                        base64_data = img_tag.get_attribute('src')
                        driver.switch_to.parent_frame(); random_delay(0.1, 0.4)

                        if base64_data and base64_data.startswith('data:image'):
                            filename = os.path.join(DOWNLOAD_DIR, f"image_{idx}_seed{seed}.png")
                            save_base64_image(base64_data, filename)
                            saved_count += 1
                            break  # Успешно получили и сохранили, выходим из цикла повторов
                        else:
                            print(f"  Warn: Данные изображения #{idx} не в формате base64, повтор...")
                            retry_count += 1
                            if retry_count < max_retries:
                                print(f"  Попытка {retry_count+1}/{max_retries}...")
                                time.sleep(2)  # Ждем перед повторной попыткой
                    except TimeoutException:
                        print(f"  Warn: Таймаут ожидания <img> в iframe #{idx}, повтор...")
                        try: driver.switch_to.parent_frame()
                        except: pass
                        retry_count += 1
                        if retry_count < max_retries:
                            print(f"  Попытка {retry_count+1}/{max_retries}...")
                            # Пробуем активировать генерацию медленной прокруткой
                            slow_scroll_down(50, 0.02)
                            time.sleep(1)
                    except Exception as e:
                        print(f"  ERR: Ошибка извлечения изображения #{idx}: {e}")
                        try: driver.switch_to.parent_frame()
                        except: pass
                        retry_count += 1
                        if retry_count < max_retries:
                            print(f"  Попытка {retry_count+1}/{max_retries}...")
                            time.sleep(1)
                
                # Если все попытки исчерпаны
                if retry_count >= max_retries:
                    print(f"  ERR: Не удалось извлечь изображение #{idx} после {max_retries} попыток.")
                
            except Exception as e:
                print(f"ERR: Ошибка обработки iframe #{idx}: {e}")
                try: driver.switch_to.parent_frame()
                except Exception as switch_err: print(f"  (Warn: Ошибка возврата из iframe #{idx}: {switch_err})")
            print("-" * 10)

    if saved_count == max_images_to_wait: print(f"OK: Успешно сохранено {saved_count} изображений.")
    elif saved_count > 0: print(f"Warn: Сохранено {saved_count} из {max_images_to_wait}.")
    elif not image_iframes: print("Сохранение не выполнено (нет iframes).")
    else: print("ERR: Не удалось сохранить из найденных iframes.")

except TimeoutException as e: print(f"Крит. ERR: Таймаут - {e}"); save_screenshot_safe(driver, 'error_timeout.png')
except NoSuchElementException as e: print(f"Крит. ERR: Элемент не найден - {e}"); save_screenshot_safe(driver, 'error_no_such_element.png')
except Exception as e:
    print(f"Крит. ERR: {type(e).__name__} - {str(e)}")
    import traceback; traceback.print_exc()
    save_screenshot_safe(driver, 'error_unknown.png')
finally:
    if driver:
        try: print("Переключение из iframe..."); driver.switch_to.default_content()
        except Exception as e: print(f"Warn: Ошибка переключения из iframe: {e}")
        print("Закрытие браузера..."); driver.quit()
    print("Скрипт завершен.")

# --- КОНЕЦ ФАЙЛА ---
