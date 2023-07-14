import requests
from datetime import datetime
from api.keys import openuv_api_key, openweathermap_api_key, getpollen_key


def get_lat_lng_from_postcode(postcode):
    url = f'http://api.postcodes.io/postcodes/{postcode}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        latitude = data['result']['latitude']
        longitude = data['result']['longitude']
        return latitude, longitude
    else:
        raise Exception(f"Error fetching coordinates for postcode {postcode}: {response.status_code}")

def get_weather_data(api_key, latitude, longitude):
    url = f'http://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        weather_data = {
            'description': data['weather'][0]['description'],
            'temperature': data['main']['temp'] - 273.15,  # Convert from Kelvin to Celsius
            'humidity': data['main']['humidity']
        }
        return weather_data
    else:
        raise Exception(f"Error fetching weather data: {response.status_code}")

def get_uv_data(api_key, latitude, longitude):
    url = f'https://api.openuv.io/api/v1/uv?lat={latitude}&lng={longitude}'
    headers = {'x-access-token': api_key}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()

        # Parse and convert timestamps to a simpler format
        uv_max_time = datetime.fromisoformat(data['result']['uv_max_time'].rstrip("Z")).strftime("%I:%M %p")
        sunrise = datetime.fromisoformat(data['result']['sun_info']['sun_times']['sunrise'].rstrip("Z")).strftime("%I:%M %p")
        sunset = datetime.fromisoformat(data['result']['sun_info']['sun_times']['sunset'].rstrip("Z")).strftime("%I:%M %p")

        uv_data = {
            'uv': data['result']['uv'],
            'uv_max': data['result']['uv_max'],
            'uv_max_time': uv_max_time,
            'sunrise': sunrise,
            'sunset': sunset
        }
        return uv_data
    else:
        raise Exception(f"Error fetching UV index data: {response.status_code}")

def get_pollen_count(latitude, longitude):
    result = requests.get(f"https://api.ambeedata.com/latest/pollen/by-lat-lng?lat={latitude}&lng={longitude}&x-api-key={getpollen_key}")
    if result.status_code == 200:
        info = result.json()
        pollen_data = info.get("data", [])

        pollen_risk = {}
        for data in pollen_data:
            for pollen_type, risk in data["Risk"].items():
                pollen_risk[pollen_type.lower()] = risk

        return pollen_risk
    else:
        raise Exception(f"Error fetching pollen count data: {result.status_code}")

def generate_temp_advice(temperature):
    if temperature >= 25:
        temp_advice = "The weather is hot today, best to stay indoors"
        print(temp_advice)
    elif temperature >= 20:
        temp_advice = "The weather is warm, have plenty of cool drinks and take regular breaks"
        print(temp_advice)
    elif temperature >= 10:
        temp_advice = "The temperature is cool today\n"
        print(temp_advice)
    elif temperature >= 0:
        temp_advice = "It's cold today, wrap up warm!"
        print(temp_advice)
    else:
        temp_advice = "Icy conditions, not suitable for gardening"
        print(temp_advice)
    return temp_advice

def generate_uv_advice(max_uv):
    if max_uv >= 8:
        uv_advice = "Peak UV levels are very high today, best to stay indoors\n"
        print(uv_advice)
    if max_uv >= 6:
        uv_advice = "Peak UV levels are high today, take care\n"
        print(uv_advice)
    else:
        uv_advice = "UV levels are safe today\n"
        print(uv_advice)
    return uv_advice

def generate_pollen_advice(pollen_risk):
    high_pollen_types = []
    moderate_pollen_types = []
    low_pollen_types = []

    for pollen_type, level in pollen_risk.items():
        formatted_pollen_type = pollen_type.replace('_', ' ').title()

        if level == 'High':
            high_pollen_types.append(formatted_pollen_type)
        elif level == 'Moderate':
            moderate_pollen_types.append(formatted_pollen_type)
        elif level == 'Low':
            low_pollen_types.append(formatted_pollen_type)

    pollen_advice = ""

    if high_pollen_types:
        pollen_advice += f"The {', '.join(high_pollen_types)} is high today. Take an antihistamine if required.\n"

    if moderate_pollen_types:
        pollen_advice += f"The {', '.join(moderate_pollen_types)} is at a moderate level today. Take appropriate measures.\n"

    if low_pollen_types:
        if len(low_pollen_types) > 1:
            pollen_list = ', '.join(low_pollen_types[:-1])
            pollen_list += f" and {low_pollen_types[-1]}"
            pollen_advice += f"The {pollen_list} is at a low level today. No specific precautions needed.\n"
        else:
            pollen_advice += f"The {low_pollen_types[0]} is at a low level today. No specific precautions needed.\n"

    if not (high_pollen_types or moderate_pollen_types or low_pollen_types):
        pollen_advice = "No specific pollen advice available.\n"

    return pollen_advice

def get_all_details(postcode):
    lat_lng = get_lat_lng_from_postcode(postcode)
    latitude = lat_lng[0]
    longitude = lat_lng[1]

    pollen_risk_data = get_pollen_count(latitude, longitude)
    uv_data = get_uv_data(openuv_api_key, latitude, longitude)
    weather_data = get_weather_data(openweathermap_api_key, latitude, longitude)

    return postcode, pollen_risk_data, uv_data, weather_data

def weather_information(weather_data):
    if weather_data is not None:
        temperature = weather_data.get('temperature', 0)
        print("Weather data:")
        print(f"Description: {weather_data.get('description', '')}")
        print(f"Temperature: {temperature:.2f} °C")
        print(f"Humidity: {weather_data.get('humidity', 0)}%")
        print("\nTemperature advice:")
        generate_temp_advice(temperature)
        return True
    else:
        return False

def uv_information(uv_data):
    if uv_data is not None:
        max_uv = uv_data.get('uv_max', 0)
        print("UV data:")
        print(f"UV index: {uv_data.get('uv', 0):.2f}")
        print()
        print(f"Max UV index: {max_uv:.2f}")
        print(f"Max UV index time: {uv_data.get('uv_max_time', '')}")
        print(f"Sunrise: {uv_data.get('sunrise', '')}")
        print(f"Sunset: {uv_data.get('sunset', '')}")
        print("\nUV advice:")
        generate_uv_advice(max_uv)
        return True
    else:
        return False

def pollen_information(pollen_risk_data):
    if pollen_risk_data is not None:
        print("Pollen count data:")
        for pollen_type, risk in pollen_risk_data.items():
            formatted_pollen_type = pollen_type.replace('_', ' ').title()
            print(f"{formatted_pollen_type}: {risk}")

        print("\nPollen advice:")
        advice = generate_pollen_advice(pollen_risk_data)
        print(advice)
        return True
    else:
        print("\nPollen count data:")
        print("No pollen count data available")
        return False

def print_summary(postcode, pollen_risk_data, uv_data, weather_data):
    print(f"Here are the weather, UV and pollen details for postcode {postcode}:\n")
    return weather_information(weather_data), uv_information(uv_data), pollen_information(pollen_risk_data)

def main_weather_program():
    global postcode
    postcode = input("Please enter your UK postcode: ").strip()  # ask user for postcode
    postcode, pollen_risk_data, uv_data, weather_data = get_all_details(postcode)
    print_summary(postcode, pollen_risk_data, uv_data, weather_data) # print weather details
    if print_summary:
        return True
    else:
        return False