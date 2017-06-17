from selenium import webdriver
import time

def main():
    browser = webdriver.Chrome(executable_path="/driver/chromedriver")
    browser.get("http://localhost:8000")

    try:
        assert("Django" in browser.title)
    finally:
        browser.quit()


if __name__ == "__main__":
    main()
