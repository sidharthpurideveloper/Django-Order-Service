# Django-Order-Service

# python 3.10 
# conda create -n django python=3.10
# conda activate django
# git clone <repository-url>
# cd stgi-ecommerce 
# pip install -r requirements.txt 
# cd stgi_ecommerce
# python manage.py makemigrations
# python manage.py migrate 
# python manage.py runserver

# I'm using default as postgresql, please uncomment database setting for sqlite, clear out migrations if you want to.

# entry-point - http://127.0.0.1:8000/api/

# make customers , make products , then go on making orders

# sample create order json = 

{
  "customer": 1,
  "order_date": "2024-08-26T10:00:00Z",
  "status": "Pending",
  "order_items": [
    {
      "product": 1,
      "quantity": 2
    },
    {
      "product": 2,
      "quantity": 1
    }
  ]
}
