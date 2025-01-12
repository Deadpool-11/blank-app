import streamlit as st
import json
from pathlib import Path
import os
import shutil

# Path to store events and club priorities
EVENTS_FILE = "events.json"
PRIORITIES_FILE = "club_priorities.json"
IMAGE_DIR = "blank-app/images"

# Ensure the image directory exists
Path(IMAGE_DIR).mkdir(parents=True, exist_ok=True)

def load_events():
    """Load existing events from the JSON file."""
    if Path(EVENTS_FILE).exists():
        with open(EVENTS_FILE, "r") as file:
            return json.load(file)
    return []

def save_events(events):
    """Save events to the JSON file."""
    with open(EVENTS_FILE, "w") as file:
        json.dump(events, file, indent=4)

def save_priorities(priorities):
    """Save club priorities to the JSON file."""
    with open(PRIORITIES_FILE, "w") as file:
        json.dump(priorities, file, indent=4)

def delete_event_image(image_path):
    """Delete the event image if it exists."""
    if image_path and image_path != "" and Path(image_path).exists():
        os.remove(image_path)

# Load existing events
existing_events = load_events()

# Streamlit app layout
st.title("IIT Delhi Event Scheduler")
st.write("Paste the text of the Instagram post below:")

# Text area for user input
user_input = st.text_area("Instagram Post Text")
uploaded_image = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

# Button to add event
if st.button("Add Event"):
    if user_input:
        image_path = ""
        if uploaded_image:
            image_path = os.path.join(IMAGE_DIR, uploaded_image.name)
            with open(image_path, "wb") as f:
                shutil.copyfileobj(uploaded_image, f)
            st.write(f"Image saved at {image_path}")
        
        # Add new event to the list
        new_event = {"post_text": user_input, "image_path": image_path}
        existing_events.append(new_event)
        # Save updated events
        save_events(existing_events)
        st.success("Event added successfully!")
    else:
        st.error("Please enter some text.")

# Display existing events
st.write("### Existing Events")
for event in existing_events:
    if "post_text" in event:
        st.write(f"- {event['post_text']}")
    if "image_path" in event and event["image_path"] != "":
        st.image(event["image_path"])

# Button to delete an event
event_to_delete = st.selectbox("Select an event to delete", [event["post_text"] for event in existing_events if "post_text" in event])
if st.button("Delete Event"):
    for event in existing_events:
        if "post_text" in event and event["post_text"] == event_to_delete:
            delete_event_image(event["image_path"])
            existing_events.remove(event)
            save_events(existing_events)
            st.success("Event deleted successfully!")
            break
