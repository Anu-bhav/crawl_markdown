import pyautogui, os, requests, re
from msedge.selenium_tools import Edge, EdgeOptions
from time import sleep
from bs4 import BeautifulSoup
from pprint import pprint
from collections import OrderedDict


def Download(path, url):
    # add edgedriver_win46/msedgedriver.exe to path
    options = EdgeOptions()
    options.use_chromium = True
    unpacked_extension_path = os.path.join(os.getcwd(), "markdown-clipper")
    options.add_argument("--load-extension={}".format(unpacked_extension_path))
    download_path = os.path.join(os.getcwd(), "Markdown Output\\", path)
    prefs = {"download.default_directory": download_path}
    options.add_experimental_option("prefs", prefs)
    driver = Edge(options=options)

    driver.get(url)
    sleep(5)
    extn = [714, 72]
    # print(extn)
    pyautogui.click(x=extn[0], y=extn[1], clicks=1, interval=0.0, button="left")
    sleep(2)
    extn = pyautogui.position()
    pyautogui.click(x=extn[0], y=extn[1], clicks=1, interval=0.0, button="left")


def make_dir(path):
    download_path = os.path.join(os.getcwd(), "Markdown Output\\", path)
    os.makedirs(download_path, exist_ok=True)


# def Crawl(url, pattern):
def Crawl(url):
    req = requests.get(url)
    soup = BeautifulSoup(req.text, "html.parser")
    course = soup.title.text.split("|")[0].strip()

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

    # Make Output Directories
    # for i in unit_index:
    #     path = course + "\\" + title_list[i]
    #     print(path)

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
                    Download(path_to_download, link_to_download)
            except (IndexError, ValueError):
                break


# Crawl("https://networklessons.com/cisco/ccna-200-301", "ccna-200-301/")
Crawl("https://networklessons.com/cisco/ccna-200-301")