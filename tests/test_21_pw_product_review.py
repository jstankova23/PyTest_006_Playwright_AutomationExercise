# Sada automatizovaných testů (pytest) na demo e-shop webu 'https://automationexercise.com/'
# testy volají fixtures definované v souboru conftest.py;
# testy následující všechny požadované kroky uvedené v test cases pro daný web (https://automationexercise.com/test_cases)

from playwright.sync_api import Page, expect

# 21_TEST CASE: Add review on product
# TEST ZADÁNÍ RECENZE K PRODUKTU
def test_product_review(page: Page):
    # 1. Launch browser; 
    # 2. Navigate to home url;
    assert page.url == "https://automationexercise.com/"             # ověření, že fixture 'page' otevřela správnou url
    

    # 3. Click on 'Products' button
    products_link = page.get_by_role("link", name=" Products")     # vyhledání linku pro 'Products' stránku
    products_link.click()                                           # kliknutí na link 'Products'
    

    # 4. Verify user is navigated to ALL PRODUCTS page successfully (new page)
    ### ověření, že se zobrazí na stránce nadpis 'ALL PRODUCTS'
    all_products_heading = page.get_by_role("heading", name="All Products")   # lokátor pro nadpis 'ALL PRODUCTS' na nové stránce
    expect(all_products_heading).to_be_visible(timeout=2000)       # ověření přesměrování na stránku s daným nadpisem a zpomalení


    # 5. Click on 'View Product' of first product
    view_product_1 = page.locator("a[href='/product_details/1']")  # lokalizátor pro link 'View Product' u 1. zobrazeného produktu
    view_product_1.click()                                         # kliknutí na link
    

    # 6. Verify 'Write Your Review' is visible
    write_your_review = page.get_by_role("link", name="Write Your Review") # lokátor na tlačítko/link 'WRITE YOUR REVIEW)' na detailu produktu
    write_your_review.click()


    # 7. Enter name, email and review
    ### Lokátory polí
    name_ipnut = page.get_by_role("textbox", name="Your Name")                  # pole 'Your Name'
    email_input = page.get_by_role("textbox", name="Email Address", exact=True) # pole 'Email Address'
    review_input = page.get_by_role("textbox", name="Add Review Here!")         # pole 'Add Review Here!'

    ### Proměnné s hodnotami
    name = "Test_21 User Reviewer"
    email = "test_21@test.com"          # pevný email, neprobíhá žádná validace
    review = "TEST REVIEW ENTRY"

    ### Vyplnění polí hodnotami
    name_ipnut.fill(name)
    email_input.fill(email)
    review_input.fill(review)


    # 8. Click 'Submit' button
    submit_btn = page.get_by_role("button", name="Submit")
    submit_btn.click()


    # 9. Verify success message 'Thank you for your review.'            
    success_review_msg = page.locator("#review-section .alert-success") # CSS lokátor na dočasnou hlášku, nutné ID, třída 'alert-success' by nestačila
    expect(success_review_msg).to_be_visible(timeout=1000) # vyčkání na zobrazení dočasné hlášky
    ###	Po kliknutí na tlačítko 'Submit' se zobrazí jen krátce hláška s poděkováním za review.
    ###	Pokud se nedaří získat selektor z DevTools během krátkého zobrazení hlášky, pak je nutné těsně před vyvoláním hlášky 
    ### (tzn. před kliknutím na tlačítko 'Submit') provést v DevTools zastavení běhu na JavaScriptu na události typu 'kliknutí':
    ### - DevTools - záložka Sources - Event Listener Breakpoints/ Mouse / Click
    ### - kliknout tlačítko 'Submit' (potvrdit odeslání review na produkt)
    ### - šipkou na debugovací liště postupně krokovat až do momentu zobrazení dané hlášky
    ### - kliknout na ikonku pro získání selektoru a označit danou hlášku
    ### - v záložce Elements dle označení pozice elementu v DOM sestavit si ručně CSS lokátor unikátní pro danou stránku
    ### - třída 'alert-success' není na stránce unikátní, tuto třídu využívá i hláška po úspěšně odeslané žádosti o odběr novinek (TC11)

