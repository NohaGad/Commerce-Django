# Commerce Django

![Python](https://img.shields.io/badge/Python-3.9-blue)
![Django](https://img.shields.io/badge/Django-3.2-green)

Commerce Django is a web application built with Django, allowing users to create auction listings, place bids, manage watchlists, and explore various categories of listings.

## Features

- **Models:** The application includes models for auction listings, bids, and comments. Users can create listings with a title, description, starting bid, and optional image and category.
- **Create Listing:** Users can create new auction listings with details such as title, description, starting bid, and optional image and category.
- **Active Listings Page:** Users can view all currently active auction listings, displaying key information like title, description, current price, and photo (if available).
- **Listing Page:** Each listing has a dedicated page displaying all details, including current price. Signed-in users can add the listing to their watchlist, place bids, and close the auction if they are the creator.
- **Watchlist:** Signed-in users can manage their watchlist, viewing all listings they've added and accessing each listing's details.
- **Categories:** Users can explore listings by category, with each category displaying all active listings within it.
- **Django Admin Interface:** Administrators have full control over listings, comments, and bids through the Django admin interface.

## Installation

### Prerequisites

- Python 3.9 installed on your system.
- Django 3.2 installed.

### Instructions

1. Clone the repository:

   ```bash
   git clone https://github.com/NohaGad/Commerce-Django.git

2. Navigate to the project directory:

   ```bash
   cd Commerce-Django

3. Run migrations:

   ```bash
   python manage.py migrate

4. Start the development server:

   ```bash
   python manage.py runserver

5. Access the application at `http://127.0.0.1:8000/`.

## Usage
1. Create a new auction listing by providing the required details.
2. Explore active listings on the homepage and click on any listing to view its details.
3. Add listings to your watchlist to keep track of them.
4. Place bids on listings you're interested in and interact with comments made on listings.
5. Browse listings by category to find items of interest.

## Contributing
Contributions are welcome! If you find any issues or have suggestions for improvements, feel free to open an issue or submit a pull request.


