Overview
The Cafe API is a Flask-based application that provides a set of endpoints to manage cafes, including creating, reading, updating, and deleting cafe records. The API interacts with a SQLite database to store and retrieve information about cafes, such as their name, location, amenities, and coffee prices.

Prerequisites
Before running the application, ensure that you have Python installed on your system. You will also need to install the required Python packages listed in the requirements.txt file.

Installation
Clone the repository:git clone <repository-url>
cd <repository-directory>

Install the required packages:

On Windows:
python -m pip install -r requirements.txt

On MacOS:
pip3 install -r requirements.txt

Run the application:python <script_name>.py
The application will start on http://127.0.0.1:5003/.

API Endpoints

1. Home
Endpoint: /
Method: GET
Description: Renders the homepage of the application.
Response: HTML page.

2. Get a Random Cafe
Endpoint: /random
Method: GET
Description: Returns a random cafe from the database.
Response: JSON object with details of a random cafe.
Example:{
  "cafe": {
    "id": 1,
    "name": "Cafe Name",
    "map_url": "https://...",
    "img_url": "https://...",
    "location": "Location Name",
    "seats": "20",
    "has_toilet": true,
    "has_wifi": true,
    "has_sockets": true,
    "can_take_calls": true,
    "coffee_price": "$2.5"
  }
}

3. Get All Cafes
Endpoint: /all
Method: GET
Description: Returns a list of all cafes sorted by their names.
Response: JSON array of cafes.
Example:
{
  "cafes": [
   {
      "id": 1,
      "name": "Cafe Name",
      "location": "Location Name",
      ...
    },
    ...
  ]
}

4. Search Cafes by Location
Endpoint: /search
Method: GET
Description: Searches for cafes based on location.
Query Parameter:
loc: The location to search for cafes.
Response: JSON array of cafes matching the location or an error message if none are found.
Example:
GET http://127.0.0.1:5003/search?loc=Peckham
Success Response:
{
  "cafes": [
    {
      "id": 1,
      "name": "Cafe in Peckham",
      ...
    }
  ]
}
Error Response:
{
  "error": {
    "Not Found": "Sorry, we don't have a cafe at that location."
  }
}
5. Add a New Cafe
Endpoint: /add
Method: POST
Description: Adds a new cafe to the database.
Query Parameters:
name: Name of the cafe.
map_url: URL to the cafe's location on a map.
img_url: Image URL of the cafe.
loc: Cafe location.
sockets: Availability of sockets (1 or 0).
toilet: Availability of toilets (1 or 0).
wifi: Availability of Wi-Fi (1 or 0).
calls: Availability of phone call space (1 or 0).
seats: Number of seats available.
coffee_price: Price of a cup of coffee.
Response: JSON object confirming the success of the operation.
Example:POST http://127.0.0.1:5003/add?name=Cafe_Name&map_url=https://map_url&img_url=https://img_url&loc=Location&sockets=1&toilet=1&wifi=1&calls=1&seats=20&coffee_price=$2.5
Success Response:{
  "response": {
    "success": "Successfully added the new cafe."
  }
}

6. Update Cafe Coffee Price
Endpoint: /update-price/<int:cafe_id>
Method: GET, PATCH
Description: Updates the price of coffee at a specific cafe.
Path Parameter:
cafe_id: The unique identifier of the cafe.
Query Parameter:
new_price: The new price of coffee at the cafe.
Response: JSON object confirming the success of the operation or an error message if the cafe is not found.
Example:PATCH http://127.0.0.1:5003/update-price/1?new_price=$3.0
Success Response:{
  "response": {
    "success": "Successfully updated the cafe coffee price"
  }
}
Error Response:{
  "error": {
    "error": "Sorry, a cafe with that id was not found in the database"
  }
}

7. Delete a Cafe (Report Closed)
Endpoint: /report-closed/<int:cafe_id>
Method: GET, DELETE
Description: Deletes a specific cafe from the database, typically when a cafe has closed down.
Path Parameter:
cafe_id: The unique identifier of the cafe.
Query Parameter:
api_key: The API key required to authorize the deletion.
Response: JSON object confirming the success of the deletion or an error message if the cafe is not found or the API key is incorrect.
Example:DELETE http://127.0.0.1:5003/report-closed/1?api_key=TopSecretAPIKey
Success Response:{
  "response": {
    "success": "Successfully deleted the cafe."
  }
}
Error Response:{
  "error": {
    "error": "Sorry, a cafe with that id was not found in the database."
  }
}

API Key Error Response:{
  "error": {
    "error": "Sorry, that's not allowed. Make sure you have the correct api_key."
  }
}
Running the Application
To run the application, simply execute the main script:python <script_name>.py
This will start the Flask development server on http://127.0.0.1:5003/.






