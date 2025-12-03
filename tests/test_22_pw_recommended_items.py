# Sada automatizovaných testů (pytest) na demo e-shop webu 'https://automationexercise.com/'
# testy volají fixtures definované v souboru conftest.py;
# testy následující všechny požadované kroky uvedené v test cases pro daný web (https://automationexercise.com/test_cases)

"""

VÝZNAM:       kontejner                                > kolekce karet                            > produkt
PROMĚNNÁ:     features_container/recommended_cotainer  > features_products/recommended_products   > product_XX (XX - pořadové číslo na stránce pro uživatele)
CSS SELEKTOR: div.features_items/div.recommended_items > .product-image-wrapper                   > a[data-product-id="YY"]
                                                                                                    product_id = "YY" (YY - ID productu v DOM)

Kontejner pro RECOMMENDED ITEMS:
recommended_container = page.locator("div.recommended_items")                  # kontejner
recommended_products = recommended_container.locator(".product-image-wrapper") # kolekce karet
product_id = "YY"                                                              # ID produktu (pořadové číslo produktu z aplikace neodpovídá vždy ID produktu)                           
product_XX = recommended_products.filter(has=page.locator(f'a[data-product-id="{product_id}"]') # produkt 

"""
from playwright.sync_api import Page, expect

# 22_TEST CASE: Add to cart from Recommended items
# TEST PŘIDÁNÍ DO KOŠÍKU PRODUKTU ZE SEKCE 'RECOMMENDED ITEMS' VE SPODNÍ ČÁSTI DOMOVSKÉ STRÁNKY A KONTROLA KOŠÍKU
 # V carouselu (pás pohyblivých slidů s kartami produktů) v sekci RECOMMENDED ITEMS v zápati Home page produkty mění třídy `item active`, `item`, `item next left` 
 # a nákup je možný u produktu pouze ve stavu s třídou `item active`.
def test_recommended_items(page: Page):
    # 1. Launch browser; 
    # 2. Navigate to home url;
    assert page.url == "https://automationexercise.com/"             # ověření, že fixture 'page' otevřela správnou url
    

    # 3. Scroll to bottom of page
    recomended_items_heading = page.get_by_role("heading", name="recommended items") # lokátor na nadpis "RECOMMENDED ITEMS" dole na home page
    recomended_items_heading.scroll_into_view_if_needed() # skrolování k nadpisu "RECOMMENDED ITEMS"


    # 4. Verify 'RECOMMENDED ITEMS' are visible
    ### a) Ověření nadpisu 'RECOMMENDED ITEMS'
    expect(recomended_items_heading).to_be_visible(timeout=500)  # ověření, že Playwright našel v zápatí požadovaný nadpis (lokátor z kroku 3)
    
    ### b) Ověření zobrazení carouselu (pohyblivých slidů karet doporučených produktů)
    recommended_container = page.locator("div.recommended_items")   # lokátor pro kontejner/sekci dopouručených položek
    expect(recommended_container).to_be_visible()                   # ověření, že daný kontejner je na stráce zobrazený

    recommended_products = recommended_container.locator(".product-image-wrapper") # vnořený lokátor pro prvek představující všechny karty produktů
    expect(recommended_products).not_to_have_count(0)   # musí existovat alespoň 1 doporučený produkt (min. 1 karta produktu)


    # 5. Click on 'Add To Cart' on Recommended product (product_id = 2)
    # POZOR: NÁKUP ZE SEKCE 'RECOMMENDED ITEMS', nikoliv s horní sekce 'FEATURES ITEMS'
    # V carouselu v sekci RECOMMENDED ITEMS v zápati Home page produkty mění třídy `item active`, `item`, `item next left` a nákup je možný u produktu pouze 
    # ve stavu s třídou `item active`.

    # Vyhledání produktu 2 v sekci RECOMMENDED ITEMS v dolní části domovské stránky
    product_id = "2"
  
    active_slide = recommended_container.locator(".carousel-inner .item.active")  # pouze AKTIVNÍ slide carouselu, tzn. třída `item active`

    recommended_product_2 = (active_slide.locator(".product-image-wrapper").filter(has=page.locator(f"a[data-product-id='{product_id}']")).first)

    # Kliknutí na link 'Add to Cart' u vybraného produktu
    add_to_cart_btn = recommended_product_2.locator("a.btn.add-to-cart")    # vnořený lokátor, tlačítko/link 'Add to Cart' v dané kartě produktu v dané sekci home page
    add_to_cart_btn.wait_for(state="visible")                               # vyčkání, až bude tlačítko/link vidět
    add_to_cart_btn.click()                                                 # kliknutí, tzn. přidání produktu do košíku




    # 6. Click on 'View Cart' button
    # Modal: Kliknutí na tlačítko 'Continue Shopping' v modalu (popup / vyskakovací okno s tlačítkem 'View Cart')
    view_cart_link = page.get_by_role("link", name="View Cart")             # lokátor pro link 'View Cart' v zobrazeném modalu
    view_cart_link.wait_for(state="visible")                                # vyčkání na plné zobrazení modalu 
    view_cart_link.click()                                                  # kliknutí na link 'View Cart'
    page.wait_for_selector("button:has-text('View Cart')", state="hidden")  # vyčkání na zavření modalu (skrytý stav modalu / tlačítka)


    # 7. Verify that product is displayed in cart page
    ### a) Technické ověření přesměrování (kontrola URL) na stránku s nákupní košíkem
    expect(page).to_have_url("https://automationexercise.com/view_cart")
    
    ### b) Uživatelské ověření přesměnrování (kontrola nadpisu podstránky)
    shopping_cart_heading = page.get_by_text("Shopping Cart")       # lokátor pro nadpis 'Shopping Cart' v záhlaví podstránky
    expect(shopping_cart_heading).to_be_visible()

    ### c) Ověření, že v nákupních košíku je řádek týkající se daného produktu 2
    cart_product_2 = page.locator("tr#product-2")                   # lokátor pro řádek 2. produktu v nákupním košíku (řádkový lokátor)       
    expect(cart_product_2).not_to_have_count(0)                     # na stránce s nákupním košíkem musí existovat řádek o produktu 2 