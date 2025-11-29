# Sada automatizovaných testů (pytest) na demo e-shop webu 'https://automationexercise.com/'
# testy volají fixtures 'page', 'browser_context', 'accept_gdpr' definované v souboru conftest.py;
# testy následující všechny požadované kroky uvedené v test cases pro daný web (https://automationexercise.com/test_cases)

from playwright.sync_api import Page, expect

# 13_TEST CASE: Verify Product quantity in Cart
# TEST PŘIDÁNÍ 4 KUSŮ JAKÉHOKOLIV PRODUKTU DO NÁKUPNÍHO KOŠÍKU PŘÍMO Z DOMOVSKÉ STRÁNKY SE ZÁVĚREČNOU KONTROLOU SPRÁVNÉHO MNOŽSTVÍ V KOŠÍKU
### Test neobsahuje přechod na podstránku s produkty, testuje se vkládání produktů přímo z domovské stránky.
def test_product_qty(page: Page):
    # 1. Launch browser; 
    # 2. Navigate to home url;
    # 3. Verify that home page is visible successfully
    assert page.url == "https://automationexercise.com/"             # ověření, že fixture 'page' otevřela správnou url
    

    # 4. Click 'View Product' for any product on home page
    view_product5_link = page.locator(".nav.nav-pills.nav-justified > li > a").nth(4)    # lokalizátor pro link 'View Product' u 5. zobrazeného produktu
    view_product5_link.click()                                                           # kliknutí na link


    # 5. Verify product detail is opened
    ### a) technické ověření přesměrování (kontrola URL)
    expect(page).to_have_url("https://automationexercise.com/product_details/5")         # vyčkání na přesměrování na stránku s detaily o 5. produktu
    
    ### b) uživatelské ověření
    ### ověření na základě bloku s detaily o produktu (název, kategorie, cena, dostupnost, stav, značka), tento blok není na home page, jen na stránce 'product_details'
    product_info_block = page.locator("div.product-information") # lokátor pro blok s detaily pro každý produkt
    expect(product_info_block).to_be_visible()


    # 6. Increase quantity to 4
    qty = page.locator("input#quantity")                # lokalizátor pro pole s množstvím
    qty.fill("4")                                       # zvýšení z default hodnoty "1" na "4" (string, ne integer)


    # 7. Click 'Add to cart' button
    add_to_cart_btn = page.get_by_role("button", name=" Add to cart")
    add_to_cart_btn.click()                                            # kliknutí na tlačítko 'Add to cart' (tzn. přidání do košíku)


    # 8. Click 'View Cart' button
    view_cart_link = page.get_by_role("link", name="View Cart")        # lokalizátor pro link 'View Cart' u zobrazeného okna
    view_cart_link.click()


    # 9. Verify that product is displayed in cart page with exact quantity
    ### a) Technické ověření přesměrování (kontrola URL) na stránku s nákupní košíkem
    expect(page).to_have_url("https://automationexercise.com/view_cart")
    
    ### b) Uživatelské ověření přesměnrování (kontrola nadpisu podstránky)
    ### ověření na základě bloku s detaily o produktu (název, kategorie, cena, dostupnost, stav, značka), tento blok není na home page, jen na stránce 'product_details'
    shopping_cart_heading = page.get_by_text("Shopping Cart")       # lokátor pro nadpis 'Shopping Cart' v záhlaví podstránky
    expect(shopping_cart_heading).to_be_visible()

    ### c) Kontrola množství na základě řádkového lokátoru pro daný produkt
    ### POZOR: NUTNÁ SPECIFIKACE ŘÁDKU S PRODUKETEM, JINÉ TESTY V HROMADNÉM SPUŠTĚTNÍ VKLÁDAJÍ TAKÉ DO KOŠÍKU VE STEJNOU DOBU A NELZE KONTROLOVAT JEN OBECNÉ MNOŽSTVÍ KUSŮ V KOŠÍKU 
    cart_product_5 = page.locator("tr#product-5")                   # lokátor pro řádek 5. produktu v nákupním košíku (řádkový lokátor)             
    cart_qty = cart_product_5.locator("td.cart_quantity button")    # lokátor pro množství (tlačítko v buňce cart_quantity) u 5. produktu
    expect(cart_qty).to_have_text("4")                              # ověření množství podle textu tlačítka, nikoli podle value (nejedná se o input element)


