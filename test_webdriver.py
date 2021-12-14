import glob
import os
import pandas as pd
import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta
import time


from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType



options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--disable-features=NetworkService")
options.add_argument("--window-size=1920x1080")
options.add_argument("--disable-features=VizDisplayCompositor")

#initial settings
def setting_selenium_options(download_file_path:str)->webdriver.ChromeOptions:
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-extensions")
    options.add_argument("--headless")
    options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")
    options.add_argument("--start-maximized")
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-running-insecure-content')
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
    options.add_argument(f'user-agent={user_agent}')
    prefs = {
        "download.default_directory":download_file_path
        #"download.prompt_for_download": False,
        #"download.directory_upgrade": True
        }

    options.add_experimental_option('prefs', prefs)
    return options

def delete_selenium_log():
    if os.path.exists('selenium.log'):
        os.remove('selenium.log')


def show_selenium_log():
    if os.path.exists('selenium.log'):
        with open('selenium.log') as f:
            content = f.read()
            st.code(content)


def get_chromedriver_path():
    results = glob.glob('/**/chromedriver', recursive=True)  # workaround on streamlit sharing
    which = results[0]
    return which


#def run_selenium():
#    name = str()
 #   with webdriver.Chrome(options=options, service_log_path='selenium.log') as driver:
  #      url = "https://www.unibet.fr/sport/football/europa-league/europa-league-matchs"
  #      driver.get(url)
   #     #xpath = '//*[@class="component__header"]'
        # Wait for the element to be rendered:
   #     element = WebDriverWait(driver, 10).until(lambda x: x.find_elements_by_xpath(xpath))
        # element = driver.find_elements_by_xpath(xpath)
    #    name = element[0].get_property('attributes')[0]['name']
    #    st.write(name)
    #return name
    
#LogIn
def Login():
    with webdriver.Chrome(options=options, service_log_path='selenium.log') as driver:
        driver.get('https://home-c13.incontact.com/inContact/Manage/Reports/ContactHistory.aspx')
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="ctl00_BaseContent_msl_txtUsername"]'))).send_keys("osfernandez@algvacations.com")
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="ctl00_BaseContent_btnNext"]'))).click()
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="ctl00_BaseContent_mslp_tbxPassword"]'))).send_keys("Avril131215+")
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="ctl00_BaseContent_mslp_btnLogin"]'))).click()

    st.write("Login succesful")
   
#Date to fetch
def set_date_to_fetch(date:str)->str:
    """
    Funcion para setear la fecha que haremos fetch, si el usuario pone de parametro date = ayer, se hara fetch de el dia anterior, de lo contrario
    puede pasar una fecha cualquiera por parametro y sobre esa fecha se hara el fetch

    Args:
        date (str): ayer o la fecha que se desee fetchear la info

    Returns:
        str: la fecha en formato string %m/%d/%Y 
    """

    if date == 'ayer':
        today_date = datetime.now().strftime('%A').lower()
        if today_date == 'monday':
            yesterday_date = datetime.now() - timedelta(3)    
        else:
            yesterday_date = datetime.now() - timedelta(1)
    else:
        yesterday_date = pd.to_datetime(date)
    
    yesterday_date_str = yesterday_date.strftime('%m/%d/%Y')

    return yesterday_date_str    

    
