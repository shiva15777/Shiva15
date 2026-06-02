import requests
import logging
from datetime import datetime
import json
from weather_config import WEATHER_API_KEY, WEATHER_API_URL

logger = logging.getLogger(__name__)

class WeatherAPI:
    """Handle weather API calls"""
    
    def __init__(self, api_key=WEATHER_API_KEY):
        self.api_key = api_key
        self.base_url = WEATHER_API_URL
    
    def get_current_weather(self, city):
        """Get current weather for a city"""
        try:
            url = f"{self.base_url}/weather"
            params = {
                'q': city,
                'appid': self.api_key,
                'units': 'metric'
            }
            
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            logger.info(f"Weather fetched for {city}")
            
            return {
                'success': True,
                'data': self._parse_current_weather(data)
            }
            
        except requests.exceptions.ConnectionError:
            logger.error("Connection error")
            return {'success': False, 'error': 'Connection error'}
        except requests.exceptions.Timeout:
            logger.error("Request timeout")
            return {'success': False, 'error': 'Request timeout'}
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error: {e}")
            if response.status_code == 404:
                return {'success': False, 'error': 'City not found'}
            return {'success': False, 'error': 'API error'}
        except Exception as e:
            logger.error(f"Error fetching weather: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def get_forecast(self, city, days=5):
        """Get weather forecast for a city"""
        try:
            url = f"{self.base_url}/forecast"
            params = {
                'q': city,
                'appid': self.api_key,
                'units': 'metric',
                'cnt': days * 8
            }
            
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            logger.info(f"Forecast fetched for {city}")
            
            return {
                'success': True,
                'data': self._parse_forecast(data)
            }
            
        except Exception as e:
            logger.error(f"Error fetching forecast: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def get_weather_by_coordinates(self, lat, lon):
        """Get weather by latitude and longitude"""
        try:
            url = f"{self.base_url}/weather"
            params = {
                'lat': lat,
                'lon': lon,
                'appid': self.api_key,
                'units': 'metric'
            }
            
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            logger.info(f"Weather fetched for coordinates {lat}, {lon}")
            
            return {
                'success': True,
                'data': self._parse_current_weather(data)
            }
            
        except Exception as e:
            logger.error(f"Error fetching weather by coordinates: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def search_cities(self, query):
        """Search for cities"""
        try:
            url = f"{self.base_url}/find"
            params = {
                'q': query,
                'appid': self.api_key,
                'type': 'like',
                'cnt': 10
            }
            
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            cities = []
            
            for city in data.get('list', []):
                cities.append({
                    'name': city['name'],
                    'country': city.get('sys', {}).get('country', ''),
                    'lat': city['coord']['lat'],
                    'lon': city['coord']['lon']
                })
            
            logger.info(f"Cities searched: {query}")
            return {'success': True, 'cities': cities}
            
        except Exception as e:
            logger.error(f"Error searching cities: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def _parse_current_weather(data):
        """Parse current weather data"""
        try:
            return {
                'city': data.get('name'),
                'country': data.get('sys', {}).get('country'),
                'temperature': data.get('main', {}).get('temp'),
                'feels_like': data.get('main', {}).get('feels_like'),
                'temp_min': data.get('main', {}).get('temp_min'),
                'temp_max': data.get('main', {}).get('temp_max'),
                'humidity': data.get('main', {}).get('humidity'),
                'pressure': data.get('main', {}).get('pressure'),
                'description': data.get('weather', [{}])[0].get('description'),
                'main': data.get('weather', [{}])[0].get('main'),
                'icon': data.get('weather', [{}])[0].get('icon'),
                'wind_speed': data.get('wind', {}).get('speed'),
                'wind_deg': data.get('wind', {}).get('deg'),
                'clouds': data.get('clouds', {}).get('all'),
                'visibility': data.get('visibility'),
                'sunrise': data.get('sys', {}).get('sunrise'),
                'sunset': data.get('sys', {}).get('sunset'),
                'timezone': data.get('timezone'),
                'coordinates': {
                    'lat': data.get('coord', {}).get('lat'),
                    'lon': data.get('coord', {}).get('lon')
                }
            }
        except Exception as e:
            logger.error(f"Error parsing weather data: {str(e)}")
            return {}
    
    @staticmethod
    def _parse_forecast(data):
        """Parse forecast data"""
        try:
            forecast_list = []
            
            for item in data.get('list', []):
                forecast_list.append({
                    'date': item.get('dt'),
                    'datetime_str': datetime.fromtimestamp(item.get('dt')).strftime('%Y-%m-%d %H:%M'),
                    'temperature': item.get('main', {}).get('temp'),
                    'feels_like': item.get('main', {}).get('feels_like'),
                    'temp_min': item.get('main', {}).get('temp_min'),
                    'temp_max': item.get('main', {}).get('temp_max'),
                    'humidity': item.get('main', {}).get('humidity'),
                    'description': item.get('weather', [{}])[0].get('description'),
                    'main': item.get('weather', [{}])[0].get('main'),
                    'icon': item.get('weather', [{}])[0].get('icon'),
                    'wind_speed': item.get('wind', {}).get('speed'),
                    'rain': item.get('rain', {}).get('3h', 0),
                    'clouds': item.get('clouds', {}).get('all')
                })
            
            return forecast_list
        except Exception as e:
            logger.error(f"Error parsing forecast data: {str(e)}")
            return []
