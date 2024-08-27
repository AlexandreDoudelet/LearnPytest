import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from configfiles.conftest import browser
import time

@pytest.mark.usefixtures("browser")
class Testamazon():
    @pytest.mark.sanity
    @pytest.mark.parametrize("search_item",["selenium","playright","cypress","boat"])
    def test_amazon_search(self, search_item):


        # Open the Amazon homepage
        self.browser.get('https://www.amazon.com')
        #self.browser.refresh()

        # Verify the page title
        assert "Amazon.com. Spend less. Smile more." in self.browser.title

        # Find the search box
        search_box = self.browser.find_element(By.ID, 'twotabsearchtextbox')

        # Type a search query
        #search_box.send_keys(browser.request_param)
        search_box.send_keys(search_item)

    # Submit the search form
        search_box.send_keys(Keys.RETURN)

        # Verify that search results appear
        assert "No results found." not in self.browser.page_source

        # Optionally, check if a specific result appears in the results
        results = self.browser.find_elements(By.CSS_SELECTOR, '#search > div.s-desktop-width-max.s-desktop-content.s-opposite-dir.s-wide-grid-style.sg-row > div.sg-col-20-of-24.s-matching-dir.sg-col-16-of-20.sg-col.sg-col-8-of-12.sg-col-12-of-16 > div > span.rush-component.s-latency-cf-section > div.s-main-slot.s-result-list.s-search-results.sg-row > div:nth-child(6)')
        print (results)
        # assert any(search_item in result.text for result in results)

    @pytest.mark.xfail
    def test_calculation():
        assert 2+2 == 5 