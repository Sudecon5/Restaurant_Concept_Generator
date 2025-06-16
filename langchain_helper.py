import streamlit as st
import os
import logging
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import SequentialChain, LLMChain

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set the Groq API key as an environment variable
groqapi_key = st.secrets["groqapi_key"]
os.environ["groqapi_key"] = groqapi_key

# Initialize LLM with error handling
def initialize_llm():
    try:
        llm = Ollama(
            model="mistral",
            base_url='http://localhost:11434',
            temperature=0.7,
            top_p=0.9,
            num_predict=500
        )
        return llm
    except Exception as e:
        logger.error(f"Failed to initialize LLM: {e}")
        raise Exception("Could not connect to language model. Please ensure Ollama is running.")

llm = initialize_llm()

def generate_restaurant_concept(params):
    """
    Generate a complete restaurant concept including name, description, and menu items.
    
    Args:
        params (dict): Dictionary containing restaurant parameters
        
    Returns:
        dict: Contains restaurant_name, description, and menu_items
    """
    try:
        # Extract parameters
        cuisine = params.get('cuisine', 'Italian')
        style = params.get('style', 'Casual')
        theme = params.get('theme', 'Modern')
        location = params.get('location', 'Downtown')
        specialty = params.get('specialty', 'Traditional')
        price = params.get('price', 'Mid-range')
        feature = params.get('feature', 'Dine-in')
        
        # Chain 1: Restaurant Name Generation
        name_prompt = PromptTemplate(
            input_variables=['cuisine', 'style', 'theme', 'location', 'specialty', 'price'],
            template="""Create a creative and memorable restaurant name for a {style} {cuisine} restaurant.

Restaurant Details:
- Cuisine: {cuisine}
- Style: {style}
- Theme: {theme}
- Location: {location}
- Specialty: {specialty}
- Price Range: {price}

The name should be:
- Catchy and memorable
- Appropriate for the cuisine and style
- Suitable for {theme} theme
- Professional yet creative

Provide only the restaurant name, nothing else."""
        )
        
        name_chain = LLMChain(
            llm=llm, 
            prompt=name_prompt, 
            output_key='restaurant_name'
        )
        
        # Chain 2: Restaurant Description Generation
        description_prompt = PromptTemplate(
            input_variables=['restaurant_name', 'cuisine', 'style', 'theme', 'specialty'],
            template="""Create a brief, appealing description for {restaurant_name}, a {style} {cuisine} restaurant.

Restaurant Details:
- Name: {restaurant_name}
- Cuisine: {cuisine}
- Style: {style}
- Theme: {theme}
- Specialty: {specialty}

Write a 2-3 sentence description that captures the restaurant's essence and would attract customers. Focus on the atmosphere, cuisine quality, and unique selling points."""
        )
        
        description_chain = LLMChain(
            llm=llm,
            prompt=description_prompt,
            output_key='description'
        )
        
        # Chain 3: Menu Items Generation
        menu_prompt = PromptTemplate(
            input_variables=['restaurant_name', 'cuisine', 'style', 'specialty', 'price'],
            template="""Create an appealing menu for {restaurant_name}, a {style} {cuisine} restaurant.

Restaurant Details:
- Name: {restaurant_name}
- Cuisine: {cuisine}
- Style: {style}
- Specialty: {specialty}
- Price Range: {price}

Generate 8-12 menu items that:
- Reflect the {cuisine} cuisine authentically
- Match the {style} style and {price} price range
- Include {specialty} options where appropriate
- Are creative but recognizable
- Include a mix of appetizers, main courses, and desserts

Format: List each item on a new line with just the dish name (no prices or descriptions).
Example format:
Truffle Mushroom Risotto
Grilled Salmon with Herbs
Chocolate Lava Cake"""
        )
        
        menu_chain = LLMChain(
            llm=llm,
            prompt=menu_prompt,
            output_key='menu_items'
        )
        
        # Create Sequential Chain
        sequential_chain = SequentialChain(
            chains=[name_chain, description_chain, menu_chain],
            input_variables=['cuisine', 'style', 'theme', 'location', 'specialty', 'price'],
            output_variables=['restaurant_name', 'description', 'menu_items'],
            verbose=False  # Set to True for debugging
        )
        
        # Execute the chain
        logger.info(f"Generating restaurant concept for {cuisine} cuisine")
        response = sequential_chain.invoke(params)
        
        # Process and clean the response
        processed_response = process_response(response)
        
        logger.info("Restaurant concept generated successfully")
        return processed_response
        
    except Exception as e:
        logger.error(f"Error in generate_restaurant_concept: {e}")
        return create_fallback_response(params)

