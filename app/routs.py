from flask import render_template
from app import app
from app.fake_data import site_menu
from app.fake_data import catalog


@app.route("/")
def index():
    return render_template("index.html", title="Главная", menu_list=site_menu)


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
def get_product():
    return render_template("products.html", title="{{}}", menu_list=site_menu)


@app.route("/about")
def about():
    pass


@app.route("/contacts")
def contacts():
    pass
