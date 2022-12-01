
# Medium List Scraper and PDF Downloader

# Author: Christoph Beckmann
# Description: 
# License: 

# ------------------------------------------------------------------------------
#  Importing libraries 

# Standard libraries
import os
import logging 
import time
from datetime import datetime, timedelta

# Libraries for WebScraping
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as BraveService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType, os_name, OSType

import pandas as pd # Library for handling data
from tqdm import tqdm   # Library for progressbar animation

# ------------------------------------------------------------------------------

# Setup logger
logger = logging.getLogger("logger")
logger.setLevel(logging.INFO)
handler = logging.FileHandler("logs.log")
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

# ------------------------------------------------------------------------------

# setup current working dir as global variable 
cwd = os.getcwd()

# ------------------------------------------------------------------------------
# Functions

def load_medium_lists(file_name: str) -> list:
    """Read library into dataframe. 
    If library file doesn't exists, create on.

    Args:
        file_name (str): Filename of library.

    Returns:
        list: Return dataframe as a list.
    """
    
    try:
        lst = pd.read_csv(file_name)
    except:
        lst = pd.DataFrame(columns=["List_Name", "Link"]).to_csv(file_name, index=False)
        print(f"Medium List Scraper - Please edit '{file_name}' and add a list with 'NAME, LINK'")
        exit()
        
    return lst.values.tolist()

def scroll_website(link: str) -> str:
    """Scroll through a link. 
    Use selenium as a webscraper to open a headerless browser (Brave Browser) 
    and scroll through it. It use the ChromeDriverManager to use always to newest
    Chrome driver.

    Args:
        link (str): Use Medium list link to scroll through this page.

    Returns:
        str: Returns pager_source for later use of BeautifulSoup
    """
    
    # binary location of brave browser driver
    binary_location = { 
     OSType.LINUX: "/usr/bin/brave-browser", 
     OSType.MAC: "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser", 
     OSType.WIN: f"{os.getenv('LOCAL APPDATA')}\\BraveSoftware\\Brave-Browser\\Application\\brave.exe", 
    }[os_name()] 

    # set binary location and headless (non visible browser) as Chrome options
    option = Options()
    option.binary_location = binary_location
    option.add_argument("--headless")
    
    # check for a new chrome / brave driver 
    driver_path = ChromeDriverManager(chrome_type=ChromeType.BRAVE).install()
    
    # Create driver object
    driver = webdriver.Chrome(service=BraveService(driver_path), options=option)
    driver.get(link)
    time.sleep(3)
    
    # scroll through page
    while True:
        previous_height = driver.execute_script("return document.body.scrollHeight")
        
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        new_height = driver.execute_script("return document.body.scrollHeight")
        
        if new_height == previous_height:
            break
    
    page_source = driver.page_source
    driver.quit()

    return page_source


def determine_date(p_in_article: list) -> str:
    """Determine the date of a list of HTML p-Elements and unify it.
     
    Because Medium use three different types of displaying date [ "Month, Day", "Month, Day, Year", "X days ago" ]
    there should be a flexible approach to scan the first p-Elements to determine the correct date. 

    Args:
        p_in_article (list): List of HTML p-Elements.

    Returns:
        str: Returns date as a unified datetime formatted string.
    """
    
    for p in p_in_article:
        
        p_text = p.text[1:] # for getting rid of "·"
        new_date = ""
        
        try: # Check for "Jan, 1" format
            result1 = bool(datetime.strptime(p_text, "%b %d"))
        except ValueError:
            result1 = False
            
        try: # Check for "Jan 1, 2022" format
            result2 = bool(datetime.strptime(p_text, "%b %d, %Y"))
        except ValueError:
            result2 = False
            
        # Unify date format
        if result1 == True:
            new_date = p_text + ", " + str(datetime.now().date().year)
            new_date = datetime.strptime(new_date, "%b %d, %Y").date()  # Change 'Mar 21, 2022' format to ISO format
            break
        if result2 == True:
            new_date = datetime.strptime(p_text, "%b %d, %Y").date() 
            break
        if p_text.find("days ago") != -1: # check if p have "days ago" in string and calculate correct date
            new_date = datetime.now().date() - timedelta(days=int(p_text.split(" ")[0]))
            break
        
    return new_date

