# Django-Order-Service

# python 3.10 
# conda env

# I'm using default postgresql uncomment setting for sqlite, clear out migrations if you want to 

# entry-point - http://127.0.0.1:8000/api/

# make customers , make products 

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
