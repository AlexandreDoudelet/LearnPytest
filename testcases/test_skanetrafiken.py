import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select  import Select
from configfiles.conftest import browser

@pytest.mark.usefixtures("browser")
class TestSkanetrafiken():
    #@pytest.mark.sanity
    def test_skanetrafiken_mainpage_search(self):
        self.browser.delete_all_cookies()
        self.browser.get("https://www.skanetrafiken.se")
        assert "Kollektivtrafik i Skåne - Res med oss " in self.browser.title
        Acceptcookie = self.browser.find_element(By.ID, 'CybotCookiebotDialogBodyButtonAccept')
        Acceptcookie.click()  

        # Find the search box
        search_box = self.browser.find_element(By.ID, 'fromDestinationAutocompleteCombobox')

        # Type a search query
        #search_box.send_keys(browser.request_param)
        search_box.send_keys("malmö")
        # Submit the search form
        search_box.send_keys(Keys.RETURN)

        # Verify that search results appear
        assert "No results found." not in self.browser.page_source

        # Optionally, check if a specific result appears in the results
        results = self.browser.find_elements(By.CSS_SELECTOR, '#search > div.s-desktop-width-max.s-desktop-content.s-opposite-dir.s-wide-grid-style.sg-row > div.sg-col-20-of-24.s-matching-dir.sg-col-16-of-20.sg-col.sg-col-8-of-12.sg-col-12-of-16 > div > span.rush-component.s-latency-cf-section > div.s-main-slot.s-result-list.s-search-results.sg-row > div:nth-child(6)')
        print (results)
        # assert any(search_item in result.text for result in results)
    @pytest.mark.parametrize("cityfrom, cityto",[("malmö","Helsingborg C"), ("Lund","Båstad")])
    def test_skanetrafiken_sokpage_search(self, cityfrom, cityto):
        self.browser.delete_all_cookies()
        self.browser.get("https://www.skanetrafiken.se")
        assert "Kollektivtrafik i Skåne - Res med oss " in self.browser.title
        Acceptcookie = self.browser.find_element(By.ID, 'CybotCookiebotDialogBodyButtonAccept')
        Acceptcookie.click()  
        Sok_resa_link = self.browser.find_element(By.CSS_SELECTOR, '* [class=st-main-menu__item]:nth-child(1)')
        Sok_resa_link.click()
        assert "Sök din kollektiva resa i Skåne-Skånetrafiken" in self.browser.title
        search_boxfrom = self.browser.find_element(By.ID, 'fromDestinationAutocompleteCombobox')   
        # Type a search query
        #search_box.send_keys(browser.request_param)
        search_boxfrom.send_keys(cityfrom)
        search_boxto = self.browser.find_element(By.ID, 'toDestinationAutocompleteCombobox')   
        # Type a search query
        #search_box.send_keys(browser.request_param)
        search_boxto.send_keys(cityto)
        search_boxto.send_keys(Keys.ENTER)
        time.sleep(4)
        if cityto == "Båstad":
            list_to = self.browser.find_elements(By.CSS_SELECTOR, "*[id='toDestinationAutocompleteListbox'] li") 
            print(len(list_to))
            for value in list_to:
                    if "Båstad station" in value.text:
                        value.click()
                        break
            #dd_destination = Select(list_to)   
            #dd_destination.select_by_visible_text(' Båstad station')    
            time.sleep(4)
        else:
            search_boxto.send_keys(Keys.ENTER)

        departureradio = self.browser.find_element(By.ID, 'departure')
        departureradio.click()
        departureradio.is_selected()

        # calendar = self.browser.find_element(By.XPATH, "//button[@class='duet-date__toggle']")
        # calendar.click()
        # self.browser.find_element(By.XPATH, "//*[contains(text(),'27 juli')]").click()
        list_date= self.browser.find_elements(By.XPATH, "//table[@class='duet-date__table']//tbody//td//button")
        print (f"{list_date}")
        print(len(list_date))
        for value in list_date:
            if "27" in value.txt:
                value.click()
                break
        time.sleep(2)

        hoursLabeldropdown = self.browser.find_element(By.CSS_SELECTOR, "*[aria-labelledby='hoursLabel']")
        #hoursLabeldropdown.scroll_to_element(hoursLabeldropdown)
        dd = Select(hoursLabeldropdown)
        dd.select_by_visible_text('11')

        time.sleep(2)

        # Submit the search form
        #search_boxto.send_keys(Keys.RETURN)
        self.browser.save_screenshot(".\\screenshots\\screenshot_" + cityfrom + "_" + cityto+ ".png")

        # Verify that search results appear
        assert "No results found." not in self.browser.page_source
 