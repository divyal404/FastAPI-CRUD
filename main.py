import fastapi
from models import Product
from database import session, engine
import database_models
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware


app = fastapi.FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"])

database_models.Base.metadata.create_all(bind=engine)

@app.get("/")
def hello():
    return {"Hello, Welcome to FastAPI Website"}

products=[
    Product(id=1, name="Product 1", description="budget Phone", price=10.99, quantity=5),
    Product(id=2, name="Product 2", description="premium Phone", price=19.99, quantity=10),
    Product(id=3, name="Product 3", description="budget Laptop", price=100.99, quantity=15),
    Product(id=4, name="Product 4", description="premium Laptop", price=199.99, quantity=20)
]

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()


def init_db():
    db = session()
    count = db.query(database_models.Product).count()
    if count == 0:
        for product in products:
            db.add(database_models.Product(**product.model_dump()))
        db.commit()

init_db()

@app.get("/products")
def get_all_products(db: Session = fastapi.Depends(get_db)):
    db_products = db.query(database_models.Product).all()
    return db_products

@app.get("/products/{id}")
def get_all_product_by_id(id: int, db: Session = fastapi.Depends(get_db)):
    db_products = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_products:
        return db_products
    return "Product not found"

@app.post("/products")
def create_product(product: Product, db: Session = fastapi.Depends(get_db)):
    db.add(database_models.Product(**product.model_dump()))
    db.commit()
    return "Product created successfully"

@app.put("/products/{id}")
def update_product(id: int, product: Product, db: Session = fastapi.Depends(get_db)):
    db_products = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_products:
        db_products.name = product.name
        db_products.description = product.description
        db_products.price = product.price
        db_products.quantity = product.quantity

        db.commit()
        return "Product updated successfully"
    else:
        return "Product not found"

@app.delete("/products/{id}")
def delete_product(id: int, db: Session = fastapi.Depends(get_db)):
    db_products = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_products:
        db.delete(db_products)
        db.commit()
        return "Product deleted successfully"
    else:
        return "Product not found"