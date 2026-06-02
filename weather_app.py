from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import logging
import os

from weather_config import *
from weather_service import WeatherAPI
from weather_cache import WeatherCache

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config.from_object('weather_config')
CORS(app)

weather_api = WeatherAPI()
weather_cache = WeatherCache()


@app.route('/')
def index():
    """Render main page"""
    return render_template('weather_dashboard.html')


@app.route('/api/weather/current', methods=['POST'])
def get_current_weather():
    """Get current weather"""
    try:
        data = request.get_json()
        city = data.get('city')
        
        if not city:
            return jsonify({'error': 'City name required'}), 400
        
        cache_key = f"current_{city.lower()}"
        cached = weather_cache.get(cache_key)
        if cached:
            logger.info(f"Returning cached weather for {city}")
            return jsonify({'success': True, 'data': cached, 'cached': True}), 200
        
        result = weather_api.get_current_weather(city)
        
        if result['success']:
            weather_cache.set(cache_key, result['data'])
            return jsonify({'success': True, 'data': result['data'], 'cached': False}), 200
        else:
            return jsonify({'error': result['error']}), 404
            
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/weather/forecast', methods=['POST'])
def get_forecast():
    """Get weather forecast"""
    try:
        data = request.get_json()
        city = data.get('city')
        days = data.get('days', 5)
        
        if not city:
            return jsonify({'error': 'City name required'}), 400
        
        cache_key = f"forecast_{city.lower()}_{days}"
        cached = weather_cache.get(cache_key)
        if cached:
            logger.info(f"Returning cached forecast for {city}")
            return jsonify({'success': True, 'data': cached, 'cached': True}), 200
        
        result = weather_api.get_forecast(city, days)
        
        if result['success']:
            weather_cache.set(cache_key, result['data'])
            return jsonify({'success': True, 'data': result['data'], 'cached': False}), 200
        else:
            return jsonify({'error': result['error']}), 404
            
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/weather/coordinates', methods=['POST'])
def get_weather_by_coordinates():
    """Get weather by coordinates"""
    try:
        data = request.get_json()
        lat = data.get('lat')
        lon = data.get('lon')
        
        if lat is None or lon is None:
            return jsonify({'error': 'Latitude and longitude required'}), 400
        
        cache_key = f"coordinates_{lat}_{lon}"
        cached = weather_cache.get(cache_key)
        if cached:
            return jsonify({'success': True, 'data': cached, 'cached': True}), 200
        
        result = weather_api.get_weather_by_coordinates(lat, lon)
        
        if result['success']:
            weather_cache.set(cache_key, result['data'])
            return jsonify({'success': True, 'data': result['data'], 'cached': False}), 200
        else:
            return jsonify({'error': result['error']}), 404
            
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/weather/search', methods=['GET'])
def search_cities():
    """Search for cities"""
    try:
        query = request.args.get('q')
        
        if not query or len(query) < 2:
            return jsonify({'error': 'Query must be at least 2 characters'}), 400
        
        result = weather_api.search_cities(query)
        
        if result['success']:
            return jsonify({'success': True, 'cities': result['cities']}), 200
        else:
            return jsonify({'error': result['error']}), 500
            
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/weather/cache/clear', methods=['POST'])
def clear_cache():
    """Clear cache"""
    try:
        data = request.get_json()
        city = data.get('city')
        
        if city:
            weather_cache.clear(f"current_{city.lower()}")
            weather_cache.clear(f"forecast_{city.lower()}_5")
        else:
            weather_cache.clear()
        
        return jsonify({'success': True, 'message': 'Cache cleared'}), 200
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal error: {str(error)}")
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    app.run(debug=DEBUG, host='0.0.0.0', port=5001)
