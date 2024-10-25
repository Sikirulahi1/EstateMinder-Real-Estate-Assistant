
# EstateMinder: Your Personal Real Estate Assistant

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Getting Started](#getting-started)
- [Scraping Data](#scraping-data)
- [Backend Development](#backend-development)
- [Frontend Development](#frontend-development)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Project Overview

EstateMinder is a powerful real estate assistant that helps users find their ideal homes based on their preferences. The application allows users to search for properties based on various criteria, including house type, price range, and specific queries. The app utilizes advanced AI technology to provide personalized recommendations, ensuring users have access to the best available listings.

## Demo Video

Check out the demo video to see EstateMinder in action!

[Link To The Video](https://youtu.be/tc8nUYXSTD8?si=NgHYATpnacB2YFnM) 

## Features

- **Property Search:** Users can select property types and price ranges to narrow down their search.
- **Intelligent Recommendations:** The app leverages Cohere AI for language understanding and Pinecone for efficient data retrieval and embeddings.
- **User-Friendly Interface:** Built with modern web technologies, the application offers an intuitive chat interface for seamless interactions.
- **Image Display:** Each property listing is accompanied by images to give users a better idea of the properties available.
- **Responsive Design:** The frontend is designed to be responsive, ensuring a smooth experience on both desktop and mobile devices.

## Technologies Used

- **Web Scraping:** [Scrapy](https://scrapy.org/) for collecting property data from the Zillow website.
- **AI and Embeddings:** [Cohere AI](https://cohere.ai/) for language modeling and [Pinecone](https://www.pinecone.io/) for managing embeddings and efficient search capabilities.
- **Backend Framework:** [Flask](https://flask.palletsprojects.com/) for creating the server-side application.
- **Frontend Technologies:** 
  - HTML for structure
  - CSS for styling
  - JavaScript for interactivity
- **Database:** Embedded property information in Pinecone for fast querying and retrieval.

## Getting Started

To run the EstateMinder application locally, follow these steps:

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/Sikirulahi1/EstateMinder-Real-Estate-Assistant.git
   cd EstateMinder-Real-Estate-Assistant
   ```

2. **Install Required Packages:**
   Ensure you have Python and pip installed. Then run:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Environment Variables:**
   Create a `.env` file in the root directory and add necessary API keys and configurations:
   ```bash
   COHERE_API_KEY=your_cohere_api_key
   PINECONE_API_KEY=your_pinecone_api_key
   ```

4. **Run the Application:**
   Start the Flask server:
   ```bash
   python app.py
   ```
   Navigate to `http://127.0.0.1:5000` in your web browser.

## Scraping Data

The property data is obtained from Zillow using the Scrapy framework. Scrapy enables efficient web scraping. The data collected includes:

- Price
- Home type
- Property Status
- Address
- Property Description
- Image URLs
- Special Features
- Agent Name
- Agent Licence No
- Real Estate Company
- Agent Contect

Ensure compliance with Zillow's terms of service while scraping data.

## Backend Development

The backend is built with Flask, handling user requests and processing data using Cohere and Pinecone. The following endpoints are available:

- **GET /query:** Processes user queries and retrieves relevant property listings from Pinecone.

## Frontend Development

The frontend is developed using HTML, CSS, and JavaScript. Key components include:

- **Chat Interface:** A dynamic chatbox where users can input their preferences.
- **House Type Selection:** Buttons for users to choose the type of property they are interested in.
- **Price Range Slider:** Sliders to select minimum and maximum prices for properties.

## Deployment

To deploy the application, you can use platforms like Heroku or Vercel. Follow their respective documentation for deployment instructions.

## Contributing

Contributions are welcome! If you have suggestions for improvements or want to report a bug, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Acknowledgments

- [Cohere AI](https://cohere.ai/) for providing advanced language modeling capabilities.
- [Pinecone](https://www.pinecone.io/) for enabling efficient vector-based data retrieval.
- [Scrapy](https://scrapy.org/) for the web scraping framework that made data collection easy.
