import time
import json
import pandas as pd
import pickle
import Salary
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys

### Glassdoor Account Credentials ###
username = "global.bmc@gmail.com" # your email here
password = "Human@123$" # your password here

def obj_dict(obj):
    return obj.__dict__
#enddef

def json_export(data, cityName):
    #jsonFile = open("Data/" + cityName + ".json", "w")
    jsonFile = open("NewDelhi.json", "w")
    jsonFile.write(json.dumps(data, indent=4, separators=(',', ': '), default=obj_dict))
    jsonFile.close()
    #import pandas as pd
    df = pd.read_json(r'C:\Users\user\Desktop\scrapping\NewDelhi.json')
    export_csv = df.to_csv(r'C:\Users\user\Desktop\scrapping\NewDelhi.csv', index=None, header=True)

#enddef


def init_driver():
    driver = webdriver.Chrome(executable_path="C:\\Users\\user\\Desktop\\scrapping\\driver\\chromedriver.exe")
    driver.wait = WebDriverWait(driver, 10)
    return driver
#enddef


def login(driver, username, password):
    driver.get("http://www.glassdoor.com/profile/login_input.htm")
    try:
        user_field = driver.wait.until(EC.presence_of_element_located((By.NAME, "username")))
        pw_field = driver.wait.until(EC.presence_of_element_located((By.NAME,"password")))
        login_button = driver.find_element_by_name("submit")
        user_field.send_keys(username)
        user_field.send_keys(Keys.TAB)
        time.sleep(1)
        pw_field.send_keys(password)
        time.sleep(1)
        login_button.click()
    except TimeoutException:
        print("TimeoutException! Username/password field or login button not found on glassdoor.com")
#enddef


def search(driver, city, title):
    driver.get("https://www.glassdoor.co.in/Salaries/index.htm")
    try:
        #search_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        #    (By.CLASS_NAME, "showHH")))
        time.sleep(10)
        title_field = driver.find_element_by_id("KeywordSearch")
        city_field = driver.find_element_by_id("LocationSearch")
        title_field.send_keys(title)
        title_field.send_keys(Keys.TAB)
        time.sleep(1)
        city_field.send_keys(city)
        city_field.send_keys(Keys.RETURN)
        time.sleep(1)
        #search_button = driver.find_element_by_id("HeroSearchButton")
        #search_button.click()

    except TimeoutException:
        print("TimeoutException! city/title field or search button not found on glassdoor.com")
#enddef

def parse_salaries_HTML(salaries, data, city):
    for salary in salaries:
        jobTitle = "-"
        company = "-"
        meanPay = "-"
        jobTitle = salary.find_all('p')[0].getText().strip()
        company = salary.find_all('p')[1].getText().strip()
        #Companyame: // div[ @ data - test = "salary-row"] // div[ @ data - test = "job-info"] // p[2]
        #Title: // div[ @ data - test = "salary-row"] // div[ @ data - test = "job-info"] // p[1]
        #Salary: // div[ @ data - test = "salary-row"] // div[2] / strong
        try:
            meanPay = salary.find_all('p')[2].getText().strip()
            meanPay = meanPay.encode('ascii', 'ignore').strip()

        except:
            meanPay = 'xxx'
        r = Salary.Salary(jobTitle, company, meanPay, city)
        data.append(r)
    #endfor
    return data
#enddef

def get_data(driver, URL, city, data, refresh, startPage=1):
    if URL[-5:-4] == '9':
        return data
    print "\nPage " + str(startPage)
    if (refresh):
        driver.get(URL)
        print "Getting " + URL
        time.sleep(2)
    try:
        #next_btn = driver.find_element_by_class_name("next")
        next_btn = driver.find_element_by_class_name("pagination__PaginationStyle__next")
        next_link = next_btn.find_element_by_css_selector("a").get_attribute('href')
    except:
        next_btn = False
        next_link = False
    #endif
    time.sleep(2)
    HTML = driver.page_source
    soup = BeautifulSoup(HTML, "html.parser")
    try:
        salaries = soup.find("div", {"id": ["SalariesByCompany"]}).find_all("div", {"data-test": ["salary-row"]})
    except:
        salaries = False
    if (salaries):
        data = parse_salaries_HTML(salaries, data, city)
        print "Page " + str(startPage) + " scraped."
        if (next_link):
            get_data(driver, next_link, city, data, True, startPage + 1)
    else:
        print "No data available for", city
    #endif
    return data
