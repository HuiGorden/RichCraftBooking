import multiprocessing
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

url = "https://reservation.frontdesksuite.ca/rcfs/richcraftkanata/Home/Index?Culture=en&PageId=b3b9b36f-8401-466d-b4c4-19eb5547b43a&ButtonId=00000000-0000-0000-0000-000000000000"

sport = "Badminton - doubles"

BookInfo = {
    0: {
        "tel": "*",
        "email": "*",
        "text": "*",
        "ticketNo": 1
    },
}
PriorKnowledge = {
    0: {
        "dayText": "Monday July 25, 2022",
        "hourText": "7:00 PM"
    },
    1: {
        "dayText": "Monday July 25, 2022",
        "hourText": "8:00 PM"
    }
}
PriorKnowledgeIndex = 0


def makeReservation(dayText, hourText, tel, email, text, bookTicketNumber, processID):
    global sport, url, timeSlot
    # Get Driver
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    #
    print(f"Process {processID} will book {dayText}, {hourText} using contact info {tel}, {email}, {text} for {bookTicketNumber} ticket")
    #
    while True:
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
            break
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
