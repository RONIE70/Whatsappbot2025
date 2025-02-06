
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


driver_path = "./resource/driver/chromedriver.exe"  # Or path to your chromedriver
service = Service(driver_path)
driver = webdriver.Chrome(service=service)

#service = Service(ChromeDriverManager().install())
#driver = webdriver.Chrome(service=service)

driver.get("https://web.whatsapp.com/")

session_id = driver.session_id
executor_url = driver.command_executor._url

print("Session ID 1: " + session_id)
print("Executor URL: " + executor_url)

with open("./resource/driver/whatsapp_session.txt", "w") as text_file:
    text_file.write(f"{executor_url}\n")
    text_file.write(session_id)

def create_driver_session(session_id, executor_url):
    from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver

    org_command_execute = RemoteWebDriver.execute

    def new_command_execute(self, command, params=None):
        if command == "newSession":
            return {'success': 0, 'value': None, 'sessionId': session_id}
        else:
            return org_command_execute(self, command, params)

    RemoteWebDriver.execute = new_command_execute

    new_driver = webdriver.Remote(command_executor=executor_url, desired_capabilities={})
    new_driver.session_id = session_id

    RemoteWebDriver.execute = org_command_execute

    return new_driver


driver2 = create_driver_session(session_id, executor_url)
print("Driver 2 URL: " + driver2.current_url)