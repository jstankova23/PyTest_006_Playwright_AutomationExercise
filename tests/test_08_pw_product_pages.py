# Sada automatizovaných testů (pytest) na demo e-shop webu 'https://automationexercise.com/'
# testy volají fixtures 'page', 'browser_context', 'accept_gdpr' definované v souboru conftest.py;
# testy následující všechny požadované kroky uvedené v test cases pro daný web (https://automationexercise.com/test_cases)

from playwright.sync_api import Page, expect

# 08_TEST CASE: Verify All Products and product detail page
# OVĚŘENÍ PŘESMĚROVÁNÍ Z DOMOVSKÉ STRÁNKY 'https://automationexercise.com/' NA PODSTRÁNKY S PRODUKTY 'https://automationexercise.com/products'
# A NA PODSTRÁNKU S DETAILY PRVNÍHO PRODUKTU 'https://automationexercise.com/product_details/1' 
def test_product_pages(page: Page):
    # 1. Launch browser; 
    # 2. Navigate to home url;
    # 3. Verify that home page is visible successfully
    assert page.url == "https://automationexercise.com/"             # ověření, že fixture 'page' otevřela správnou url
    

    # 4. Click on 'Products' button
    products_link = page.get_by_role("link", name=" Products")     # vyhledání linku pro 'Products' stránku
    products_link.click()                                           # kliknutí na link 'Products'
    

    # 5. Verify user is navigated to ALL PRODUCTS page successfully (new page)
    ### ověření, že se zobrazí na stránce nadpis 'ALL PRODUCTS'
    all_products_heading = page.get_by_role("heading", name="All Products")   # lokátor pro nadpis 'ALL PRODUCTS' na nové stránce
    expect(all_products_heading).to_be_visible(timeout=2000)       # ověření přesměrování na stránku s daným nadpisem a zpomalení


    # 6. The products list is visible
    ### Seznam produktů je na stránce reprezentovaný gridem / mřížkou karet produktů;
    ### každý produkt = jedna karta (v gridu / mřížce)
    ### všechny karty mají stejnou třídu <div class="product-image-wrapper">...</div>
    products = page.locator(".product-image-wrapper")    # CSS lokátor pro seznam všech karet v mřížce, tzn. karty všech produktů na stránce
    expect(products.first).to_be_visible(timeout=2000)   # časová rezerva na vyobrazení karty 1. produktu na nové stránce

    # 7. Click on 'View Product' of first product
    ### 1. karta / produkt: .product-image-wrapper.first nebo .product-image-wrapper.nth(0)
    view_product1_link = page.locator(".nav.nav-pills.nav-justified > li > a").first     # lokalizátor pro link 'View Product' u 1. zobrazeného produktu
    view_product1_link.click()                                                           # kliknutí na link
    
                                                     
    # 8. User is landed to product detail page
    ### a) technické ověření přesměrování (kontrola URL)
    expect(page).to_have_url("https://automationexercise.com/product_details/1")         # vyčkání na přesměrování na stránku s detaily o 1. produktu
    
    ### b) uživatelské ověření
    ### ověření na základě bloku s detaily o produktu (název, kategorie, cena, dostupnost, stav, značka), tento blok není na home page, jen na stránce 'product_details'
    product_info_block = page.locator("div.product-information") # lokátor pro blok s detaily pro každý produkt
    expect(product_info_block).to_be_visible()


    # 9. Verify that product detail is visible: product name, category, price, availability, condition, brand
    
    ### lokátory pro pole určená pro detailní informace o produktu
    ##### nejsou spjaté s konkrétní hodnotou, 1.produkt se může v čase měnit)
    ##### funkční lokátory z Playwright Inspectora nejsou jednoznačné, nutné použít CSS lokátory
    product_name = page.locator("div.product-information > h2") # lokátor pro blok s detaily zacílený na nadpis / název produktu       
    category = page.locator("p:has-text('Category')")
    price = page.locator("div.product-information span").first  # locator("span:has-text('Rs.')") není jednoznačný pro danou stránku
    availability = page.locator("p:has-text('Availability')")
    condition = page.locator("p:has-text('Condition')")
    brand = page.locator("p:has-text('Brand')")

    ### ověření nenulových hodnot polí - parametrizovaná funkce:
    ##### 1. parametr: proměnná pro lokátor daného pole
    ##### 2. parametr: proměnná pro název daného pole (kvůli přesnější chybové hlášce, které pole je vlastně prázdné).

    ##### lokátor získá text daného elementu bez mezer před a za textem a uloží ho do proměnné 'text';
    ##### některé HTML elementy obsahují jen mezery a bez metody strip() pro odstranění mezer by Playwright tvrdil, že text existuje, ale nic by nebylo vidět
    ##### text != "" ... pokud je text prázdný, tak Fail; jinak PASS
    ##### kvůli jednoznačnosti hlášky je funkce pro ověření nenulové hodnoty polí doplněna o parametr 'Pole' 
    def assert_not_empty(locator, name="Pole"):
        text = locator.text_content().strip()          # možnost i použít metodu inner_text(), je ale pomalejší
        assert text, f"Pozor, pole {name} je prázdné!"

    assert_not_empty(product_name, "Název produktu")
    assert_not_empty(category, "Kategorie")
    assert_not_empty(price, "Cena")
    assert_not_empty(availability, "Dostupnost")
    assert_not_empty(condition, "Stav zboží")
    assert_not_empty(brand, "Značka")























