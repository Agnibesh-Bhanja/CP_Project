import streamlit as st
import json
import os

# Inventory with images!
inventory = [
    {"Item_id": 1, "Item_name": "T-shirt", "No_of_units": 50, "Price": 500, "Image": "D:/Projects/Images/T_shirt.jpg"},
    {"Item_id": 2, "Item_name": "Jeans", "No_of_units": 30, "Price": 1200, "Image": "D:/Projects/Images/Jeans.jpg"},
    {"Item_id": 3, "Item_name": "Jacket", "No_of_units": 20, "Price": 2500, "Image": "D:/Projects/Images/Jacket.jpg"},
    {"Item_id": 4, "Item_name": "Cap", "No_of_units": 40, "Price": 800, "Image": "D:/Projects/Images/Cap.jpg"},
    {"Item_id": 5, "Item_name": "Shorts", "No_of_units": 25, "Price": 600, "Image": "D:/Projects/Images/Shorts.jpg"},
    {"Item_id": 6, "Item_name": "Coat", "No_of_units": 15, "Price": 2000, "Image": "D:/Projects/Images/Coat.jpg"},
    {"Item_id": 7, "Item_name": "Skirt", "No_of_units": 30, "Price": 1500, "Image": "D:/Projects/Images/Skirt.jpg"},
    {"Item_id": 8, "Item_name": "Sweater", "No_of_units": 20, "Price": 1800, "Image": "D:/Projects/Images/Sweater.jpg"},
    {"Item_id": 9, "Item_name": "Sneakers", "No_of_units": 60, "Price": 300, "Image": "D:/Projects/Images/Sneakers.jpg"},
]

# Extra info used as streamlit is stateless function so we Initialize session state variables if not already initialized!
if "inventory" not in st.session_state:
    st.session_state.inventory = inventory
if "customer_cart" not in st.session_state:
    st.session_state.customer_cart = []

# Function to register unique customer IDs and names!
def register_customer(name):
    if os.path.exists("cust_name.json"):
        with open("cust_name.json", "r") as file:
            data = file.readlines()
            if data:
                for entry in data:
                    cust_data = json.loads(entry.strip())
                    if name == cust_data["name"]:
                        st.success(f"Welcome back, {name}! Your ID is {cust_data['id']}.")
                        return cust_data["id"]
                last_id = json.loads(data[-1].strip())["id"]
                cust_id = int(last_id) + 1
            else:
                cust_id = 1
    else:
        cust_id = 1

    with open("cust_name.json", "a") as file:
        json.dump({"name": name, "id": cust_id}, file)
        file.write("\n")
    st.success(f"Welcome, {name}! Your ID is {cust_id}.")
    return cust_id

# Function to add items to the customer cart!
def add_to_cart(cust_id, cust_name, cart_items):
    # Update the inventory and add items to the customer cart!
    for item_id, quantity in cart_items.items():
        for item in st.session_state.inventory:
            if item["Item_id"] == item_id and quantity > 0:
                if item["No_of_units"] >= quantity:
                    # Update the inventory in session state!
                    item["No_of_units"] -= quantity
                    # Add to customer cart in session state!
                    st.session_state.customer_cart.append({
                        "Cust_id": cust_id,
                        "Cust_name": cust_name,
                        "Item_id": item_id,
                        "Item_name": item["Item_name"],
                        "Quantity": quantity,
                        "Price": item["Price"],
                        "Total": item["Price"] * quantity,
                        "Order_status": "Pending",  # Order status added here!
                        "Image": item["Image"],
                    })
                else:
                    st.error(f"Not enough stock for {item['Item_name']}!")
    st.success("Items added to cart successfully!")

# Function to calculate the total order amount!
def calculate_total():
    return sum(item["Total"] for item in st.session_state.customer_cart)

# Streamlit App!
st.title("\U0001F600 AMAGON")
st.markdown("""
    <style>
    .stTabs [data-baseweb="tab"] {
        font-size: 50px;
        font-family: cursive;
        font-weight: bold;
        color: #070808;
        background-color: #5eed0c;
        border-radius: 15px;
        padding: 10px;
        margin: 0 36px;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #3CB371;
        color: #FFFFFF;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background-color: #228B22;
        color: #FFFFFF;
        border: 2px solid #FFFFFF;
    }
    </style>
    """, unsafe_allow_html=True)
# Navigation bar!
tab1, tab2, tab3, tab4 = st.tabs(["Home", "Shop", "Inventory", "Customer Cart"])

# Tab 1: Home!
with tab1:
    st.header("Welcome to AMAGON \U0001F600")
    st.subheader("Register or login here to Shop")
    with st.form("register_form", clear_on_submit=True):
        name = st.text_input("Enter your name:")
        submitted = st.form_submit_button("Register")
        if submitted and name.strip():
            cust_id = register_customer(name)
            # Save customer id and name to session state!
            st.session_state.cust_id = cust_id
            st.session_state.cust_name = name
        elif submitted:
            st.error("Please enter a valid name.")

