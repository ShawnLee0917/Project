class Product:
    def __init__(self, item_id, name, category, price):
        self.item_id = item_id
        self.name = name
        self.category = category
        self.price = price

def main():
    # 1. EXPANDED AMAZON PRODUCT DATABASE
    amazon_products = [
        # Tech
        Product('T1', 'Kindle Paperwhite', 'tech', 650.00),
        Product('T2', 'Apple iPad 9th Gen', 'tech', 1599.00),
        Product('T3', 'Logitech MX Master 3S', 'tech', 499.00),
        # Books
        Product('B1', 'Atomic Habits by James Clear', 'books', 55.00),
        Product('B2', 'Steve Jobs Biography', 'books', 65.00),
        Product('B3', 'The Psychology of Money', 'books', 50.00),
        # Audio
        Product('A1', 'Sony WH-1000XM5', 'audio', 1499.00),
        Product('A2', 'Amazon Echo Dot (5th Gen)', 'audio', 250.00),
        Product('A3', 'Apple AirPods Pro 2', 'audio', 1099.00),
        # Fitness
        Product('F1', 'Fitbit Charge 6', 'fitness', 750.00),
        Product('F2', 'Garmin Forerunner 255', 'fitness', 1650.00),
        Product('F3', 'Manduka PRO Yoga Mat', 'fitness', 420.00)
    ]

    valid_categories = ['tech', 'books', 'audio', 'fitness']
    cart = []

    print("="*50)
    print("      WELCOME TO AMAZON SHOPPING SYSTEM      ")
    print("="*50)


# 2. MAIN SHOPPING LOOP
    while True:
        print("\n--- CATEGORIES ---")
        print("Available categories: tech, books, audio, fitness")
        
        # Keep asking until a valid category is entered
        category_choice = input("What are you looking for? (or type 'checkout' to pay): ").strip().lower()
        
        if category_choice == 'checkout':
            break
            
        if category_choice not in valid_categories:
            print(">>> Invalid category! Please choose from the list above.")
            continue

if __name__ == '__main__':
    main()