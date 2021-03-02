[![Account Password change](https://img.shields.io/twitter/follow/NicolasNasr )](https://twitter.com/NicolasNasr)   

# E-commerce Website

E-commerce website built with django 3.1.7 and Python 3.9.1  
[Live Demo](https://nicolas-e-commerce.herokuapp.com)  
[![Account Password change](https://img.shields.io/website?url=https%3A%2F%2Fnicolas-e-commerce.herokuapp.com%2Fstore%2F )](https://nicolas-e-commerce.herokuapp.com/store/)   

<hr>

#### Landing Page
![Landing Page](https://i.imgur.com/vSYxRHI.png "Landing Page")
When Visiting the website The user will be prompted to the 'Store' Page where he will be able to browse/add/view Products.  
Out of stocks items will show that, and the customer will still be able to view them but he cannot add them to the cart.
<br><br>

#### Tokens:
Each visitor will be given a Token that will let them Add items to their cart and checkout without logging in (They can still login if they want to )  
![Token](https://i.imgur.com/UQPSuVK.png "Token")

![Token](https://i.imgur.com/scK7W2m.png "Token")  

<br>

#### Filter:
The customer will be able to filter products by: Category, price, search by product name  
![Filter](https://i.imgur.com/lH87LZ7.png "Filter")  

#### Product Page:  
View product description, specs, rating, price and quantity available 
![Product Page](https://i.imgur.com/NjpF1UE.png "Product Page")  
  <br><br>

#### Shopping Cart:
When a customer first add an Item to the cart an order will be created for that customer and it will be marked as not complete.  
If the visitor is not logged in, the order will be assigned to his device [Token](./README.md#Tokens) .  

The customer will be able to see the items that he has added to the cart, he can adjust the quantity, and the prices will update in real time, the product will be removed from cart if the quantity reaches 0 and the user will be alerted if he keeps increasing quantity over the total qty.  

Total is calculated: subTotal + 10% (shipping and handling)
![Shopping Cart](https://i.imgur.com/Kk2d3rZ.png "Shopping Cart")  
![Shopping Cart](https://i.imgur.com/pfRxIzY.png "Shopping Cart")  
![Max qty](https://i.imgur.com/UWOn6JO.png "Max qty")  
###### (At the center we have the quantity that the user has added/total quantity, on the left we have the initial product price, and on the right we have the total price for an item; item price*quantity added)  

<br>

#### Checkout:  
For the user to be able to proceeds to the checkout page they need to have items in their cart otherwise they will be redirected to the home page with a warning message like this one:   
![Warning add to cart](https://i.imgur.com/fS4v9In.png "Warning add to cart")  

Once the user reaches the checkout page they can review their order on the right hand side and add a Discount coupon (c, 4, NICOLAS; are some demo coupons); They can't add more than one coupon at a time.

They will need to fill out their address then in order to be able to make the payment (The order will be noted as complete but not shipped).  
Name and E-mail are only required if a user is not logged in else they will not appear.
###### (For now the payment form is only a button)
![Checkout](https://i.imgur.com/bEPV5KD.png "Checkout")  

<br>

#### Order Track:
Once the payment is done the user will be redirected to his order page Where they can check the order status, delivery date, transaction id (That will let the user to track their order), price, and cancel their order 

![Order page](https://i.imgur.com/FYrDwTq.png "Order page")  

Once the order is shipped the order status will change to delivery complete: 
![Order shipped](https://i.imgur.com/CLeyVyQ.png "Order shipped")  
###### if the user decides to cancel their order, the order will be deleted 

#### Track order:
The customer can track their order if they click on the link in the navbar [Track your order](./README.md#Track-order):

![Track order](https://i.imgur.com/HGqQtHA.png "Track order")  

#### Add Product:
if the user is a part of the *Sellers* group they can add a product by going to the [Add a product](./README.md#Add-Product) link in the navbar (It's only visible to those who are part of the *Sellers* group)

![Add Product](https://i.imgur.com/suPnwJ9.png "Add Product")  

#### Account settings:
Logged in users can change their account credentials by clicking on their account name on the to right in the navbar:

![Account settings](https://i.imgur.com/rcxl0lV.png "Account settings")  
![Account Password change](https://i.imgur.com/TdDMHyI.png "Account Password change")  
___

<br>

# Installation
<ul>
<li>Clone or download the repository</li>
<li>CD into the folder that contains manage.py (MYSITE)</li>
<li><code>pip install -r requirements.txt</code></li>
<li>Run <code>py manage.py runserver</code></li>
</ul>

# login credentials:
Username | Password | is-seller 
------------ | ------------- |---------
admin | admin | Yes

<br>
