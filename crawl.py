import pyautogui, os, requests, re
from msedge.selenium_tools import Edge, EdgeOptions
from time import sleep
from bs4 import BeautifulSoup


def Download(url):
    # add edgedriver_win46/msedgedriver.exe to path
    options = EdgeOptions()
    options.use_chromium = True
    unpacked_extension_path = os.path.join(os.getcwd(), "markdown-clipper")
    options.add_argument("--load-extension={}".format(unpacked_extension_path))
    download_path = os.path.join(os.getcwd(), "Markdown Output")
    prefs = {"download.default_directory": download_path}
    options.add_experimental_option("prefs", prefs)
    driver = Edge(options=options)

    driver.get(url)
    sleep(3)
    extn = [714, 72]
    print(extn)
    pyautogui.click(x=extn[0], y=extn[1], clicks=1, interval=0.0, button="left")
    sleep(1)
    extn = pyautogui.position()
    pyautogui.click(x=extn[0], y=extn[1], clicks=1, interval=0.0, button="left")


# Download("https://www.w3schools.com/python/python_functions.asp")


def Crawl(url, pattern):
    req = requests.get(url)
    soup = BeautifulSoup(req.text, "html.parser")
    print(soup.title)

    for link in soup.find_all("a", {"href": re.compile(pattern)}):
        print(link.get("href"))


Crawl("https://networklessons.com/cisco/ccna-200-301", "ccna-200-301/")