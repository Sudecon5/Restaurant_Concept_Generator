import streamlit as st
import langchain_helper as helper
import time

st.set_page_config(
    page_title="Restaurant Name Generator",
    page_icon="🍽️",
    layout="wide"
)

st.title("🍽️ Restaurant Name Generator")
st.markdown("Generate unique restaurant names and menus tailored to your vision!")

# Sidebar inputs
st.sidebar.header("🎨 Customize Your Restaurant")
cuisine = st.sidebar.selectbox("Pick a cuisine", 
    ["Italian", "Chinese", "Mexican", "Indian", "American", "French", "Japanese", "Thai"])
style = st.sidebar.selectbox("Pick a style", 
    ["Casual", "Fine Dining", "Fast Food", "Cafe", "Buffet", "Food Truck"])
theme = st.sidebar.selectbox("Pick a theme", 
    ["Family-friendly", "Romantic", "Trendy", "Rustic", "Modern", "Vintage"])
location = st.sidebar.selectbox("Pick a location", 
    ["Downtown", "Suburb", "Rural", "Coastal", "Urban", "Shopping Mall"])
specialty = st.sidebar.selectbox("Pick a specialty", 
    ["Vegetarian", "Vegan", "Gluten-free", "Seafood", "Barbecue", "Fusion", "Traditional"])
price = st.sidebar.selectbox("Pick a price range", 
    ["Budget", "Mid-range", "Premium", "Luxury"])
feature = st.sidebar.selectbox("Pick a special feature", 
    ["Live Music", "Outdoor Seating", "Pet-friendly", "Takeout Only", "Delivery", "24/7"])

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    if st.button("🚀 Generate Restaurant Concept", type="primary", use_container_width=True):
        if not cuisine:
            st.error("❌ Please select a cuisine category.")
        else:
            # Create restaurant parameters
            restaurant_params = {
                'cuisine': cuisine,
                'style': style,
                'theme': theme,
                'location': location,
                'specialty': specialty,
                'price': price,
                'feature': feature
            }
            
            # Show loading spinner
            with st.spinner('🎭 Crafting your unique restaurant concept...'):
                try:
                    # Add artificial delay for better UX
                    time.sleep(1)
                    response = helper.generate_restaurant_concept(restaurant_params)
                    
                    # Display results
                    st.success("✨ Your restaurant concept is ready!")
                    
                    # Restaurant name section
                    st.markdown("---")
                    restaurant_name = response.get('restaurant_name', ['Unnamed Restaurant'])[0].strip()
                    st.markdown(f"## 🏪 **{restaurant_name}**")
                    
                    # Restaurant description
                    if 'description' in response:
                        description = response['description'].strip()
                        if description:
                            st.markdown(f"*{description}*")
                    
                    # Menu section
                    st.markdown("### 📋 **Menu Highlights**")
                    menu_items = response.get('menu_items', [])
                    
                    if menu_items:
                        # Filter out empty items and clean up
                        clean_items = [item.strip() for item in menu_items if item.strip()]
                        
                        if clean_items:
                            # Display menu in columns for better layout
                            menu_cols = st.columns(2)
                            for i, item in enumerate(clean_items[:10]):  # Limit to 10 items
                                with menu_cols[i % 2]:
                                    if item.startswith(('-', '•', '*')):
                                        st.markdown(f"🍽️ {item[1:].strip()}")
                                    else:
                                        st.markdown(f"🍽️ {item}")
                        else:
                            st.warning("No menu items generated. Try again!")
                    else:
                        st.warning("No menu items generated. Try again!")
                    
                    # Concept summary
                    st.markdown("---")
                    st.markdown("### 📊 **Concept Summary**")
                    concept_info = f"""
                    **Cuisine:** {cuisine} | **Style:** {style} | **Theme:** {theme}
                    
                    **Location:** {location} | **Specialty:** {specialty} | **Price Range:** {price}
                    
                    **Special Feature:** {feature}
                    """
                    st.markdown(concept_info)
                    
                except Exception as e:
                    st.error(f"❌ Error generating restaurant concept: {str(e)}")
                    st.info("💡 Please try again or check your connection to the language model.")

with col2:
    st.markdown("### 💡 **Tips**")
    st.info("""
    🎯 **Mix different options** to create unique concepts
    
    🎨 **Experiment** with various combinations
    
    🔄 **Try multiple times** for different creative results
    
    📝 **Note down** your favorite combinations
    """)

# Sidebar info
st.sidebar.markdown("---")
st.sidebar.header("ℹ️ About")
st.sidebar.info("""
This app generates unique restaurant names and menus based on your preferences using AI.

**Features:**
- Customizable restaurant parameters
- AI-generated names and menus
- Multiple cuisine options
- Professional concept summaries

**Developed by:** Sudipta Priyam Kakoty
""")

st.sidebar.markdown("---")
st.sidebar.markdown("### 🚀 **Quick Start**")
st.sidebar.markdown("""
1. Select your preferences
2. Click 'Generate Restaurant Concept'
3. Review your unique restaurant idea
4. Try different combinations!
""")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>🍽️ Restaurant Name Generator - Bringing culinary dreams to life!</div>", 
    unsafe_allow_html=True
)