def download_metadata_day(day):
    
    with webdriver.Chrome(options=options, service_log_path='selenium.log') as driver:
        if day=="yesterday":
            yesterday_date=(pd.to_datetime("today")-timedelta(1)).strftime("%m/%d/%Y")
            date=yesterday_date
        else:
            date=day

        Hours=[["12:00:00 AM","09:59:59 AM"],["10:00:00 AM","12:59:59 PM"],["13:00:00 PM","15:59:59 PM"],["16:00:00 PM","23:59:59 PM"]]

        #Show options click
        #WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME,'//*[@id="ctl00_ctl00_BaseContent_ReportOptionsContent_CHOptionsHeaderPanelID"]'))).click()
        #time.sleep(30)
        #driver.find_element_by_class_name("CHOptionsHeaderPanelButton").click()
        
        
        #Teleperformance Bogota
        #WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="ctl00_ctl00_BaseContent_ReportOptionsContent_ddTeams"]'))).send_keys("Teleperformance Bogota")
        #time.sleep(2)
        
        #driver.find_element_by_xpath('//*[@id="ctl00_ctl00_BaseContent_ReportOptionsContent_ddTeams"]').send_keys("Teleperformance Bogota")
        
        #MediaType Phone
        time.sleep(2)
        #WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="ctl00_ctl00_BaseContent_ReportOptionsContent_ddMediaType"]'))).send_keys("Phone")
        #driver.find_elements_by_xpath('//*[@id="ctl00_ctl00_BaseContent_ReportOptionsContent_ddMediaType"]').send_keys("Phone")
        #Iterate hours to download for every day
        
        for hour in Hours:
            #Date1
            #WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="ctl00_ctl00_BaseContent_ReportOptionsContent_txtStartDate"]'))).clear()          
            #WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="ctl00_ctl00_BaseContent_ReportOptionsContent_txtStartDate"]'))).send_keys(date)
            driver.find_element_by_xpath('//*[@id="ctl00_ctl00_BaseContent_ReportOptionsContent_txtStartDate"]').clear() 
            driver.find_element_by_xpath('//*[@id="ctl00_ctl00_BaseContent_ReportOptionsContent_txtStartDate"]').send_keys(date)
            #Date2
            #WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="ctl00_ctl00_BaseContent_ReportOptionsContent_txtEndDate"]'))).clear()
            #WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="ctl00_ctl00_BaseContent_ReportOptionsContent_txtEndDate"]'))).send_keys(date)
            
            driver.find_element_by_xpath('//*[@id="ctl00_ctl00_BaseContent_ReportOptionsContent_txtEndDate"]').clear() 
            driver.find_element_by_xpath('//*[@id="ctl00_ctl00_BaseContent_ReportOptionsContent_txtEndDate"]').send_keys(date)
            
            #Hour1
            #WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="ctl00_ctl00_BaseContent_ReportOptionsContent_txtStartTime"]'))).clear()
            #WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="ctl00_ctl00_BaseContent_ReportOptionsContent_txtStartTime"]'))).send_keys(hour[0])
            driver.find_element_by_xpath('//*[@id="ctl00_ctl00_BaseContent_ReportOptionsContent_txtStartTime"]').clear() 
            driver.find_element_by_xpath('//*[@id="ctl00_ctl00_BaseContent_ReportOptionsContent_txtStartTime"]').send_keys(hour[0])
            
            #Hour2
            #WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="ctl00_ctl00_BaseContent_ReportOptionsContent_txtEndTime"]'))).clear()
            #WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="ctl00_ctl00_BaseContent_ReportOptionsContent_txtEndTime"]'))).send_keys(hour[1])
            driver.find_element_by_xpath('//*[@id="ctl00_ctl00_BaseContent_ReportOptionsContent_txtStartTime"]').clear() 
            driver.find_element_by_xpath('//*[@id="ctl00_ctl00_BaseContent_ReportOptionsContent_txtStartTime"]').send_keys(hour[1])
            #Scroll top of page
            #driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)
            #Apply options
            #WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="btnApplyOptions_ShadowButtonSpan"]'))).click()
            #time.sleep(2)
            #driver.find_element_by_tag_name('body').send_keys(Keys.DOWN)
            #driver.find_element_by_tag_name('body').send_keys(Keys.DOWN)
            #time.sleep(10)

            #Download
            #WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="ctl00_ctl00_BaseContent_ReportMainContent_btnDownload"]'))).click()
            
        time.sleep(5)
        st.write("Succesful metadata day downloaded")
 
#Ejecución del script completo
def main(date,download_file_path,options):
    
    with webdriver.Chrome(options=options, service_log_path='selenium.log') as driver:
        yesterday_date_str = set_date_to_fetch(date=date) # PARAMETRO IMPORTANTE, PASAR 'AYER' si se desea hacer fetch del dia anterior, de lo contrario pasar fecha como string en formato MM-DD-YYYY
        yesterday_date_folder=yesterday_date_str.replace("/","-")
        try:
            os.mkdir(f'{download_file_path}\\{yesterday_date_folder}') # creo una carpeta cuyo nombre es el dia que corresponde a la descarga de la metadata
        except:
            pass
        
        
        #Login
        Login()
        #Metadata
        download_metadata_day(yesterday_date_str)
        time.sleep(5)


    
    
if __name__ == "__main__":
    delete_selenium_log()
    st.set_page_config(page_title="Selenium Test", page_icon='✅',
        initial_sidebar_state='collapsed')
    st.title('🔨 Selenium Test for Streamlit Sharing')
    st.markdown("""
        This app is only a very simple test for **Selenium** running on **Streamlit Sharing** runtime. <br>
        The suggestion for this demo app came from a post on the Streamlit Community Forum.  <br>
        <https://discuss.streamlit.io/t/issue-with-selenium-on-a-streamlit-app/11563>  <br>
        Unfortunately this app has deployment issues on Streamlit Sharing, sometimes deployment fails, sometimes not... 😞
        This is just a very very simple example and more a proof of concept.
        A link is called and waited for the existence of a specific class and read it. If there is no error message, the action was successful.
        Afterwards the log file of chromium is read and displayed.
        ---
        """, unsafe_allow_html=True)
    download_file_path = st.text_input('Folder download',"")
    download_file_path=download_file_path.replace("/","\\")
    st.write('Folder download', download_file_path)
    # executable_path = get_chromedriver_path()
    executable_path = "notset"
    # st.info(f'Chromedriver Path: {str(executable_path)}')
    st.balloons()
    if st.button('Start Selenium run'):
        st.info('Selenium is running, please wait...')
        #result = run_selenium()
        main("12/10/2021",download_file_path,options)
        #st.info(f'Result -> {result}')
        st.info('Successful finished. Selenium log file is shown below...')
        show_selenium_log()

        
        
 
