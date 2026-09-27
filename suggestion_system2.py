from collections import Counter


class Product:
    def __init__(self, item_id, name, category, price, rating=4.0, is_bestseller=False):
        self.item_id = item_id
        self.name = name
        self.category = category
        self.price = price
        self.rating = rating
        self.is_bestseller = is_bestseller


def get_amazon_products():
    return [
        Product('T1', 'Kindle Paperwhite', 'tech', 650.00, rating=4.7, is_bestseller=True),
        Product('T2', 'Apple iPad 9th Gen', 'tech', 1599.00, rating=4.6),
        Product('T3', 'Logitech MX Master 3S', 'tech', 499.00, rating=4.8, is_bestseller=True),
        Product('B1', 'Atomic Habits by James Clear', 'books', 55.00, rating=4.9, is_bestseller=True),
        Product('B2', 'Steve Jobs Biography', 'books', 65.00, rating=4.5),
        Product('B3', 'The Psychology of Money', 'books', 50.00, rating=4.7),
        Product('A1', 'Sony WH-1000XM5', 'audio', 1499.00, rating=4.8, is_bestseller=True),
        Product('A2', 'Amazon Echo Dot (5th Gen)', 'audio', 250.00, rating=4.4),
        Product('A3', 'Apple AirPods Pro 2', 'audio', 1099.00, rating=4.7),
        Product('F1', 'Fitbit Charge 6', 'fitness', 750.00, rating=4.3),
        Product('F2', 'Garmin Forerunner 255', 'fitness', 1650.00, rating=4.6),
        Product('F3', 'Manduka PRO Yoga Mat', 'fitness', 420.00, rating=4.5, is_bestseller=True),
    ]


# Categories that tend to get bought together (cross-sell pairs)
COMPLEMENTARY_CATEGORIES = {
    'tech': ['audio', 'fitness'],
    'audio': ['tech'],
    'fitness': ['tech', 'audio'],
    'books': [],
}


def calculate_recommendation_score(candidate, cart_products, cart_categories, cart_avg_price):
    """
    Scores how strongly `candidate` should be recommended given what's
    already in the cart. Higher = more relevant. 0-100ish scale.
    """
    score = 0.0

    # Factor 1: Same-category affinity (up to 40 pts) — weighted by how
    # many items of that category are already in the cart.
    same_cat_count = cart_categories.get(candidate.category, 0)
    score += min(same_cat_count * 20, 40)

    # Factor 2: Complementary-category cross-sell (up to 25 pts)
    for cat in cart_categories:
        if candidate.category in COMPLEMENTARY_CATEGORIES.get(cat, []):
            score += 12.5
    score = min(score, 40 + 25)

    # Factor 3: Price-band similarity to the cart's average item price
    # (up to 15 pts) — closer price = more likely to feel "in budget".
    if cart_avg_price:
        price_gap = abs(candidate.price - cart_avg_price)
        price_score = max(0, 15 - (price_gap / 100))
        score += price_score

    # Factor 4: Rating quality (up to 10 pts)
    score += (candidate.rating / 5.0) * 10

    # Factor 5: Bestseller nudge (5 pts)
    if candidate.is_bestseller:
        score += 5

    return round(min(score, 100), 1)


def get_recommendations(cart, all_products, top_n=3):
    """Returns up to top_n Product recommendations based on cart contents."""
    if not cart:
        # Cold start: no cart yet, just surface bestsellers.
        bestsellers = [p for p in all_products if p.is_bestseller]
        bestsellers.sort(key=lambda p: p.rating, reverse=True)
        return bestsellers[:top_n]

    cart_products = [item['product'] for item in cart]
    cart_ids = {p.item_id for p in cart_products}
    cart_categories = Counter(p.category for p in cart_products)
    cart_avg_price = sum(p.price for p in cart_products) / len(cart_products)

    scored = []
    for candidate in all_products:
        if candidate.item_id in cart_ids:
            continue
        score = calculate_recommendation_score(
            candidate, cart_products, cart_categories, cart_avg_price
        )
        scored.append((score, candidate))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [product for score, product in scored[:top_n] if score > 0]


def print_recommendations(cart, all_products):
    recs = get_recommendations(cart, all_products)
    if not recs:
        return
    header = "You might also like" if cart else "Trending right now"
    print(f"\n--- {header} ---")
    for p in recs:
        star = " (Bestseller)" if p.is_bestseller else ""
        print(f"  [{p.item_id}] {p.name:<30} : RM {p.price:.2f}  {'*' * round(p.rating)}{star}")
    print("-" * 45)


def display_welcome():
    print("=" * 50)
    print("      WELCOME TO AMAZON SHOPPING SYSTEM      ")
    print("=" * 50)


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
                print_recommendations(cart, amazon_products)
            else:
                print(">>> Invalid quantity! Must be a positive number.")
        else:
            print(">>> Invalid Product ID! Please try again.")


def process_checkout(cart):
    if not cart:
        print("\nYour cart is empty. Thank you for visiting Amazon!")
        return

    print("\n" + "=" * 50)
    print("          AMAZON PRIME CHECKOUT SYSTEM          ")
    print("=" * 50)

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
    print("\n" + "." * 50)
    print("                AMAZON OFFICIAL RECEIPT                ")
    print("." * 50)
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
    print_recommendations(cart, amazon_products)  # cold-start bestsellers

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

    if cart:
        print("\nBefore you go...")
        print_recommendations(cart, amazon_products)

    process_checkout(cart)


if __name__ == '__main__':
    main()