def process_response(response):
    """
    Clean and process the LLM response.
    
    Args:
        response (dict): Raw response from LLM chain
        
    Returns:
        dict: Processed response
    """
    try:
        # Clean restaurant name
        restaurant_name = response.get('restaurant_name', 'Unnamed Restaurant')
        if isinstance(restaurant_name, str):
            restaurant_name = [line.strip() for line in restaurant_name.split('\n') if line.strip()]
        
        # Clean description
        description = response.get('description', '')
        if isinstance(description, str):
            description = description.strip()
        
        # Clean menu items
        menu_items = response.get('menu_items', '')
        if isinstance(menu_items, str):
            menu_items = [
                item.strip() 
                for item in menu_items.split('\n') 
                if item.strip() and not item.strip().startswith(('Menu', 'Items:', '---'))
            ]
        
        return {
            'restaurant_name': restaurant_name if restaurant_name else ['Unnamed Restaurant'],
            'description': description,
            'menu_items': menu_items if menu_items else ['No menu items available']
        }
        
    except Exception as e:
        logger.error(f"Error processing response: {e}")
        return {
            'restaurant_name': ['Processing Error'],
            'description': 'Unable to process restaurant description',
            'menu_items': ['Unable to process menu items']
        }

def create_fallback_response(params):
    """
    Create a fallback response when LLM fails.
    
    Args:
        params (dict): Restaurant parameters
        
    Returns:
        dict: Fallback response
    """
    cuisine = params.get('cuisine', 'Fusion')
    style = params.get('style', 'Casual')
    
    fallback_names = {
        'Italian': ['Bella Vista', 'La Famiglia', 'Nonna\'s Kitchen'],
        'Chinese': ['Golden Dragon', 'Jade Garden', 'Lucky Bamboo'],
        'Mexican': ['Casa Fiesta', 'El Corazón', 'Aztec Grill'],
        'Indian': ['Spice Route', 'Maharaja Palace', 'Curry Corner'],
        'American': ['Liberty Grill', 'Stars & Stripes', 'All-American Diner'],
        'French': ['Le Petit Bistro', 'Café Paris', 'Bonne Appetite']
    }
    
    fallback_menus = {
        'Italian': ['Margherita Pizza', 'Fettuccine Alfredo', 'Chicken Parmigiana', 'Tiramisu'],
        'Chinese': ['Sweet & Sour Pork', 'Kung Pao Chicken', 'Fried Rice', 'Spring Rolls'],
        'Mexican': ['Tacos al Pastor', 'Chicken Quesadilla', 'Beef Burrito', 'Churros'],
        'Indian': ['Butter Chicken', 'Biryani', 'Naan Bread', 'Gulab Jamun'],
        'American': ['Classic Burger', 'BBQ Ribs', 'Mac and Cheese', 'Apple Pie'],
        'French': ['Coq au Vin', 'French Onion Soup', 'Ratatouille', 'Crème Brûlée']
    }
    
    name = fallback_names.get(cuisine, ['The Local Eatery'])[0]
    menu = fallback_menus.get(cuisine, ['House Special', 'Chef\'s Choice', 'Daily Special'])
    
    return {
        'restaurant_name': [f"{name} ({style})"],
        'description': f"A charming {style.lower()} {cuisine.lower()} restaurant serving authentic flavors in a welcoming atmosphere.",
        'menu_items': menu
    }

# Legacy function for backward compatibility
def generate_name_and_items(cuisine):
    """
    Legacy function - maintained for backward compatibility.
    Use generate_restaurant_concept() for new implementations.
    """
    params = {'cuisine': cuisine}
    response = generate_restaurant_concept(params)
    
    return {
        "restaurant_name": response['restaurant_name'],
        "menu_items": response['menu_items'],
        "items": response['menu_items']  # Keep for legacy support
    }

# Test function
def test_generation():
    """Test function to verify the generator works."""
    test_params = {
        'cuisine': 'Italian',
        'style': 'Fine Dining',
        'theme': 'Romantic',
        'location': 'Downtown',
        'specialty': 'Traditional',
        'price': 'Premium',
        'feature': 'Live Music'
    }
    
    result = generate_restaurant_concept(test_params)
    print("Test Results:")
    print(f"Restaurant Name: {result['restaurant_name']}")
    print(f"Description: {result['description']}")
    print("Menu Items:")
    for item in result['menu_items']:
        print(f"- {item}")

if __name__ == "__main__":
    test_generation()
