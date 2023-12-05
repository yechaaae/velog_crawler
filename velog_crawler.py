from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

def scroll_down(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

def crawl_data(url, driver_path, max_data, min_like, mode):
    options = webdriver.ChromeOptions()
    #options.add_argument('--headless')
    driver = webdriver.Chrome(executable_path=driver_path, options=options)        

    try:
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'PostCard_block__t_0t8')))

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        # 초기화된 데이터 수집
        cards = soup.find_all('div', class_='PostCard_block__t_0t8')

        # 현재까지 수집된 데이터의 개수
        data_count = 0

        for card in cards:
            card_main = card.find('div', class_='PostCard_content__DxJzL')
            card_sub = card.find('div', class_='PostCard_subInfo__aMAtH')
            card_foot = card.find('div', class_='PostCard_footer__CONJG')

            title_tag = card_main.find('h4', class_='PostCard_h4__Yj8PZ')
            title = title_tag.text.strip() if title_tag else "N/A"

            description_tag = card_main.find('p', class_='PostCard_clamp__jvmBn')
            description = description_tag.text.strip() if description_tag else "N/A"

            link_tag = card_main.find('a', class_='VLink_block__Uwj4P')
            link = link_tag['href'] if link_tag else "N/A"

            writer_tag = card_foot.find('b')
            writer = writer_tag.text.strip() if writer_tag else 'N/A'

            like_tag = card_foot.find('div', 'PostCard_likes__pWcUv')
            like = like_tag.text.strip() if like_tag else 'N/A'

            if like != 'N/A' and int(like) >= min_like:
                yield {'Title': title, 'Description': description, 'Link': link, 'Writer' : writer, 'Like' : like}
                data_count += 1

            if data_count >= max_data:
                return

        # 추가적인 스크롤 동작
        while data_count < max_data:
            scroll_down(driver)

            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            new_cards = soup.find_all('div', class_='PostCard_block__t_0t8')

            for new_card in new_cards:
                new_card_main = new_card.find('div', class_='PostCard_content__DxJzL')
                new_card_sub = new_card.find('div', class_='PostCard_subInfo__aMAtH')
                new_card_foot = new_card.find('div', class_='PostCard_footer__CONJG')
                
                title_tag = new_card_main.find('h4', class_='PostCard_h4__Yj8PZ')
                title = title_tag.text.strip() if title_tag else "N/A"

                description_tag = new_card_main.find('p', class_='PostCard_clamp__jvmBn')
                description = description_tag.text.strip() if description_tag else "N/A"

                link_tag = new_card_main.find('a', class_='VLink_block__Uwj4P')
                link = link_tag['href'] if link_tag else "N/A"

                writer_tag = new_card_foot.find('b')
                writer = writer_tag.text.strip() if writer_tag else 'N/A'

                like_tag = new_card_foot.find('div', 'PostCard_likes__pWcUv')
                like = like_tag.text.strip() if like_tag else 'N/A'

                if like != 'N/A' and int(like) >= min_like:
                    yield {'Title': title, 'Description': description, 'Link': link, 'Writer' : writer, 'Like' : like}
                    data_count += 1

                if data_count >= max_data:
                    return

    finally:
        driver.quit()

if __name__ == '__main__':
    url = 'https://velog.io'
    driver_path = '/Users/yechan/Documents/chromedriver-mac-arm64/chromedriver'

    mode = input("1 : 기본 , 2 : 트렌딩 , 3 : 최신, 4 : 검색\n")
    if mode == '2':
        during = input("1 : 오늘 , 2 : 이번 주 , 3 : 이번 달, 4 : 올해\n")
        if during == '1':
            url = f'{url}/trending/day'
        if during == '2':
            url = f'{url}/trending/week'
        if during == '3':
            url = f'{url}/trending/month'
        if during == '4':
            url = f'{url}/trending/year'
    if mode == '3':
        url = f'{url}/recent'

    card_num = input("가져올 글의 수를 입력하시오 :\n")
    min_like = input("최소 좋아요 수를 입력하시오 :\n")

    data_generator = crawl_data(url, driver_path, int(card_num), int(min_like), mode)

    # 결과 출력
    for i, data in enumerate(data_generator, start=1):
        print(f'{i}번째')
        print(f"Title: {data['Title']}")
        print(f"Description: {data['Description']}")
        print(f"Link: {data['Link']}")
        print(f"Writer: {data['Writer']}")
        print(f"Like: {data['Like']}")
        print('-' * 50)