# Tab 2: Shop!
with tab2:
    st.header("Shop now \U0001F60E")
    
    # Ensure that cust_id is available at current working position!
    if "cust_id" not in st.session_state:
        # Usage of error box feature for doubt message!
        st.error("Please register to proceed with shopping at AMAGON.")
    else:
        # Usage of selectbox streamlit feature for appearance of sorting options!
        # Used Unicode streamlit features for icon
        sort= st.selectbox('Sort by Price \u2193\u2191',
        ('Select','low to high \u2193','High to low \u2191'))
        if sort=='Select':
        # sorted the elements in item_id order!
            st.session_state.inventory = sorted(st.session_state.inventory, key=lambda x: x["Item_id"])
        elif sort=='low to high \u2193':
        # sorted the elements in ascending order by using direct sorting function!
            st.session_state.inventory = sorted(st.session_state.inventory, key=lambda x: x["Price"])
        else:
        # sorted the elements in descending order by using direct sorting function!
            st.session_state.inventory = sorted(st.session_state.inventory, key=lambda x: x["Price"], reverse=True)

        cust_id = st.session_state.cust_id
        cust_name = st.session_state.cust_name
        # cart_items dictionary is empty now and iterating it item by item and extracting items from inventory!
        cart_items = {}
        for item in st.session_state.inventory:
            #columns are for separation and 3,6,2 are width of coloumns!
            col1, col2, col3, col4 = st.columns([3, 2.5, 3, 2])
            #streamlit feature to extract image and image width!
            with col1:
                st.image(item["Image"], width=100)
            #streamlit feature to extract and print it from session_state_inventory for both item name and price!
            with col2:
                st.write(f"**{item['Item_name']}**")
            with col3:
                st.write(f"Price: ₹{item['Price']}")
            #streamlit feature to take input from number_input style, step=1 is for rate in increase of one time button press, key for unique identity for an item!
            with col4:
                quantity = st.number_input(
                    f"Quantity ({item['Item_name']})", min_value=0, max_value=item["No_of_units"], step=1, key=f"qty_{item['Item_id']}")
                cart_items[item["Item_id"]] = quantity
        # Here add to cart function will work!
        if st.button("Add to Cart"):
            add_to_cart(cust_id, cust_name, cart_items)

# Tab 3: Inventory
with tab3:
    st.header("Inventory")
    inventory_skip = [{
        "Item (id)": item["Item_id"],
        "Item (name)": item["Item_name"],
        "Stock": item["No_of_units"],
        "Price": item["Price"]}for item in st.session_state.inventory]
    st.table(inventory_skip)
    new_item_id= st.text_input("Enter item id:")
    new_item_name= st.text_input("Enter item name:")
    new_stock_quantity= st.text_input("Enter stock quantity:")
    new_price= st.text_input("Enter price:")
    def new_item(item_id, item_name, stock_quantity, price):
        if any(item['Item_id'] == item_id for item in st.session_state.inventory):
                st.error(f"Item ID {item_id} already exists in inventory!")
                return
        st.session_state.inventory.append({
                "Item_id": item_id,
                "Item_name": item_name,
                "No_of_units": stock_quantity,
                "Price": price,})
        st.success(f"Item '{item_name}' added successfully to the inventory!")
    if st.button("Add Item"):
        try:
            new_item_id = int(new_item_id)
            new_stock_quantity = int(new_stock_quantity)
            new_price = int(new_price)
            new_item_id and new_item_name and new_stock_quantity and new_price
            new_item(new_item_id, new_item_name, new_stock_quantity, new_price)
            inventory_change = [{
            "Item (id)": item["Item_id"],
            "Item (name)": item["Item_name"],
            "Stock": item["No_of_units"],
            "Price": item["Price"]}for item in st.session_state.inventory]
            st.table(inventory_change)
        except:
            st.error("Please enter valid numeric values for Item ID, Stock Quantity, and Price.")
    else:
         st.error("Fill details to add item!")
# Tab 4: Customer Cart
with tab4:
    st.header("Customer Cart")
    if "customer_cart" in st.session_state and st.session_state.customer_cart:
        for item in st.session_state.customer_cart:
            col1, col2, col3 = st.columns([2, 3, 3])
            with col1:
                st.image(item["Image"], width=100)
            with col2:
                st.write(f"**{item['Item_name']}**")
            with col3:
                st.write(f"Quantity: {item['Quantity']} | Total: ₹{item['Total']} | Customer ID: {item['Cust_id']} | Customer Name: {item['Cust_name']} | Order Status: {item['Order_status']}")
                
        st.subheader(f"Total Amount: ₹{calculate_total()}")
        if st.button("Place Order"):
            for item in st.session_state.customer_cart:
                item["Order_status"] = "Order placed"
            st.success(f"Congratulations {item['Cust_name']}! Your order is successful. Total amount to pay: ₹{calculate_total()}")        
    else:
        st.error("Your cart is empty right now.")
