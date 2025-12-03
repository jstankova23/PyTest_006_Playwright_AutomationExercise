# Sada automatizovaných testů (pytest) na demo e-shop webu 'https://automationexercise.com/'
# testy volají fixtures definované v souboru conftest.py;
# testy následující všechny požadované kroky uvedené v test cases pro daný web (https://automationexercise.com/test_cases)

"""

VÝZNAM:       kontejner                                > kolekce karet                            > produkt
PROMĚNNÁ:     features_container/recommended_cotainer  > features_products/recommended_products   > product_XX (XX - pořadové číslo na stránce pro uživatele)
CSS SELEKTOR: div.features_items/div.recommended_items > .product-image-wrapper                   > a[data-product-id="YY"]
                                                                                                    product_id = "YY" (YY - ID productu v DOM)

Kontejner pro FEATURES ITEMS:
features_container = page.locator("div.features_items")                  # kontejner
features_products = features_container.locator(".product-image-wrapper") # kolekce karet
product_id = "YY"                                                        # ID produktu (pořadové číslo produktu z aplikace neodpovídá vždy ID produktu)                           
product_XX = features_products.filter(has=page.locator(f'a[data-product-id="{product_id}"]') # produkt 

"""
from playwright.sync_api import Page, expect

# 12_TEST CASE: Add Products in Cart
# TEST PŘIDÁNÍ PRVNÍCH DVOU PRODUKTŮ DO NÁKUPNÍHO KOŠÍKU Z HOME PAGE BEZ PŘIHLÁŠENÍ UŽIVATELE, SE ZÁVĚREČNOU KONTROLOU KOŠÍKU
def test_product_cart(page: Page):
    # 1. Launch browser; 
    # 2. Navigate to home url;
    # 3. Verify that home page is visible successfully
    assert page.url == "https://automationexercise.com/"             # ověření, že fixture 'page' otevřela správnou url
    
    # 4. Click on 'Products' button
    products_link = page.get_by_role("link", name=" Products")     # lokátor pro vyhledání linku pro 'Products' podstránku v záhlaví domovské stránky
    products_link.click()                                           # kliknutí na link 'Products'
    
    # 5. Hover over first product and click 'Add to cart'
    ### Seznam produktů je v horní části home page v sekci FEATURES ITEMS reprezentovaný gridem / mřížkou karet produktů;
    ### Každý produkt = jedna karta (v gridu / mřížce)
    ### Všechny karty mají stejnou třídu <div class="product-image-wrapper">...</div>
    features_container = page.locator("div.features_items")                      # lokátor pro kontejner/sekci features items položek v horní části home page
    features_products = features_container.locator(".product-image-wrapper")     # vnořený lokátor, kolekce všech karet produktů v kontejneru/sekci features items položek

    ###### a) Vyhledání 1. produktu dle ID přes href v mřížce a hover
    product_id = "1"
    product_1 = features_products.filter(has=page.locator(f"a[data-product-id='{product_id}']")).first # vyhledání první karty produktu z mřížky (products), která obsahuje odkaz na detail produktu s daným ID
    product_1.scroll_into_view_if_needed() # pokud je karta produktu mimo viditelnou část stránky, Playwright ji posune do zorného pole, overlay se často aktivuje jen na viditelné kartě
    product_1.hover()                      # simulace najetí myší na kartu produktu, tím se zobrazí overlay vrstva (.product-overlay) a v ní tlačítko 'Add to cart'

    ###### b) Overlay vrstva: Kliknutí na tlačítko 'Add to Cart'
    add_to_cart_prod1_btn = product_1.locator(".overlay-content .btn") # vyhledání tlačítka 'Add to Cart' v overlay vrstvě (vnořený lokátor) UVNITŘ TÉTO KONKRÉTNÍ KARTY produktu 
    add_to_cart_prod1_btn.wait_for(state="visible") # vyčkání, až se overlay vrstva skutečně ukáže
    add_to_cart_prod1_btn.click(force=True)         # kliknutí na tlačítko 'Add to Cart', i když ho dočasně něco překrývá, klik i při krátkém překrytí karty produktu

    # 6. Modal: Click 'Continue Shopping' button
    continue_shop_btn = page.get_by_role("button", name="Continue Shopping") # lokátor pro tlačítko 'Continue Shopping'
    continue_shop_btn.wait_for(state="visible")                              # vyčkání na plné zobrazení modalu 
    continue_shop_btn.click()                                                # kliknutí na tlačítko 'Continue Shopping' v modalu
    page.wait_for_selector("button:has-text('Continue Shopping')", state="hidden")  # vyčkání na zavření modalu (skrytý stav modalu / tlačítka), pak teprve přejít na další produkt

    # 7. Hover over second product and click 'Add to cart'
    ###### a) Vyhledání 2. produktu dle ID přes href v gridu a hover
    product_id = "2"
    product_2 = features_products.filter(has=page.locator(f"a[data-product-id='{product_id}']")).first
    product_2.scroll_into_view_if_needed()  
    product_2.hover()

    ###### b) Overlay vrstva: Kliknutí na tlačítko 'Add to Cart'
    add_to_cart_prod7_btn = product_2.locator(".overlay-content .btn")
    add_to_cart_prod7_btn.wait_for(state="visible") 
    add_to_cart_prod7_btn.click(force=True)
    

    # 8. Modal: Click 'View Cart' button
    view_cart_link = page.get_by_role("link", name="View Cart")             # lokátor pro link 'View Cart' v zobrazeném modalu
    view_cart_link.wait_for(state="visible")                                # vyčkání na plné zobrazení modalu 
    view_cart_link.click()                                                  # kliknutí na link 'View Cart'
    page.wait_for_selector("button:has-text('View Cart')", state="hidden")  # vyčkání na zavření modalu (skrytý stav modalu / tlačítka)


    # 9. Verify both products are added to Cart
    ### Lokátory pro řádky 1. a 2. produktu v nákupním košíku
    ### Každý řádek reprezentuje jeden konkrétní produkt a obsahuje:
    ### - jednotkovou cenu (price)
    ### - objednané množství (quantity)
    ### - celkovou cenu za produkt (total = price * quantity)

    ### Řádkové lokátory
    cart_product_line1 = page.locator("tr#product-1")   
    cart_product_line2 = page.locator("tr#product-2")

    ### Inteligentní assert – vyčkání, dokud se oba produkty v košíku nezobrazí
    ### to_be_visible() – ověření, že produkt skutečně existuje v košíku
    expect(cart_product_line1).to_be_visible()
    expect(cart_product_line2).to_be_visible()

    # 10. Verify their prices, quantity and total price
    ### Kvůli stabilitě testu i při případné změně cen se neověřují konkrétní hodnoty cen, ale pouze:
    ### - existence jednotkové ceny (price)
    ### - správné množství (quantity)
    ### - existence celkové ceny produktu (total)
    ### not_to_be_empty() - jednotková cena produktu (price) a celková cena produktu (total) nejsou prázdné;
    ### to_have_value("1") - definice podmínky, že v košíku je přesně 1 produkt od daného výrobku.

    ### 1. produkt (lokalizace jednotlivých údajů v rámci řádkového lokátoru produktu)
    product_1_price = cart_product_line1.locator("td.cart_price")       # lokátor pro jednotkovou cenu 1. produktu v košíku 
    product_1_quantity = cart_product_line1.locator("td.cart_quantity button") # lokátor pro množství (tlačítko v buňce cart_quantity) u 1. produktu v košíku
    product_1_total = cart_product_line1.locator("p.cart_total_price")  # lokátor pro celkovou cenu 1. produktu v košíku

    expect(product_1_price).not_to_be_empty()    # ověření, že pole s jednotkovou cenou 1. produktu není prázdné    
    expect(product_1_quantity).to_have_text("1") # ověření množství podle textu tlačítka (nejedná se o input element)
    expect(product_1_total).not_to_be_empty()    # ověření, že pole s celkovou cenou 1. produktu není prázdné

    ### 2. produkt (lokalizace jednotlivých údajů v rámci řádkového lokátoru produktu)
    product_2_price = cart_product_line2.locator("td.cart_price")
    product_2_quantity = cart_product_line2.locator("td.cart_quantity button")
    product_2_total = cart_product_line2.locator("p.cart_total_price")

    expect(product_2_price).not_to_be_empty()
    expect(product_2_quantity).to_have_text("1")       
    expect(product_2_total).not_to_be_empty()

























