import multiprocessing
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

url = "https://reservation.frontdesksuite.ca/rcfs/nepeansportsplex/Home/Index?Culture=en&PageId=b0d362a1-ba36-42ae-b1e0-feefaf43fe4c&ShouldStartReserveTimeFlow=False&ButtonId=00000000-0000-0000-0000-000000000000"
sport = "Badminton"


BookInfo = {
    0: {
        "tel": "*",
        "email": "*",
        "text": "Hui",
        "ticketNo": 2
    },
}
PriorKnowledge = {
    0: {
        "dayText": "Friday March 31, 2023",
        "hourText": "7:45 PM"
    },
    1: {
        "dayText": "Friday March 31, 2023",
        "hourText": "9:00 PM"
    }
}
PriorKnowledgeIndex = 0


def makeReservation(dayText, hourText, tel, email, text, bookTicketNumber, processID):
    global sport, url, timeSlot
    isBooked = False
    # Get Driver
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    #
    while isBooked is False:
        print(
            f"Process {processID} will book {dayText}, {hourText} using contact info {tel}, {email}, {text} for {bookTicketNumber} ticket")
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
            # Final Confirmation
            driver.find_element(By.XPATH, "//button[@id='submit-btn']").click()
            isBooked = True
        except:
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
