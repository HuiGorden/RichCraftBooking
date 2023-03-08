import multiprocessing
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from getCodeFromGmailSnippet import getCodeFromGmail

url = "https://reservation.frontdesksuite.ca/rcfs/richcraftkanata/Home/Index?Culture=en&PageId=b3b9b36f-8401-466d-b4c4-19eb5547b43a&ShouldStartReserveTimeFlow=False&ButtonId=00000000-0000-0000-0000-000000000000"
sport = "Badminton doubles - adult"
# sport = "Lane swim"

BookInfo = {
    0: {
        "tel": "*",
        "email": "*",
        "text": "*",
        "ticketNo": 2
    },
}
PriorKnowledge = {
    0: {
        "dayText": "Thursday March 9, 2023",
        "hourText": "7:00 PM"
    },
    1: {
        "dayText": "Thursday March 9, 2023",
        "hourText": "8:00 PM"
    }
}



def makeReservation(dayText, hourText, tel, email, text, bookTicketNumber, processID):
    global sport, url, timeSlot
    isBooked = False
    # Get Driver
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    #
    while isBooked is False:
        print(
            f"Process {processID} will book {sport} {dayText}, {hourText} using contact info {tel}, {email}, {text} for {bookTicketNumber} ticket")
        driver.get(url)
        sportDiv = driver.find_element(By.XPATH, f"//div[text()='{sport}']")
        sportDiv.click()
        try:
            ReservationCountInput = driver.find_element(By.NAME, "ReservationCount")
            ReservationCountInput.clear()
            ReservationCountInput.send_keys(f"{bookTicketNumber}")
            driver.find_element(By.ID, "submit-btn").click()
            # expand
            driver.find_element(By.XPATH, f"//span[@class='header-text' and text()='{dayText}']").click()
            driver.find_element(By.XPATH, f"//div[contains(@class, 'one-queue')]//span[text()='{dayText}']/ancestor::div[contains(@class, 'one-queue')]//span[text()='{hourText}']/ancestor::a").click()

            driver.find_element(By.XPATH, "//input[@type='tel']").clear()
            driver.find_element(By.XPATH, "//input[@type='tel']").send_keys(tel)

            driver.find_element(By.XPATH, "//input[@type='email']").clear()
            driver.find_element(By.XPATH, "//input[@type='email']").send_keys(email)

            driver.find_element(By.XPATH, "//input[@type='text']").clear()
            driver.find_element(By.XPATH, "//input[@type='text']").send_keys(text)

            driver.find_element(By.XPATH, "//button[@id='submit-btn']").click()

            #
            code_list = []
            while isBooked is False:
                try:
                    element = driver.find_element(By.XPATH, "//h1[text()='Confirmation']")
                    print("Set isBooked to True")
                    isBooked = True
                except Exception as e:
                    if not code_list:
                        code_list = getCodeFromGmail()
                    if not code_list:
                        print("Gmail doesn't receive code yet...")
                        continue
                    else:
                        print(f"Gmail code is {code_list}")
                    code = code_list.pop(0)
                    driver.find_element(By.XPATH, "//input[@type='number']").send_keys(code)
                    driver.find_element(By.CLASS_NAME, "mdc-button").click()
                    print("Submit Gmail Code")
                    time.sleep(0.2)

        except Exception as e:
            print(f"Process {processID}: Retrying....")


if __name__ == "__main__":
    pool = multiprocessing.Pool(processes=len(PriorKnowledge))
    for index in range(len(PriorKnowledge)):
        dayText = PriorKnowledge[index]["dayText"]
        hourText = PriorKnowledge[index]["hourText"]
        tel = BookInfo[0]["tel"]
        email = BookInfo[0]["email"]
        text = BookInfo[0]["text"]
        ticketNo = BookInfo[0]["ticketNo"]
        pool.apply_async(makeReservation, args=(dayText, hourText, tel, email, text, ticketNo, index))
    pool.close()
    pool.join()
