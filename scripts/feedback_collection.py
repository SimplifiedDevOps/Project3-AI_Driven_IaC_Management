# scripts/feedback_collection.py
import csv
import os
from datetime import datetime

# File path for storing feedback responses
feedback_file_path = "../feedback/feedback_responses.csv"

# Function to initialize the feedback file with headers
def initialize_feedback_file():
    if not os.path.exists(feedback_file_path):
        with open(feedback_file_path, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Timestamp", "DeploymentID", "Rating", "Comments"])

# Function to collect feedback from the operator
def collect_feedback(deployment_id):
    print(f"\nPlease provide feedback for Deployment ID: {deployment_id}")
    rating = input("Rate the deployment experience from 1 to 5 (1 = Poor, 5 = Excellent): ")
    comments = input("Additional comments (optional): ")

    # Save feedback to the CSV file
    with open(feedback_file_path, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now(), deployment_id, rating, comments])

    print("Thank you! Your feedback has been recorded.\n")

if __name__ == "__main__":
    # Initialize feedback file if it doesn't exist
    initialize_feedback_file()

    # Example deployment ID (could be dynamically set in real scenarios)
    deployment_id = "DEPLOY12345"

    # Collect feedback for the deployment
    collect_feedback(deployment_id)
