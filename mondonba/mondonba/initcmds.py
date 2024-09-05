from gestione.models import *

def erase_db():
    print("Delete il DB")
    Product.objects.all().delete()
    Cart.objects.all().delete()
    Comment.objects.all().delete()

def init_db():
    if len(Product.objects.all()) != 0:
        return

    productdict = {
        "names": ["Vince Carter Funko Pop", "LaMelo Ball Funko Pop", "Luka Dončić Funko Pop", "Scottie Barnes Funko Pop", "Dirk Nowitzki Funko Pop",
                  "Allen Iverson Uniform", "Michael Jordan Uniform", "LeBron James Uniform", "Nikola Jokić Uniform", "De'Aaron Fox Uniform",
                  "NBA Wilson Ball 1", "NBA Wilson Ball 2", "NBA Wilson Ball 3", "NBA Wilson Ball 4", "NBA Wilson Ball 5",
                  "NBA Shoes 1", "NBA Shoes 2", "NBA Shoes 3", "NBA Shoes 4", "NBA Shoes 5",
                  "NBA Bag 1", "NBA Bag 2", "NBA Bag 3", "NBA Bag 4", "NBA Bag 5",
                  "NBA Gadget 1", "NBA Gadget 2", "NBA Gadget 3", "NBA Gadget 4", "NBA Gadget 5",
                  "LeBron James Jersey (Olympic Edition)", "Anthony Davis Jersey (Olympic Edition)", "Jrue Holiday Jersey (Olympic Edition)", "Kevin Durant Jersey (Olympic Edition)", "Stephen Curry Jersey (Olympic Edition)"],
        "prices": ["15", "15", "15", "15", "15",
                   "70", "70", "70", "25", "25",
                   "35", "35", "35", "35", "35",
                   "120", "120", "120", "120", "120",
                   "30", "30", "30", "30", "30",
                   "5", "5", "5", "5", "5",
                   "45", "45", "45", "45", "45"],
        "valuation": [],
        "category": ["Gadget", "Gadget", "Gadget", "Gadget", "Gadget",
                     "Clothing", "Clothing", "Clothing", "Clothing", "Clothing",
                     "Tool", "Tool", "Tool", "Tool", "Tool",
                     "Clothing", "Clothing", "Clothing", "Clothing", "Clothing",
                     "Tool", "Tool", "Tool", "Tool", "Tool",
                     "Gadget", "Gadget", "Gadget", "Gadget", "Gadget",
                     "Clothing", "Clothing", "Clothing", "Clothing", "Clothing"],
        "description": [],
        "image": []
    }
    for i in range(35):
        p = Product()
        p.name = productdict["names"][i]
        p.price = productdict["prices"][i]
        p.valuation = 0
        p.category = productdict["category"][i]
        i = i + 1
        productdict["description"].append("Description" + str(i))
        if i < 10:
            i = "0" + str(i)
        productdict["image"].append("products/product-" + str(i) + ".jpg" )
        p.description = productdict["description"][int(i) - 1]
        p.image = productdict["image"][int(i) - 1]
        p.save()

    print("Create DB!")


