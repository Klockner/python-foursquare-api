from geocode import getGeocodeLocation
import json
import httplib2

import sys
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)

foursquare_client_id = "UGXKPPJFGE5MNSK3JOESNOHWURXEKFYBSPGRSHZLH3VRETCR"
foursquare_client_secret = "QBP45JXKX4TZ0ADC4AGZ3UYUA0IS1H1HH3ISIUVTEGIHRPUW"

h = httplib2.Http()

def findARestaurant(mealType,location):
	geoLocation = str(getGeocodeLocation(location))
	prettyGeoLocation = geoLocation.strip('()').replace(' ', '')

	url = ('https://api.foursquare.com/v2/venues/search?'
	'client_id=%s&client_secret=%s&v=20170830&ll=%s&query=%s' %
	(foursquare_client_id, foursquare_client_secret, prettyGeoLocation, mealType))

	response, content = h.request(url, 'GET')
	result = json.loads(content)

	if result['response']['venues']:
		restaurant = result['response']['venues'][0]
		restaurant_name = restaurant['name']
		restaurant_address = restaurant['location']['formattedAddress']
		venue_id = restaurant['id']

		address = ''
		for i in restaurant_address:
			address += i + " "

		restaurant_address = address

		restaurantInfo = {'name':restaurant_name, 'address':restaurant_address, 'image':findPhoto(venue_id)}
		print('Restaurant Name: %s' % restaurantInfo['name'])
		print('Restaurant Address: %s' % restaurantInfo['address'])
		print('Image: %s \n' % restaurantInfo['image'])
		return restaurantInfo
	else:
		print('No Restaurants Found for %s' % location)
		return 'No Restaurants Found'

def findPhoto(venue_id):
	url = ('https://api.foursquare.com/v2//venues/%s/photos?client_id=%s&v=20170830&client_secret=%s' %
	(venue_id, foursquare_client_id, foursquare_client_secret))

	result = json.loads(h.request(url, 'GET')[1])

	if result['response']['photos']['items']:
		firstPic = result['response']['photos']['items'][0]
		prefix = firstPic['prefix']
		suffix = firstPic['suffix']
		imageURL = prefix + '300x300' + suffix
	else:
		imageURL = ('https://media.licdn.com/mpr/mpr/shrink_100_100/'
		'AAEAAQAAAAAAAApwAAAAJDI3MTIwYWM2LWY5MTYtNDA1OS1iMDZkLTlkNmE2MmNlYjRiYw.jpg')

	return imageURL


if __name__ == '__main__':
	findARestaurant("Pizza", "Tokyo, Japan")
	findARestaurant("Tacos", "Jakarta, Indonesia")
	findARestaurant("Tapas", "Maputo, Mozambique")
	findARestaurant("Falafel", "Cairo, Egypt")
	findARestaurant("Spaghetti", "New Delhi, India")
	findARestaurant("Cappuccino", "Geneva, Switzerland")
	findARestaurant("Sushi", "Los Angeles, California")
	findARestaurant("Steak", "La Paz, Bolivia")
	findARestaurant("Gyros", "Sydney Australia")
	findARestaurant("Pizza", "Curitiba Brazil")