def scrape_list(lst_name: str, link: str) -> list:
    """Scrape data from list item.
    Call out scroll_website to get page_source of scrolled list.
    Scrape data for each article object. 
    Append data to articles list.

    Args:
        lst_name (str): List name, which is located in 'medium_lists.csv'.
        link (str): link of according list, also located in 'medium_lists.csv'

    Returns:
        list: Returns data in list type.
    """
    
    print("")
    print(f"Medium List Scraper - {lst_name} - Scrape website ...")
    
    # Scroll and get page source / response
    response = scroll_website(link)
    soup = BeautifulSoup(response, "html.parser")

    articles = []
    title = ""
    author = ""
    date = ""
    link = ""
    date_added = ""

    for article_object in soup.find_all("article"):
        try:
            title = article_object.find("h2").text
        except:
            pass
        try:
            author = article_object.find("p").text
        except: 
            pass
        try:
            date = determine_date(article_object.find_all("p"))
        except:
            pass
        try:
            link = "https://medium.com" +  article_object.find_all("a", href=True)[3]["href"]    
        except:
            pass

        articles.append(
            [
                title,
                author,
                date,
                lst_name,
                link,
                date_added
            ]
        )
        
    return articles

def safe_filename(filename: str) -> str:
    """Convert filename to a safe PDF filename. 

    Args:
        filename (str): Title of article

    Returns:
        str: Returns safe string, without weird symbols. Which can be problematic for saving as a PDF file. 
    """
    
    keep_characters = (' ','.','_', "-")
    return "".join(c for c in filename if c.isalnum() or c in keep_characters).rstrip()

def download_articles(lst_name: str, df: pd.DataFrame):
    """Download articles 
    Create download folders. 
    Get through each element of 'download' dataframe.
    Transform medium link to scribe.rip link, to get more beautiful formatted PDFs.
    Use "percollate" a CLI tool for downloading HTML to beautiful PDFs and safe some Metadata in file.

    Args:
        lst_name (str): _description_
        df (pd.DataFrame): _description_
    """
    
    print(f"Medium List Scraper - {lst_name} - Download articles ...")
    
    try: # create downloads folder
        target_dir = cwd + f"/downloads/{lst_name}"
        if os.path.exists(target_dir) == False:
            os.mkdir(target_dir)
        else:
            pass
        os.chdir(target_dir)    # Change current working dir to download folder
    except Exception as e:
        logging.warning("Error in creating download folder" + str(e))
        
    try: # download articles
        for index, row in (pbar := tqdm(df.iterrows(), total=df.shape[0], unit="Article")): # walrus operator
            pbar.set_postfix_str(f"Processing {str(index)}. {row['Title']}")
            
            # transform link to scribe.rip for better a better frontmatter and styled PDFs
            scribe_link = str(row["Link"]).replace("medium.com", "scribe.rip")
            
            # download website to pdf
            file_name = f"{row['Date']}-{str(row['Author']).replace(' ', '_')}-{str(row['Title']).replace(' ', '_')}.pdf"
            file_name = safe_filename(file_name)
            output =  os.popen(
                    f"percollate pdf '{scribe_link}' --title='{row['Title']}' --author='{row['Author']}' --no-toc --output='{file_name}'"
                ).read()
            logger.info(output)
    except Exception as e:
        logging.warning("Error in downloading articles" + str(e))
    
    os.chdir(cwd)   # set initial current working dir to program folder

def main():
    """Handler for all functions.
    
    Load medium list with "load_medium_lists" function.
    For each list in lists scrape data. 
    Determine differences between library and scraped data. 
    Download differences.
    Append differences to library. 
    """

    lists = load_medium_lists("medium_lists.csv")  # Get lists of medium 

    print("Medium List Scraper: Scraping following lists: " + ", ".join([list_name[0] for list_name in lists]) + " ...")
    
    for lst in lists:
        lst_name = lst[0]
        link = lst[1]
        
        # Scrape Website
        scraped_list = []
        scraped_list = scrape_list(lst_name, link)
    
        # Create dataframe
        columns = ["Title", "Author", "Date", "List_Name", "Link", "Date_Added"]
        df_scraped_articles = pd.DataFrame(scraped_list, columns=columns)

        try: # to read library or create new one 
            df_library = pd.read_csv("library.csv")
        except:
            df_library = pd.DataFrame(columns=columns)

        # Determine differences and create 'to-download' dataframe
        df_diff = df_library.merge(df_scraped_articles, indicator=True, on="Title", how="right")
        df_download = df_diff[df_diff['_merge'] == 'right_only'].drop(columns=["Author_x", "Date_x", "List_Name_x", "Link_x", "Date_Added_x", "_merge"])
        df_download.columns = columns

        if not df_download.empty:
            # Download articles
            download_articles(lst_name, df_download.reset_index())
                
            # Add to library
            try: 
                print("Add following articles into library: \n")
                pd.options.display.max_colwidth = 100
                print(df_download["Title"])
                
                df_download["Date_Added"] = datetime.now()
                df_new_library = pd.concat([df_library, df_download], ignore_index=True)
                df_new_library.to_csv("library.csv", index=False)
            except Exception as e:
                logging.error("Error occurred in adding df to library: " + str(e))
        else:
            print(f"Medium List Scraper - {lst_name} - You're up to date!")

# ------------------------------------------------------------------------------
# Call out Main function

if __name__ == "__main__":
    main()