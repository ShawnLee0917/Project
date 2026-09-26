def _calculate_unified_match_score(
    candidate_product,
    user_interests=None,
    user_preferences=None,
):
    """
    Unified matching algorithm for Amazon Product suggestions.
    (Preserved and adapted from the original matching system)
    """
    
    STOPWORDS = {
        'the', 'a', 'an', 'and', 'or', 'in', 'on', 'is', 'to', 'for', 'of',
        'with', 'that', 'this', 'it', 'as', 'are', 'was', 'be', 'from', 'at',
        'by', 'your', 'not', 'has', 'have', 'will', 'can', 'i', 'its'
    }
    
    # Adapted from PROGRAMMING_LANGUAGES to Amazon Categories
    PRODUCT_CATEGORIES = {
        'electronics': ['electronics', 'tech', 'device', 'gadget', 'smart'],
        'books': ['books', 'reading', 'paperback', 'hardcover', 'novel'],
        'audio': ['audio', 'music', 'sound', 'headphones', 'speaker'],
        'fitness': ['fitness', 'health', 'workout', 'wearable', 'sports'],
        'home': ['home', 'kitchen', 'appliance', 'decor']
    }
    
    # Adapted from interest_keywords to Product Features
    feature_keywords = {
        'reading': ['read', 'reader', 'e-reader', 'kindle', 'books', 'habit'],
        'music': ['audio', 'sound', 'noise-canceling', 'speaker', 'music', 'listen'],
        'smart home': ['alexa', 'smart devices', 'control', 'home', 'automation'],
        'productivity': ['habits', 'improve', 'framework', 'daily', 'focus'],
        'health': ['fitness', 'tracker', 'heart rate', 'gps', 'active', 'lifestyle'],
        'tech': ['electronics', 'wireless', 'display', 'battery', 'tech', 'gadget']
    }
    
    score = 0
    candidate_tags = (candidate_product.tags or '').lower()
    candidate_desc = (candidate_product.description or '').lower()
    candidate_target = (candidate_product.target_audience or '').lower()
    
    candidate_tags_set = set(t.strip().lower() for t in candidate_tags.split(',') if t.strip())
    candidate_desc_words = set(w for w in candidate_desc.split() if w not in STOPWORDS and len(w) > 2)
    
    if not user_interests:
        return 0
    
    user_interests_lower = [i.lower() for i in user_interests]
    
    # Factor 1: Category Matching (Preserved logic)
    category_match_bonus = 0
    for interest in user_interests_lower:
        if interest in PRODUCT_CATEGORIES:
            variants = PRODUCT_CATEGORIES[interest]
            for variant in variants:
                if variant in candidate_tags:
                    category_match_bonus += 12
        
        if interest in candidate_tags:
            category_match_bonus += 15
            
    category_match_bonus = min(category_match_bonus, 35)
    score += category_match_bonus
    
    # Factor 2: Feature Keyword Matching
    feature_keyword_hits = set()
    for interest in user_interests_lower:
        keywords = feature_keywords.get(interest, [])
        for keyword in keywords:
            if keyword in candidate_desc or keyword in candidate_tags:
                feature_keyword_hits.add(keyword)
    
    feature_match_score = min(len(feature_keyword_hits) * 2, 30)
    score += feature_match_score
    
    # Factor 3: Description Quality
    if candidate_desc:
        desc_match_score = min(len(candidate_desc_words) * 0.5, 10)
        score += desc_match_score
    
    # Factor 4: Preferences-to-Target Alignment
    if user_preferences and candidate_target:
        user_pref_lower = [p.lower() for p in user_preferences]
        pref_in_target = 0
        for pref in user_pref_lower:
            if pref in candidate_target:
                pref_in_target += 1
        
        pref_bonus = min(pref_in_target * 5, 15)
        score += pref_bonus
    
    # Precision filters
    if score < 30:
        score = max(score, 10)  
    score = min(100, max(0, score))
    
    return int(score)


class Product:
    def __init__(self, item_id, name, tags, description, target_audience, price):
        self.item_id = item_id
        self.name = name
        self.tags = tags
        self.description = description
        self.target_audience = target_audience
        self.price = price


def main():
    # ---------------------------------------------------------
    # PART 1: SUGGESTION SYSTEM (Adapted from Teammate's Code)
    # ---------------------------------------------------------
    amazon_products = [
        Product(1, 'Kindle Paperwhite', 'electronics, books, tech', 'Waterproof e-reader with high-resolution display.', 'reader, student', 650.00),
        Product(2, 'Amazon Echo Dot', 'electronics, audio, smart home', 'Smart speaker with Alexa for home automation.', 'tech lover, family', 250.00),
        Product(3, 'Atomic Habits by James Clear', 'books, productivity', 'A proven framework for building good habits.', 'reader, professional', 55.00),
        Product(4, 'Sony WH-1000XM5', 'electronics, audio, tech', 'Industry-leading noise-canceling headphones.', 'music lover, traveler', 1499.00),
        Product(5, 'Fitbit Charge 6', 'electronics, fitness, health', 'Advanced health tracker with built-in GPS.', 'athlete, fitness enthusiast', 750.00)
    ]

    print('\n' + '='*50)
    print('  WELCOME TO AMAZON AI PRODUCT MATCHMAKER  ')
    print('='*50)
    
    interests = input('What are you looking for? (e.g., tech, books, audio, fitness): ').strip()
    if not interests:
        print('Please enter at least one interest to get suggestions.')
        return

    preferences = input('Enter your user profile (e.g., reader, traveler, student): ').strip()
    
    user_interests = [i.strip() for i in interests.split(',') if i.strip()]
    user_preferences = [p.strip() for p in preferences.split(',') if p.strip()]

    suggestions = [
        (
            _calculate_unified_match_score(
                product,
                user_interests=user_interests,
                user_preferences=user_preferences,
            ),
            product,
        )
        for product in amazon_products
    ]
    # Sort by highest match score
    suggestions.sort(key=lambda item: item[0], reverse=True)

    print('\n--- TOP SUGGESTIONS FOR YOU ---')
    for score, product in suggestions:
        print(f"[{product.item_id}] {product.name} - Match: {score}% | Price: RM {product.price:.2f}")
        print(f"    Tags: {product.tags}")
        print(f"    Desc: {product.description}\n")