# Sada automatizovaných testů (pytest) na demo e-shop webu 'https://automationexercise.com/'
# testy volají fixtures 'page', 'browser_context', 'accept_gdpr' definované v souboru conftest.py;
# testy následující všechny požadované kroky uvedené v test cases pro daný web (https://automationexercise.com/test_cases)

from playwright.sync_api import Page, expect

# 12_TEST CASE: Add Products in Cart
# TEST PŘIDÁNÍ PRVNÍCH DVOU PRODUKTŮ DO NÁKUPNÍHO KOŠÍKU SE ZÁVĚREČNOU KONTROLOU KOŠÍKU
def test_product_cart(page: Page):
    # 1. Launch browser; 
    # 2. Navigate to home url;
    # 3. Verify that home page is visible successfully
    assert page.url == "https://automationexercise.com/"             # ověření, že fixture 'page' otevřela správnou url
    
    # 4. Click on 'Products' button
    products_link = page.get_by_role("link", name=" Products")     # lokátor pro vyhledání linku pro 'Products' stránku
    products_link.click()                                           # kliknutí na link 'Products'
    
    # 5. Hover over first product and click 'Add to cart'
    ### Seznam produktů je na stránce reprezentovaný gridem / mřížkou karet produktů;
    ### každý produkt = jedna karta (v gridu / mřížce)
    ### všechny karty mají stejnou třídu <div class="product-image-wrapper">...</div>
    ### 1. karta / produkt: .product-image-wrapper.first nebo .product-image-wrapper.nth(0)
    ### 2. karta / produkt: .product-image-wrapper.nth(1)
    ### 3. karta / produkt: .product-image-wrapper.nth(2)
    ### poslední karta / produkt: .product-image-wrapper.last
    products = page.locator(".product-image-wrapper")       # CSS lokátor pro seznam všech karet v gridu / mřížce, tzn. karty všech produktů na stránce
    first_product = products.nth(0)                         # proměnná pro určení pozice karty 1. produktu v mřížce

    expect(first_product).to_be_visible(timeout=1000)       # časová rezerva na vyobrazení karty 1. produktu na nové stránce
    
    first_product.hover()

    add_to_cart_prod1_btn = page. locator(".overlay-content > .btn").nth(0)  # lokátor pro tlačítko 'Add to cart' u 1. produktu s krycí vrstvou
    add_to_cart_prod1_btn.click()

    # 6. Click 'Continue Shopping' button
    continue_shop_btn = page.get_by_role("button", name="Continue Shopping")    # lokátor tlačítka 'Continue Shopping'
    continue_shop_btn.click()                                                   # kliknutí na tlačítko

    # 7. Hover over second product and click 'Add to cart'
    second_product = products.nth(1)                         # proměnná pro určení pozice karty 2. produktu v mřížce

    expect(second_product).to_be_visible(timeout=1000)       # časová rezerva na vyobrazení karty 2. produktu na nové stránce
    
    second_product.hover()

    add_to_cart_prod2_btn = page. locator(".overlay-content > .btn").nth(1)  # lokátor pro tlačítko 'Add to cart' u 2. produktu s krycí vrstvou
    add_to_cart_prod2_btn.click()                                            # kliknutí na tlačítko 'Add to cart' (tzn. přidání do košíku)
    
    # 8. Click 'View Cart' button
    view_cart_link = page.get_by_role("link", name="View Cart")    # lokátor pro link 'View Cart' v zobrazeném oknu
    view_cart_link.click()                                         # kliknutí na link 'View Cart'
    
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

























