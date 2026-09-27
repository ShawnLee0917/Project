class Product:
    def __init__(self, item_id, name, category, price):
        self.item_id = item_id
        self.name = name
        self.category = category
        self.price = price

def get_amazon_products():
    return [
        Product('T1', 'Kindle Paperwhite', 'tech', 650.00),
        Product('T2', 'Apple iPad 9th Gen', 'tech', 1599.00),
        Product('T3', 'Logitech MX Master 3S', 'tech', 499.00),
        Product('B1', 'Atomic Habits by James Clear', 'books', 55.00),
        Product('B2', 'Steve Jobs Biography', 'books', 65.00),
        Product('B3', 'The Psychology of Money', 'books', 50.00),
        Product('A1', 'Sony WH-1000XM5', 'audio', 1499.00),
        Product('A2', 'Amazon Echo Dot (5th Gen)', 'audio', 250.00),
        Product('A3', 'Apple AirPods Pro 2', 'audio', 1099.00),
        Product('F1', 'Fitbit Charge 6', 'fitness', 750.00),
        Product('F2', 'Garmin Forerunner 255', 'fitness', 1650.00),
        Product('F3', 'Manduka PRO Yoga Mat', 'fitness', 420.00)
    ]

def display_welcome():
    print("="*50)
    print("      WELCOME TO AMAZON SHOPPING SYSTEM      ")
    print("="*50)

def select_category(valid_categories):
    print("\n--- CATEGORIES ---")
    print(f"Available categories: {', '.join(valid_categories)}")
    return input("What are you looking for? (or type 'checkout' to pay): ").strip().lower()

def browse_and_add_products(category_choice, amazon_products, cart):
    while True:
        print(f"\n--- {category_choice.upper()} PRODUCTS ---")
        category_items = [p for p in amazon_products if p.category == category_choice]
        for item in category_items:
            print(f"[{item.item_id}] {item.name:<30} : RM {item.price:.2f}")
            
        print("-" * 45)
        item_choice = input("Enter Product ID to buy, 'back' to change category, or 'checkout': ").strip().upper()
        
        if item_choice in ['CHECKOUT', 'BACK']:
            return item_choice
            
        selected_item = next((p for p in category_items if p.item_id == item_choice), None)
        if selected_item:
            qty_input = input(f"How many '{selected_item.name}' would you like? ")
            if qty_input.isdigit() and int(qty_input) > 0:
                qty = int(qty_input)
                cart.append({'product': selected_item, 'qty': qty})
                print(f">>> Success! Added {qty}x {selected_item.name} to cart.")
            else:
                print(">>> Invalid quantity! Must be a positive number.")
        else:
            print(">>> Invalid Product ID! Please try again.")

def process_checkout(cart):
    if not cart:
        print("\nYour cart is empty. Thank you for visiting Amazon!")
        return

    print("\n" + "="*50)
    print("          AMAZON PRIME CHECKOUT SYSTEM          ")
    print("="*50)
    
    is_prime = input("Are you an Amazon Prime Member? (Y/N): ").strip().upper()
    subtotal = sum(item['product'].price * item['qty'] for item in cart)
    
    if is_prime == 'Y':
        print("\n[Prime Member] Applying Free Premium Shipping & 10% Discount...")
        shipping_fee = 0.0
        discount = subtotal * 0.10
    elif subtotal > 200:
        print("\n[Standard Checkout] Subtotal over RM 200. Applying Free Shipping...")
        shipping_fee = 0.0
        discount = 0.0
    else:
        print("\n[Standard Checkout] Adding standard RM 15 shipping fee...")
        shipping_fee = 15.00
        discount = 0.0
        
    final_total = (subtotal - discount) + shipping_fee
    print_receipt(cart, subtotal, discount, shipping_fee, final_total)

def print_receipt(cart, subtotal, discount, shipping_fee, final_total):
    print("\n" + "."*50)
    print("                AMAZON OFFICIAL RECEIPT                ")
    print("."*50)
    for item in cart:
        p = item['product']
        q = item['qty']
        line_total = p.price * q
        print(f"{q}x {p.name[:25]:<25} : RM {line_total:8.2f}")
    
    print("-" * 50)
    print(f"Subtotal                       : RM {subtotal:8.2f}")
    print(f"Prime Discount                 :-RM {discount:8.2f}")
    print(f"Shipping Fee                   :+RM {shipping_fee:8.2f}")
    print("=" * 50)
    print(f"TOTAL AMOUNT DUE               : RM {final_total:8.2f}")
    print("=" * 50)
    print("Thank you for shopping with us!")

def main():
    amazon_products = get_amazon_products()
    valid_categories = ['tech', 'books', 'audio', 'fitness']
    cart = []

    display_welcome()

    while True:
        category_choice = select_category(valid_categories)
        if category_choice == 'checkout':
            break
        if category_choice not in valid_categories:
            print(">>> Invalid category! Please choose from the list above.")
            continue
            
        action = browse_and_add_products(category_choice, amazon_products, cart)
        if action == 'CHECKOUT':
            break

    process_checkout(cart)

if __name__ == '__main__':
    main()