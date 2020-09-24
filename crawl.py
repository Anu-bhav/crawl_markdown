import pyautogui, os, requests, re, random
from msedge.selenium_tools import Edge, EdgeOptions, webdriver
from time import sleep, time
from bs4 import BeautifulSoup
from http_request_randomizer.requests.proxy.requestProxy import RequestProxy
from pprint import pprint
from collections import OrderedDict


def Download(path, url, proxy):
    # add edgedriver_win46/msedgedriver.exe to path
    options = EdgeOptions()
    options.use_chromium = True
    unpacked_extension_path = os.path.join(os.getcwd(), "markdown-clipper")
    options.add_argument("--load-extension={}".format(unpacked_extension_path))
    options.add_argument("--proxy-server=http://{}".format(proxy))
    download_path = os.path.join(os.getcwd(), "Markdown Output\\", path)
    prefs = {"download.default_directory": download_path, "profile.default_content_settings.popups": 0, "directory_upgrade": True}
    options.add_experimental_option("prefs", prefs)
    options.add_experimental_option("detach", True)
    driver = Edge(options=options)

    driver.get(url)
    sleep(5)

    # # click to close agree cookies
    # extn = [899, 1040]
    # pyautogui.click(x=extn[0], y=extn[1], clicks=1, interval=0.0, button="left")
    # sleep(5)

    # click on markdown clipper extension icon
    CloseAds(driver)
    extn = [714, 72]
    pyautogui.click(x=extn[0], y=extn[1], clicks=1, interval=0.0, button="left")
    sleep(2)

    # click on save button for download dialog, mouse is automatically over save button
    extn = pyautogui.position()
    pyautogui.click(x=extn[0], y=extn[1], clicks=1, interval=0.0, button="left")
    driver.close()


def make_dir(path):
    download_path = os.path.join(os.getcwd(), "Markdown Output\\", path)
    os.makedirs(download_path, exist_ok=True)


def CloseAds(driver):
    agree = driver.find_elements_by_xpath('//*[@id="catapult-cookie-bar"]/div/div')
    join = driver.find_elements_by_xpath("/html/body/div[9]/div/div/button")

    if agree:
        try:
            agree[0].click()
        except Exception:
            pass
    if join:
        try:
            join[0].click()
        except Exception:
            pass


# def Crawl(url, pattern):
def Crawl(url):

    req_proxy = RequestProxy()
    proxies = req_proxy.get_proxy_list()
    proxy = random.choice(proxies).get_address()

    req = req_proxy.generate_proxied_request(url)
    soup = BeautifulSoup(req.text, "html.parser")
    course = soup.title.text.split("|")[0].strip()
    print(course)
    # gets all links directly
    # for link in soup.find_all("a", {"href": re.compile(pattern)}):
    #     print(link.get("href"))

    spans = soup.find_all("ul", {"class": "bellows-nav"})

    title_list = []
    links_list = OrderedDict()

    for span in spans:
        for title in span.find_all("span", {"class": "bellows-target-title"}):
            text = title.text.replace(":", " -")
            title_list.append(text)

        for item2 in span.find_all("a", {"class": "bellows-target"}, href=True):
            links_list[item2.text] = item2["href"]

    unit_index = []
    links_index = []

    for i, item in enumerate(title_list):
        if "Unit " in item:
            unit_index.append(i)

    for link in links_list:
        links_index.append([index for index, num in enumerate(title_list) if link in num][0])

    for i, unit in enumerate(unit_index):
        for link in links_index:
            try:
                # print(link, unit, unit_index[i + 1])
                if (unit < link) and (link < unit_index[i + 1]):
                    print(title_list[unit], " ---- ", title_list[link], " ---- ", links_list[title_list[link]])
                    # Unit 1 - Introduction  ----  How to study Networking  ----  https://...
                    path_to_download = course + "\\" + title_list[unit]
                    link_to_download = links_list[title_list[link]]
                    make_dir(path_to_download)
                    Download(path_to_download, link_to_download, proxy)
                    # sleep(10)
            except (IndexError, ValueError):
                break


# Crawl("https://networklessons.com/cisco/ccna-200-301", "ccna-200-301/")
Crawl("https://networklessons.com/cisco/ccna-200-301")