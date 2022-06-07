from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import pytest
from selenium.webdriver.common.by import By
import logging


class Driver:
    def __init__(self, url):
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox");  # Bypass OS security model
        chrome_options.add_argument("--disable-dev-shm-usage");  # overcome limited resource problems
        chrome_options.add_argument("--headless");  # Bypass OS security model
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        self.driver.implicitly_wait(5)
        self.driver.get(url)

    def close(self):
        self.driver.close()


class Voting_Page:
    _VOTE_URL = "http://localhost:5555/"
    _CATS_BUTTON_ID = "a"
    _DOGS_BUTTON_ID = "b"

    def __init__(self):
        self.driver = Driver(url=self._VOTE_URL)
        assert "Cats vs Dogs!" in self.get_driver().title

    def get_driver(self):
        return self.driver.driver

    def get_title(self):
        return self.get_driver().title

    def cast_vote(self, vote="b"):
        if vote in ["b", "a"]:
            self.get_driver().find_element(By.ID, vote).click()
        else:
            logging.warning("Improper vote cast, no vote will be made...")

    def get_cats_button(self):
        return self.get_driver().find_element(By.ID, self._CATS_BUTTON_ID)

    def get_dogs_button(self):
        return self.get_driver().find_element(By.ID, self._DOGS_BUTTON_ID)


class Results_Page:
    _RESULT_URL = "http://localhost:9876/"
    _VOTES_XPATH = '//*[@id="result"]/span'
    _CATS_BG_COLOR_ID = 'background-stats-1'
    _DOGS_BG_COLOR_ID = 'background-stats-2'
    _RESULTS_CONTAINER_ID = 'choice'
    _CATS_CONTAINER_XPATH = '//*[@id="choice"]/div[1]'
    _DOGS_CONTAINER_XPATH = '//*[@id="choice"]/div[2]'


    def __init__(self):
        self.driver = Driver(url=self._RESULT_URL)
        assert "Cats vs Dogs -- Result" in self.get_driver().title

    def get_driver(self):
        return self.driver.driver

    def get_title(self):
        return self.get_driver().title

    def get_votes(self):
        votes_text = self.get_driver().find_element(By.XPATH, self._VOTES_XPATH).text
        votes = int(votes_text[:-6])
        return votes

    def get_cats_bg_color(self):
        return self.get_driver().find_element(By.ID, self._CATS_BG_COLOR_ID)

    def get_dogs_bg_color(self):
        return self.get_driver().find_element(By.ID, self._DOGS_BG_COLOR_ID)

    def get_results_container(self):
        return self.get_driver().find_element(By.ID, self._RESULTS_CONTAINER_ID)

    def get_cats_container(self):
        return self.get_driver().find_element(By.XPATH, self._CATS_CONTAINER_XPATH)

    def get_dogs_container(self):
        return self.get_driver().find_element(By.XPATH, self._DOGS_CONTAINER_XPATH)        


@pytest.fixture
def voting_page():
    voting_page = Voting_Page()
    yield voting_page
    voting_page.get_driver().close()


@pytest.fixture
def results_page():
    results_page = Results_Page()
    yield results_page
    results_page.get_driver().close()


def test_user_can_go_to_voting_page(voting_page):
    assert "Cats vs Dogs!", "Wrong voting page title" in voting_page.get_title()


def test_voting_page_elements_exist(voting_page):
    assert voting_page.get_cats_button(), "Element not found..."
    assert voting_page.get_dogs_button(), "Element not found..."


def test_user_can_go_to_results_page(results_page):
    assert "Cats vs Dogs -- Result", "Wrong results page title" in results_page.get_title()


def test_results_page_elements_exist(results_page):
    assert results_page.get_cats_bg_color(), "Element not found..."
    assert results_page.get_dogs_bg_color(), "Element not found..."
    assert results_page.get_results_container(), "Element not found..."
    assert results_page.get_cats_container(), "Element not found..."
    assert results_page.get_dogs_container(), "Element not found..."


@pytest.mark.parametrize("vote", [
    "b",
    "a"
])
def test_user_can_vote(vote, results_page, voting_page):
    start_votes = results_page.get_votes()
    voting_page.cast_vote(vote=vote)
    results_page.get_driver().refresh()
    end_votes = results_page.get_votes()
    assert end_votes > start_votes, "Vote count should have inceased..."
