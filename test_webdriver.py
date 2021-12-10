import glob
import os

import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait

options = Options()
options.add_argument("--headless")
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


def run_selenium():
    name = str()
    with webdriver.Chrome(options=options, service_log_path='selenium.log') as driver:
        url = "https://www.unibet.fr/sport/football/europa-league/europa-league-matchs"
        driver.get(url)
        xpath = '//*[@class="ui-mainview-block eventpath-wrapper"]'
        # Wait for the element to be rendered:
        element = WebDriverWait(driver, 10).until(lambda x: x.find_elements_by_xpath(xpath))
        # element = driver.find_elements_by_xpath(xpath)
        name = element[0].get_property('attributes')[0]['name']
        # print(name)
    return name

#LogIn
def Login():
    with webdriver.Chrome(options=options, service_log_path='selenium.log') as driver:
        driver.get('https://signin.vivint.com/app/vivintinc_genesyspurecloud_1/exk4bop5qmPYkzu632p7/sso/saml?SAMLRequest=PHNhbWxwOkF1dGhuUmVxdWVzdCB4bWxuczpzYW1scD0idXJuOm9hc2lzOm5hbWVzOnRjOlNBTUw6Mi4wOnByb3RvY29sIiB4bWxuczpzYW1sPSJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6YXNzZXJ0aW9uIiBJRD0iSEs1RWpqS1ZRWmhFaUVvR0RLQ2xEZ0s1TGkwWWdraWl0b3EzTTJOdHlmSSIgVmVyc2lvbj0iMi4wIiBQcm90b2NvbEJpbmRpbmc9InVybjpvYXNpczpuYW1lczp0YzpTQU1MOjIuMDpiaW5kaW5nczpIVFRQLVBPU1QiIEFzc2VydGlvbkNvbnN1bWVyU2VydmljZVVSTD0iaHR0cHM6Ly9sb2dpbi51c3cyLnB1cmUuY2xvdWQvc2FtbCIgSXNzdWVJbnN0YW50PSIyMDIxLTA4LTI3VDE3OjAyOjUyWiIgRGVzdGluYXRpb249Imh0dHBzOi8vc2lnbmluLnZpdmludC5jb20vYXBwL3ZpdmludGluY19nZW5lc3lzcHVyZWNsb3VkXzEvZXhrNGJvcDVxbVBZa3p1NjMycDcvc3NvL3NhbWwiPjxzYW1sOklzc3Vlcj5odHRwOi8vd3d3Lm9rdGEuY29tL2V4azRib3A1cW1QWWt6dTYzMnA3PC9zYW1sOklzc3Vlcj48c2FtbHA6TmFtZUlEUG9saWN5IEFsbG93Q3JlYXRlPSJ0cnVlIiBGb3JtYXQ9InVybjpvYXNpczpuYW1lczp0YzpTQU1MOjIuMDpuYW1laWQtZm9ybWF0OnRyYW5zaWVudCIvPjwvc2FtbHA6QXV0aG5SZXF1ZXN0Pg%3D%3D')
        WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'input[id="okta-signin-username"]'))).send_keys("oscar.fernandez")
        WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'input[id="okta-signin-submit"]'))).click()
        WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'input[name="password"]'))).send_keys("TPteamNLP2021")
        WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'.button.button-primary'))).click()


        time.sleep(10)

        driver.get("https://apps.usw2.pure.cloud/directory")

    return ("Login complete")

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
        result=Login()
        st.info(f'Result -> {result}')
        st.info('Successful finished. Selenium log file is shown below...')
        show_selenium_log()