#enddef


def json_to_csv():
    import pdb; pdb.set_trace();
    df = pd.read_json(r'C:\Users\user\Desktop\scrapping\NewDelhi.json')
    print df
    export_csv = df.to_csv(r'C:\Users\user\Desktop\scrapping\NewDelhi.csv', index=None, header=True)

def create_list_from_json1():
    import pdb; pdb.set_trace();
    with open(r'C:\Users\user\Desktop\scrapping\NewDelhi.json') as f:
        data = json.load(f)

    data_list = []
    # initializing list

    # printing original list
    print("The original list is : " + str(test_list))

    # Convert List of Dictionaries to List of Lists
    # Using loop + enumerate()
    res = []
    for idx, sub in enumerate(test_list, start=0):
        if idx == 0:
            res.append(list(sub.keys()))
            res.append(list(sub.values()))
        else:
            res.append(list(sub.values()))

        # printing result
    print("The converted list : " + str(res))

def create_list_from_json():
    import pdb; pdb.set_trace();
    with open(r'C:\Users\user\Desktop\scrapping\NewDelhi.json') as f:
        data = json.load(f)

    data_list = []  # create an empty list

    # append the items to the list in the same order.
    data_list.append(data['meanPay'])
    data_list.append(data['jobTitle'])
    data_list.append(data['company'])
    data_list.append(['city'])

    # In few json files, the race was not there so using KeyError exception to add '' at the place
    try:
        data_list.append(data['meta']['unstructured']['race'])
    except KeyError:
        data_list.append("")  # will add an empty string in case race is not there.
    data_list.append(data['name'])

    return data_list

def create_list_from_json_new():
    import pdb; pdb.set_trace();
    with open(r'C:\Users\user\Desktop\scrapping\NewDelhi_final.json') as f:
        data = json.load(f)

    pd.DataFrame.f
    pd.DataFrame.from_dict(data, orient='index',columns=['meanPay', 'jobTitle', 'company', 'city'], dtype=float)

    dfItem = pd.DataFrame.from_records(data)
    dfItem = pd.DataFrame.from_records(data, columns=['meanPay', 'jobTitle', 'company', 'city'])
    export_csv = dfItem.to_csv(r'C:\\Users\\user\\Desktop\\scrapping\\NewDelhi.csv', index=None, header=True)

    df1 = pd.DataFrame(data, columns=['meanPay', 'jobTitle', 'company', 'city'], dtype=float)
    pd.DataFrame(data,index=False,columns=['meanPay', 'jobTitle', 'company', 'city'], dtype=float)




if __name__ == "__main__":
    create_list_from_json_new()
    exit()
    create_list_from_json()
    exit()
    json_to_csv()
    exit()
    driver = init_driver()
    time.sleep(3)
    print "Logging into Glassdoor account ..."
    login(driver, username, password)
    time.sleep(10)
    # search(driver, city, title)
    print "\nStarting data scraping ..."
    city_list = open("cities.txt").read().splitlines()
    data_out = []
    for city in city_list:
        search(driver, city, 'Project Manager')
        #search(driver, city, 'Data Scientist')
        appendable = get_data(driver, driver.current_url, city, [], False, 1)
        print "\nExporting data to " + city + ".json"
        if appendable:
            data_out.append(appendable)
            json_export(appendable, city)
    if data_out:
        json_export(data_out, 'allcities')
    driver.quit()
#endif