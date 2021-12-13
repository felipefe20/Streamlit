import glob
import os

import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

options = Options()
#options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--disable-features=NetworkService")
options.add_argument("--window-size=1920x1080")
options.add_argument("--disable-features=VizDisplayCompositor")


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
    # executable_path = get_chromedriver_path()
    executable_path = "notset"
    # st.info(f'Chromedriver Path: {str(executable_path)}')
    st.balloons()
    if st.button('Start Selenium run'):
        st.info('Selenium is running, please wait...')
        #result = run_selenium()
        Login()
        #st.info(f'Result -> {result}')
        st.info('Successful finished. Selenium log file is shown below...')
        show_selenium_log()
