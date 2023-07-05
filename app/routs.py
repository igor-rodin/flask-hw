from flask import render_template
from app import app
from app.fake_data import site_menu
from app.fake_data import catalog, get_product_by_id


@app.route("/")
def index():
    return render_template(
        "index.html", caption="Фреймворки Flask и FastAPI (семинары)"
    )


@app.route("/shop")
def shop():
    return render_template("shop.html", title="Главная", menu_list=site_menu)


@app.route("/products/")
@app.route("/products/<string:category>")
def products(category: str = "all"):
    match category:
        case "all":
            products = list(catalog.values())
        case _:
            products = [catalog[category]]
    return render_template(
        "products.html", title="Наша продукция", menu_list=site_menu, products=products
    )


@app.route("/product/<int:id>")
def get_product(id: int):
    product = get_product_by_id(id)
    title = f"{product['brand']}/{product['title']}"
    return render_template(
        "product.html", title=title, menu_list=site_menu, product=product
    )


@app.route("/about")
def about():
    return render_template("about.html", title="О компании", menu_list=site_menu)
