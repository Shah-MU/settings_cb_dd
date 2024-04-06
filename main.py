import streamlit as st
import firebase_admin
from firebase_admin import credentials, db

# Initialize Firebase app
if not firebase_admin._apps:
    # Initialize Firebase app
    cred = credentials.Certificate("sprint1-dataflow-test-firebase-adminsdk-j3s7u-7ad4f76319.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://sprint1-dataflow-test-default-rtdb.firebaseio.com/'
    })

# Firebase reference
ref = db.reference('pet_info')

def format_to_amazon_url(pet_type, pet_breed, age_group, dietary_restrictions):
    # Format pet information into a search query for Amazon
    query = "+".join([
        dietary_restrictions.lower().replace(" ", "+"),
        pet_breed.replace(" ", "+"),
        age_group.lower(),
        pet_type.lower()


    ])
    return f"https://www.amazon.ca/s?k={query}+food"

def main():
    st.title("Pet Information Form")

    # Fetch pet information from Firebase
    pet_info = ref.get()

    # Display pet information in editable text fields
    if pet_info:
        pet_name = st.text_input("Pet's Name:", value=pet_info.get('name', ''))
        pet_type = st.text_input("Pet Type:", value=pet_info.get('type', ''))
        pet_breed = st.text_input("Pet Breed:", value=pet_info.get('breed', ''))
        age_group = st.selectbox("Age group:", ["Baby", "Adult", "Senior"], index=["Baby", "Adult", "Senior"].index(pet_info.get('age_group', '')))
        dietary_restrictions = st.text_area("Dietary Restrictions:", value=pet_info.get('dietary_restrictions', ''))
    else:
        pet_name = st.text_input("Pet's Name:")
        pet_type = st.text_input("Pet Type:")
        pet_breed = st.text_input("Pet Breed:")
        age_group = st.selectbox("Age group:", ["Baby", "Adult", "Senior"])
        dietary_restrictions = st.text_area("Dietary Restrictions:")

    # Generate and display Amazon URL
    amazon_url = format_to_amazon_url(pet_type, pet_breed, age_group, dietary_restrictions)

    # Submit button
    if st.button("Submit"):
        # Update pet information in Firebase
        updated_pet_info = {
            'name': pet_name,
            'type': pet_type,
            'breed': pet_breed,
            'age_group': age_group,
            'dietary_restrictions': dietary_restrictions
        }
        ref.update(updated_pet_info)
        st.success("Pet information updated successfully!")

if __name__ == "__main__":
    main()
