import requests
from bs4 import BeautifulSoup

def get_car_cover_listings():
    # Define the URL to search for "car cover" items on OLX India
    search_url = "https://www.olx.in/items/q-car-cover"

    # Use headers to mimic a real browser (avoids getting blocked)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    # Send HTTP GET request to OLX
    response = requests.get(search_url, headers=headers)

    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed to fetch listings. Status code: {response.status_code}")
        return

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all item containers (may need to be adjusted if OLX updates their layout)
    listings = soup.find_all('li', class_='EIR5N')

    # Create a list to store the results
    car_covers = []

    for listing in listings:
        # Try to extract title, price, and location
        title_tag = listing.find('span', class_='_2tW1I')
        price_tag = listing.find('span', class_='_89yzn')
        location_tag = listing.find('span', class_='tjgMj')

        # Store only if title and price are found
        if title_tag and price_tag:
            car_covers.append({
                'title': title_tag.get_text(strip=True),
                'price': price_tag.get_text(strip=True),
                'location': location_tag.get_text(strip=True) if location_tag else 'Location not available'
            })

    # Save the results to a text file
    with open("olx_car_covers.txt", "w", encoding="utf-8") as file:
        for index, item in enumerate(car_covers, start=1):
            file.write(f"{index}. {item['title']} - {item['price']} ({item['location']})\n")

    print(f"✅ Saved {len(car_covers)} car cover listings to 'olx_car_covers.txt'")

# Run the function
if __name__ == "__main__":
    get_car_cover_listings()
