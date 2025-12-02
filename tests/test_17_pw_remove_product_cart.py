# Sada automatizovaných testů (pytest) na demo e-shop webu 'https://automationexercise.com/'
# testy volají fixtures definované v souboru conftest.py;
# testy následující všechny požadované kroky uvedené v test cases pro daný web (https://automationexercise.com/test_cases)

from playwright.sync_api import Page, expect

# 17_TEST CASE: Remove Products From Cart
# TEST ODSTRANĚNÍ PRODUKTU Z NÁKUPNÍHO KOŠÍKU (VÝMAZ JEDNOHO ŘÁDKU ZE DVOU), BEZ PŘHLÁŠENÍ UŽIVATELE, ZÁVĚREČNÁ KONTROLA VÝMAZU
def test_remove_product_cart(page: Page):
    # 1. Launch browser; 
    # 2. Navigate to home url;
    # 3. Verify that home page is visible successfully
    assert page.url == "https://automationexercise.com/"             # ověření, že fixture 'page' otevřela správnou url
    

    # 4. Add products to cart
    ### Přidání 11. a 12. produktu dle pořadí zobrazení na stránce do košíku, identifikace konkrétních produktů probíhá ale podle jejich ID v DOM (ID neodpovídá vždy pořadí na stránce).   
    ### Seznam produktů je na stránce reprezentovaný gridem / mřížkou karet produktů;
    ### každý produkt = jedna karta (v gridu / mřížce)
    ### všechny karty mají stejnou třídu <div class="product-image-wrapper">...</div>
    products = page.locator(".product-image-wrapper")   # CSS lokátor pro seznam všech karet v gridu / mřížce, tzn. karty všech produktů na stránce

    ### Přidání 11. produktu do košíku
    ###### a) Vyhledání 11. produktu dle ID přes href v mřížce a hover
    product_11 = products.filter(has=page.locator("a[data-product-id='13']")).first # vyhledání první karty produktu z mřížky (products), která obsahuje odkaz na detail produktu s daným ID
    product_11.scroll_into_view_if_needed() # pokud je karta produktu mimo viditelnou část stránky, Playwright ji posune do zorného pole, overlay se často aktivuje jen na viditelné kartě
    product_11.hover()                      # simulace najetí myší na kartu produktu, tím se zobrazí overlay vrstva (.product-overlay) a v ní tlačítko 'Add to cart'

    ###### b) Overlay vrstva: Kliknutí na tlačítko 'Add to Cart'
    add_to_cart_prod11_btn = product_11.locator(".overlay-content .btn") # vyhledání tlačítka 'Add to Cart' v overlay vrstvě (vnořený lokátor) UVNITŘ TÉTO KONKRÉTNÍ KARTY produktu 
    add_to_cart_prod11_btn.wait_for(state="visible") # vyčkání, až se overlay vrstva skutečně ukáže
    add_to_cart_prod11_btn.click(force=True)         # kliknutí na tlačítko 'Add to Cart', i když ho dočasně něco překrývá, klik i při krátkém překrytí karty produktu

    ###### c) Modal: Kliknutí na tlačítko 'Continue Shopping' v modalu (popup / vyskakovací okno s tlačítkem 'Continue Shopping')
    continue_shop_btn = page.get_by_role("button", name="Continue Shopping") # lokátor pro tlačítko 'Continue Shopping'
    continue_shop_btn.wait_for(state="visible")                              # vyčkání na plné zobrazení modalu 
    continue_shop_btn.click()                                                # kliknutí na tlačítko 'Continue Shopping' v modalu
    page.wait_for_selector("button:has-text('Continue Shopping')", state="hidden")  # vyčkání na zavření modalu (skrytý stav modalu / tlačítka), pak teprve přejít na další produkt

    ### Přidání 12. produktu do košíku (bude v kroku 7 z košíku vymazán)
    ###### a) Vyhledání 12. produktu dle ID přes href v mřížce a hover
    product_12 = products.filter(has=page.locator("a[data-product-id='14']")).first # vyhledání první karty produktu z mřížky (products), která obsahuje odkaz na detail produktu s daným ID
    product_12.scroll_into_view_if_needed() # pokud je karta produktu mimo viditelnou část stránky, Playwright ji posune do zorného pole, overlay se často aktivuje jen na viditelné kartě
    product_12.hover()                      # simulace najetí myší na kartu produktu, tím se zobrazí overlay vrstva (.product-overlay) a v ní tlačítko 'Add to cart'

    ###### b) Overlay vrstva: Kliknutí na tlačítko 'Add to Cart'
    add_to_cart_prod12_btn = product_12.locator(".overlay-content .btn") # vyhledání tlačítka 'Add to Cart' v overlay vrstvě (vnořený lokátor) UVNITŘ TÉTO KONKRÉTNÍ KARTY produktu 
    add_to_cart_prod12_btn.wait_for(state="visible") # vyčkání, až se overlay vrstva skutečně ukáže
    add_to_cart_prod12_btn.click(force=True)         # kliknutí na tlačítko 'Add to Cart', i když ho dočasně něco překrývá, klik i při krátkém překrytí karty produktu

    ###### c) Modal: Kliknutí na tlačítko 'Continue Shopping' v modalu (popup / vyskakovací okno s tlačítkem 'Continue Shopping')
    continue_shop_btn = page.get_by_role("button", name="Continue Shopping") # lokátor pro tlačítko 'Continue Shopping'
    continue_shop_btn.wait_for(state="visible")                              # vyčkání na plné zobrazení modalu 
    continue_shop_btn.click()                                                # kliknutí na tlačítko 'Continue Shopping' v modalu
    page.wait_for_selector("button:has-text('Continue Shopping')", state="hidden")  # vyčkání na zavření modalu (skrytý stav modalu / tlačítka), pak teprve přejít na další produkt


    # 5. Click 'Cart' button
    cart_link = page.get_by_role("link", name=" Cart")                      # lokátor pro link Cart v záhlaví domovské stránky
    cart_link.click()


    # 6. Verify that cart page is displayed
    ### a) Technické ověření přesměrování na stránku košíku (kontrola URL)
    expect(page).to_have_url("https://automationexercise.com/view_cart")     
    
    ### b) Uživatelské ověření, že je skutečně zobrazen obsah nákupního košíku
    shopping_cart_heading = page.get_by_text("Shopping Cart") # nebo s CSS lokátorem: shopping_cart_heading = page.locator("ol.breadcrumb li.active") 
    expect(shopping_cart_heading).to_be_visible()             # nebo s CSS lokátorem: expect(shopping_cart_heading).to_have_text("Shopping Cart")     


    # 7. Click 'X' button corresponding to particular product
    # Výmaz řádku s 12. produktem v nákupním košíku (product_id = 14)

    ### Identifikace produktu určeného pro výmaz
    ### Vizuálně 12. produkt v pořadí na domovské stránce, ale ve skutečnosti má product_id = 14
    product_id = "14"

    ### Lokátor řádku daného produktu v nákupním košíku
    product_row = page.locator(f"tr#product-{product_id}")

    ### Lokátor tlačítka pro smazání (x) v rámci daného řádku vybraného pro výmaz
    product_delete_btn = product_row.locator("a.cart_quantity_delete")

    ### Kliknutí na tlačítko (link) pro výmaz (x)
    product_delete_btn.click()


    # 8. Verify that product is removed from the cart
    expect(product_row).to_have_count(0)

 

























