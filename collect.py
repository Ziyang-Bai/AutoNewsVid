from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def fetch_answers(question_url):
    chrome_options = ChromeOptions()
    chrome_options.add_argument('--headless')  # 无头模式
    chrome_options.add_argument('--disable-gpu')  # 禁用GPU加速
    chrome_options.add_argument('--no-sandbox')  # 沙盒模式
    chrome_options.add_argument('--ignore-certificate-errors')  # 忽略证书错误
    chrome_options.add_argument('lang=zh-CN')
    chrome_options.add_argument("chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')")
    # 初始化WebDriver
    service = Service(executable_path='C:/Users/Danie/Documents/GitHub/AutoNewsVid/chromedriver.exe')  # 修改为你的chromedriver路径
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        print(f"Sending request to {question_url}...")
        driver.get(question_url)

        # 显式等待页面加载完成
        wait = WebDriverWait(driver, 20)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'List-item')))

        # 模拟滚动，确保加载更多内容
        scroll_and_load(driver)

        # 获取答案列表 - 针对知乎的动态内容，使用精确的选择器
        answers = driver.find_elements(By.CSS_SELECTOR, '.List-item .RichContent-inner')

        answer_texts = []
        for i, answer in enumerate(answers[:3], start=1):
            # 获取每个答案的纯文本，防止乱码问题
            print(f"Processing answer {i}...")
            answer_text = answer.text.strip()  # 去掉前后空白字符
            answer_texts.append(answer_text)
            print(f"Answer {i}: {answer_text}")

        return answer_texts

    except Exception as e:
        print(f"An error occurred: {e}")
        return []
    finally:
        driver.quit()

def scroll_and_load(driver, scroll_pause_time=2):
    """ 模拟用户滚动，确保加载更多内容 """
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # 向下滚动页面
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause_time)

        # 计算新的滚动高度，判断是否加载了新内容
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break  # 如果没有新内容加载，则退出循环
        last_height = new_height

if __name__ == "__main__":
    # 示例问题URL
    question_url = "https://www.zhihu.com/question/640365780"

    answers = fetch_answers(question_url)
    if not answers:
        print("No answers found.")
    else:
        for i, answer in enumerate(answers, start=1):
            print(f"Answer {i}:")
            print(answer)
            print("\n")
