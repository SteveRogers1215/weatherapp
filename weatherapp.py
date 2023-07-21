from tkinter import *
import requests
import json
from datetime import datetime

#Initialize window
root = Tk()
root.geometry("400x400")#default size
root.resizable(0,0)
#window title
root.title("WeatherApp")
#Window background
root.configure(bg='#062726')

#Fetch and display weather info
city_value = StringVar()

def time_format_for_location(utc_with_tz):
    local_time = datetime.utcfromtimestamp(utc_with_tz)
    return local_time.time()

city_value = StringVar()

def showWeather():
    #Enter your API key from OpenWeather
    api_key = "9c9f80141dd33ecc46bceb11819f93bb"

    #city name from user input
    city_name = city_value.get()

    #API url
    weather_url ='http://api.openweathermap.org/data/2.5/weather?q=' + city_name + '&appid=' + api_key

    try:
        response = requests.get(weather_url)
        response.raise_for_status()  # Raise an exception for HTTP errors (e.g., 404, 500)

        weather_info = response.json()

 

    #COD of 200 means successful retrieval
        if weather_info['cod'] == 200:
            kelvin = 273

            #Storing fetched values
            temp = int(weather_info['main']['temp'] - kelvin)
            feels_like_temp = int(weather_info['main']['feels_like'] - kelvin)
            pressure = weather_info['main']['pressure']
            humidity = weather_info['main']['humidity']
            wind_speed = weather_info['wind']['speed'] * 3.6
            sunrise = weather_info['sys']['sunrise']
            sunset = weather_info['sys']['sunset']
            timezone = weather_info['timezone']
            cloudy = weather_info['clouds']['all']
            description = weather_info['weather'][0]['description']

            sunrise_time = time_format_for_location(sunrise + timezone)
            sunset_time = time_format_for_location(sunset + timezone)

            #Assign values to weather variable for display
            weather = f"\nWeather of: {city_name}\nTemperature (Celsius): {temp}°\nFeels like in (Celsius): {feels_like_temp}°\nPressure: {pressure} hPa\nHumidity: {humidity}%\nSunrise at {sunrise_time} and Sunset at {sunset_time}\nCloud: {cloudy}%\nInfo: {description}"
        else:
            weather = f"\n\tWeather for '{city_name}' not found!\n\tPlease enter valid city name!"

        tfield.delete("1.0", "end")
        tfield.insert(INSERT, weather)#sending text field values to display
        

    except requests.exceptions.RequestException as e:
        tfield.delete("1.0", "end")  # Clear the text field
        error_msg = f"An error occurred: {e}"
        tfield.insert(INSERT, error_msg)

    except json.JSONDecodeError as e:
        tfield.delete("1.0", "end")
        error_msg = f"Unable to parse JSON response: {e}"
        tfield.insert(INSERT, error_msg)

    except Exception as e:
        tfield.delete("1.0", "end")
        error_msg = f"An unexpected error occurred: {e}"
        tfield.insert(INSERT, error_msg)   
       

#GUI
city_head = Label(root, text='Enter City Name', font='Montserrat 12 bold', bg='#062726', fg='#FFFFFF').pack(pady=10)
inp_city = Entry(root, textvariable=city_value, width=24, font='Montserrat 14 bold').pack()

Button(root, command=showWeather, text="Check Weather", font="Montserrat 10 bold", bg='#B100E8', fg='#e2cfea', activebackground='teal', padx=5, pady=5).pack(pady=20)

#Show output
weather_now = Label(root, text="The Weather is:", font='Montserrat 12 bold', bg='#062726', fg='#FFFFFF').pack(pady=10)

tfield=Text(root, width=46, height=10)
tfield.pack()

root.mainloop()