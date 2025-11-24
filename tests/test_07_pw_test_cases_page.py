# Sada automatizovaných testů (pytest) na demo e-shop webu 'https://automationexercise.com/'
# testy volají fixtures 'page', 'browser_context', 'accept_gdpr' definované v souboru conftest.py;
# testy následující všechny požadované kroky uvedené v test cases pro daný web (https://automationexercise.com/test_cases)

from playwright.sync_api import Page, expect

# 07_TEST CASE: Verify Test Cases Page
# OVĚŘENÍ PŘESMĚROVÁNÍ Z DOMOVSKÉ STRÁNKY 'https://automationexercise.com/' NA PODSTRÁNKU S TEST CASES 'https://automationexercise.com/' 
def test_cases_page(page: Page):
    # 1. Launch browser; 
    # 2. Navigate to home url;
    # 3. Verify that home page is visible successfully
    assert page.url == "https://automationexercise.com/"             # ověření, že fixture 'page' otevřela správnou url
    
    # 4. Click on 'Test Cases' button
    test_cases_link = page.get_by_role("link", name=" Test Cases")   # vyhledání linku pro 'Test Cases' stránku
    test_cases_link.click()                                           # kliknutí na link 'Test Cases'
    
    # 5. Verify user is navigated to test cases page successfully (new page)
    test_cases_heading = page.locator("b")                  # lokátor pro nadpis 'TEST CASES' na nové stránce
    expect(test_cases_heading).to_be_visible(timeout=2000)  # ověření přesměrování na stránku s daným nadpisem a zpomalení

    























