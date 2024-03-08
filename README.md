# Brand Detection App

## Description

Project for DBMS class. The Brand Detection App leverages the power of vector databases to perform similarity searches across non-structured data. Our idea for implementation was to build a mobile app using Flutter akin to google lens searching in a specific dataset and backend with Qdrant+Django framework. Dataset used includes 120.000+ brands. (https://data.vision.ee.ethz.ch/sagea/lld/)

## Technologies Used

- **Frontend**: Flutter
- **Backend**: Python, Django REST Framework
- **Database**: Qdrant (with Docker)
- **Authentication**: Google Auth

## Requirements

- Docker (for Qdrant)
- Python 3.x
- Django
- Flutter

## Installation Instructions

### Qdrant Database Setup

1. Install Docker.
2. Copy the Qdrant image from web
3. Run the Qdrant container
4. Upload your dataset embeddings to your Qdrant collection as per the Qdrant documentation.
Check: https://qdrant.tech/documentation/quick-start/

### Backend Setup

1. Ensure Python 3.x and Django are installed.
2. Clone the repository and navigate to the backend directory.
3. Install required Python packages: 
pip install -r requirements.txt
4. Replace keys with your own for google auth and blip(if you wish to use hugging face api instead of local embedding)
5. Specify Docker container’s port.

## Usage Instructions

1. Open the app on your mobile device and log in with your Google account.
2. Upload a photo or select one from your gallery to identify brands.
3. View the top 10 closest brand matches, including details like the brand's name, origin country, and website.

## Working Demo

[Youtube Demo Video](https://youtube.com/shorts/mYDNG9ezYkA?si=oKN3qk-yP9nFdEgd)

## Extra featues made for the sake of it: 
1. Feedback
2. New entry request form
3. Xml-json import-export for recent searches
4. Slightly customised django admin panel for productivity
