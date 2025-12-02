# Sada automatizovaných testů (pytest) na demo e-shop webu 'https://automationexercise.com/'
# testy volají fixtures definované v souboru conftest.py;
# testy následující všechny požadované kroky uvedené v test cases pro daný web (https://automationexercise.com/test_cases)

from playwright.sync_api import Page, expect

# 18_TEST CASE: View Category Products
# TEST FILTRACE PRODUKTŮ PODLE ZNAČEK Z PODSTRÁNKY PRODUCTS S OVĚŘENÍM ZOBRAZENÍ PRODUKTŮ
def test_filter_brands_products_page(page: Page):
    # 1. Launch browser; 
    # 2. Navigate to home url;
    assert page.url == "https://automationexercise.com/"            # ověření, že fixture 'page' otevřela správnou url

    # 3. Click on 'Products' button
    products_link = page.get_by_role("link", name=" Products")     # lokátor pro vyhledání linku pro 'Products' podstránku v záhlaví domovské stránky
    products_link.click()                                           # kliknutí na link 'Products'    

    # 4. Verify that Brands are visible on left side bar
    #### Levý svislý postranní panel slouží k filtraci produktů
    brands_heading = page.get_by_role("heading", name="Brands")     # vyhledání nadpisu 'BRANDS' na domovské stránce
    expect(brands_heading).to_be_visible()


    # 5. Click on H&M brand name
    hm_brand_link = page.get_by_role("link", name="(5) H&M")        # vyhledání nadpisu / linku 'H&M' v sekci 'BRANDS'
    hm_brand_link.click()                                           # kliknutí na link
                                  

    # 6. Verify that user is navigated to H&M brand page and brand products are displayed
    ### a) UI ověření - zobrazení stránky s nadpisem "BRAND - H&M PRODUCTS"
    brand_hm_products_heading = page.get_by_role("heading", name="Brand - H&M Products")
    expect(brand_hm_products_heading).to_be_visible(timeout=1000) 

    ### b) Technické ověření přesměrování - kontrola URL
    expect(page).to_have_url("https://automationexercise.com/brand_products/H&M")    

    ### c) Ověření, že jsou zobrazeny produkty
    ### Ověření, že filtrace vrátila alespoň jeden produkt (netestuje se pevný počet)
    
    ### Hierarchie prvků v DOM (dle DevTools): 
    ###### kontejner          > kolekce karet (s ID jedna konkrétní karta) > vnitřní obsah karty
    ###### div.features_items > .product-image-wrapper                     > div.single-products

    ###### div.features_items     = univerzální kontejner všech karet produktů (rodič, obal výsledků)
    ###### .product-image-wrapper = každá karta v kontejneru má tuto třídu, lokátor vrací celou kolekci karet v kontejneru, pro výběr konkrétní karty nutné uvést ID (např. tr#product-14)
    ###### div.single-products    = vnitřní obsah jedné karty, např. název produktu, cena, tlačítka (vnuk kontejneru)
    products_container = page.locator("div.features_items")      
    products = products_container.locator("div.single-products") 
    expect(products).not_to_have_count(0)                        # ověření, že výpis produktů není prázdný


    # 7. On left side bar, click on BIBA brand link
    ### Kliknutí na jinou značku ve filtru BRANDS v levém postranním panelu
    biba_link = page.get_by_role("link", name="(5) Biba")           # vyhledání nadpisu / linku 'BIBA' v sekci 'BRANDS'
    biba_link.click()                                               # kliknutí na link

    
    # 8. Verify that user is navigated to BIBA brand page and can see products
    ### a) UI ověření - zobrazení stránky s nadpisem "BRAND - BIBA PRODUCTS"
    brand_biba_products_heading = page.get_by_role("heading", name="Brand - Biba Products")
    expect(brand_biba_products_heading).to_be_visible(timeout=1000) 

    ### b) Technické ověření přesměrování - kontrola URL
    expect(page).to_have_url("https://automationexercise.com/brand_products/Biba") 

    ### c) Ověření, že jsou zobrazeny produkty
    products_container = page.locator("div.features_items")      
    products = products_container.locator("div.single-products") 
    expect(products).not_to_have_count(0)                        # ověření, že výpis produktů není prázdný


