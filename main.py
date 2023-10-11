# Hello! Welcome to my console app.
# Please start by entering your api key for OpenWeatherMap in the url section below.
# find it at https://openweathermap.org/
# I orginally intended for users to be able to choose from a number of locations, but I struggled to make the timezones work.
# However, if I was to develop this application, this is the next feature I would add.
# EXPLANATION OF API
# The API here is used to pull data about the current weather in London from the latitude and longitude already built into the programme.
# From this data, I use the sunrise time, sunset time, and weather details to assign human-friendly terms to the weather
# I then use my csv files to suggest how good the weather is for outdoor photography, and to give advice for those times when it is okay.
# This advice is taken from blogs around the internet. Sources are credited.

from datetime import datetime, timedelta
# EXPLANATION OF ADDITIONAL MODULES
# I'm importing the datetime module to allow me to work with and manipulate times. This will allow me to work out the time of day in user friendly terms.
# I'm importing the timedelta class from this module to allow me to perform maths on datetime objects, such as adding or subtracting 1 hour.
import requests
# I'm importing requests to allow the programme to communicate with the API.
import csv
# I'm importing CSV to allow me to access my databases of weather ratings and advice external to this python file.

# USE OF INBUILT FUNCTION (PRINT)
print("Hello! Welcome to LondonSnapper, the application that gives Londoners advice for outdoor photography based on the current weather.")
name = input("Please enter your name: ") # USE OF INBUILT FUNCTION (INPUT)
print("Hi {}! Thanks for using our app today.".format(name))

# getting the full response from the api as a json
# USE AN API TO GET RESPONSE AS A JSON
url = "https://api.openweathermap.org/data/2.5/weather?lat=51.509865&lon=-0.118092&appid={enter api here}"
# please replace this API key with your own API key. find it at https://openweathermap.org/
response = requests.get(url).json()

##### USE OF FUNCTIONS ######

# a function to turn the unix timestamp into a regular timestamp
def unix_to_datetime(unix):
    date_and_time = datetime.fromtimestamp(unix)
    return date_and_time

# a function to see whether it's daytime or nighttime
def is_it_daytime(): # USE OF IF...ELSE
    if date_time_sunrise <= date_time_now <= date_time_sunset:
        return "daytime"
    else:
        return "nighttime"

# a function to use string slicing to get the time only from a YY:MM:DD HH:MM:SS timestamp
def get_time(timestamp):
    time = str(timestamp)[11:19] # USE OF STRING SLICING
    dt_format = "%H:%M:%S"
    dt_time = datetime.strptime(time, dt_format)
    return dt_time.time()

# a function to turn a string time into a datetime object
def string_time_to_datetime(string):
    today_date = datetime.now().date()
    midnight_time = datetime.strptime(string, "%H:%M:%S").time()
    result = datetime.combine(today_date, midnight_time)
    return result

# a function to determin what time of the day it is in human-friendly terms
def time_of_day():
    one_hour = timedelta(hours=1)
    two_hours = timedelta(hours=2)
    midnight = string_time_to_datetime("00:00:00")
    start_of_blue_hour_morning = date_time_sunrise - one_hour
    end_of_golden_hour_morning = date_time_sunrise + one_hour
    noon = string_time_to_datetime("12:00:00")
    start_of_evening = date_time_sunset - two_hours
    start_of_golden_hour_evening = date_time_sunset - one_hour
    end_of_blue_hour_evening = date_time_sunset + one_hour
    # USE OF IF...ELSE
    if start_of_blue_hour_morning <= date_time_now < date_time_sunrise or date_time_sunset <= date_time_now < end_of_blue_hour_evening:
        return "Blue hour"
    elif date_time_sunrise <= date_time_now < end_of_golden_hour_morning or start_of_golden_hour_evening <= date_time_now < date_time_sunset:
        return "Golden hour"
    elif end_of_golden_hour_morning <= date_time_now < noon:
        return "Morning"
    elif noon <= date_time_now < start_of_evening:
        return "Afternoon"
    elif start_of_evening <= date_time_now < start_of_golden_hour_evening:
        return "Evening"
    else:
        return "Night"

# defining variables
date_time_now = datetime.now()
date_time_sunrise = unix_to_datetime(response['sys']['sunrise'])
date_time_sunset = unix_to_datetime(response['sys']['sunset'])
location = response['name']
main_weather = response['weather'][0]['main']
detail_weather = response['weather'][0]['description']
daytime_or_nighttime = is_it_daytime()

# USE OF DATA STRUCTURE
conditions_now = {"time" : get_time(date_time_now),
                  "location" : location,
                  "daytime or nighttime" : daytime_or_nighttime,
                  "weather" : detail_weather}

# interacting with the user using while loops and user input
while True: # USE OF BOOLEAN VALUES, WHILE LOOP
    user_input = input("Want to generate some free advice?\n"
                        "Enter Y for Yes and N for No: ") # USE OF INBUILT FUNCTION (INPUT)
    # USE OF IF...ELSE
    if user_input == "Y" or user_input == "y":
        conditions_output = "TIME {}: In {}, it's {} and the weather is {}.".format(
            conditions_now["time"],
            conditions_now["location"],
            conditions_now["daytime or nighttime"],
            conditions_now["weather"])
        print(conditions_output)

        csv_file_path = 'weather_rating.csv'
        target_description = detail_weather
        rating = None
        rating_output = ""
        with open(csv_file_path, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['Description'] == target_description:
                    rating = row[time_of_day()]
                    break
        if rating is not None:
            rating_output = f"The rating for these conditions is: {rating} for outdoor photography"
            print(rating_output)
        else:
            rating_output = f"No data found for '{target_description}'"
            print(rating_output)

        csv_file_path = 'advice.csv'
        target_description = detail_weather
        advice = None
        with open(csv_file_path, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['Description'] == target_description:
                    advice = row[time_of_day()]
                    break
        advice_output = ""
        # USE OF IF...ELSE
        if advice == "Rainy evening":
            advice_output = "Rainy evenings are great for capturing the reflections of the city lights in the wet streets.\n"\
                            "Source: https://petapixel.com/photography-weather-lighting-conditions/#5_Taking_Photographs_on_Sunny_Days)"
        elif advice == "Snowy":
            advice_output = "Snowy conditions make for some wonderful photography opportunities.\n"\
                            "However, taking photos in snow can be a little bit challenging.\n"\
                            "This is for a number of reasons, from the brightness of the snow, through to the cold weather conditions that can hamper a camera’s functions.\n"\
                            "Then of course you have to consider general winter issues, like ice and cold, that can make conditions challenging for a photographer.\n"\
                            "Source: https://www.findingtheuniverse.com/snow-photography-tips/#:~:text=Snowy%20conditions%20make%20for%20some,can%20hamper%20a%20camera's%20functions."
        elif advice == "Mist":
                            "Misty conditions tend to make elements in the scene that are closer to the camera more ‘punchy’ and defined against the more ‘faded’ background.\n"\
                            "This layering of stronger tones over faded tones can help create a sense of depth in the scene.\n"\
                            "Source: https://petapixel.com/photography-weather-lighting-conditions/#4_Taking_Photographs_on_Misty_Mornings"
        elif advice == "Smoke":
            advice_output = "Light through moderate smoke pollution typically grabs sunrise and sunset colour.\n"\
                            "Smoke can cluster, appearing cloud-like, and colour up with unique reds, pinks, oranges and yellows.\n"\
                            "This can result in some spectacular sky conditions, so continue capturing images and experimenting as you would under normal sky conditions.\n"\
                            "Source: https://www.ginayeo.com/blog/how-to-capture-landscape-images-in-wildfire-smoke"
        elif advice == "Blue hour":
            advice_output = "At this time the sky is no longer the pure black of nighttime but an attractive deep shade of blue.\n"\
                            "Blue hour is by far the best time to capture night photos, especially in cities.\n"\
                            "There is just enough ambient light to balance the light of the city with the darkness of the sky.\n"\
                            "Source: https://petapixel.com/photography-weather-lighting-conditions/#1_Taking_Photographs_During_Morning_Blue_Hour"
        elif advice == "Golden hour":
            advice_output = "Most novice photographers know about the virtues of shooting at golden hour and with good reason too.\n"\
                            "The light at this time can help produce stunning results.\n"\
                            "The golden hour refers to the period just after the sun rises or just before it sets.\n"\
                            "I’m sure you’ve noticed how the light of the early morning sunrise and its evening sunset counterpart often bathe buildings or nature in a beautiful golden glow.\n"\
                            "This golden warm tone is due to the fact that the sun is lower in the sky in the morning and evening.\n"\
                            "This means the light passes through more atmosphere which scatters the bluer cooler light in the spectrum.\n"\
                            "This leaves us with the warmer red, orange, and yellow tones.\n"\
                            "Source: https://petapixel.com/photography-weather-lighting-conditions/#4_Taking_Photographs_on_Misty_Mornings"
        elif advice == "Fog":
            advice_output = "If there’s one thing that we know about fog, it is that it reduces contrast within the scene.\n"\
                            "This can make it difficult to create any sense of depth in your shots, resulting in flat and boring compositions.\n"\
                            "Fog can be used to demonstrate depth between the foreground and background.\n"\
                            "You can work around this by getting closer to your subject.\n"\
                            "How close you’ll need to get will depend largely upon how dense the fog is.\n"\
                            "The more distance you place between yourself and the subject,\nthe less contrast that you’ll achieve and the more it will seem as though it is fading into the fog.\n"\
                            "Source: https://iceland-photo-tours.com/articles/photography-tutorials/how-to-improve-your-fog-photography"
        elif advice == "Clear morning/evening":
            advice_output = "The light is most interesting in morning and evening.\n"\
                            "You can try all different types of outdoor photography at this time."
        elif advice == "Scattered clouds daytime":
            advice_output = "I find that wooded areas make excellent subjects on a sunny day.\n"\
                            "In the above photo, the high sun streams its light through the trees of the forest making for an attractive photo.\n"\
                            "Sunny days with a clear blue sky are rarely conducive to capturing the more artistic style photos.\n"\
                            "The light is harsh and the cloudless sky can seem uninteresting and devoid of drama.\n"\
                            "Such days, however, can be very suitable for architecture photography.\n"\
                            "Source: https://petapixel.com/photography-weather-lighting-conditions/#5_Taking_Photographs_on_Sunny_Days"
        elif advice == "Sunny day":
            advice_output = "Sunny days with scattered clouds and strong light are great for creating high contrast black and white images.\n"\
                            "Source:https://petapixel.com/photography-weather-lighting-conditions/#5_Taking_Photographs_on_Sunny_Days"
        elif advice == "Overcast":
            advice_output = "Overcast days are perfect for portrait photography.\n"\
                            "An overcast sky is like a giant studio light-box and guarantees even light on the subjects.\n"\
                            "This is always more flattering than strong sunlight which casts shadows across the face and amplifies every wrinkle and blemish.\n"\
                            "Source: https://petapixel.com/photography-weather-lighting-conditions/#6_Taking_Photographs_on_Overcast_Days"
        else:
            advice_output = "You can go for it, but you might be better off waiting for better conditions!"
        print(advice_output) # USE OF INBUILT FUNCTION (PRINT)
        while True: # USE OF BOOLEAN VALUES, WHILE LOOP
            user_input = input("Would you like to save this advice for later?\n"
                               "Enter Y for yes, and N for no: ") # USE OF INBUILT FUNCTION (INPUT)
            if user_input == "Y" or user_input == "y":
                with open("saved_advice.txt", "w") as file: # WRITE RESULTS IN A FILE:
                    file.write(str(conditions_output))
                    file.write("\n")
                    file.write(str(rating_output))
                    file.write("\n")
                    file.write(str(advice_output))
                    print("Okay, I've saved that for you in the file saved_advice.txt")
                    print("Thanks for using the app!")
                break
            elif user_input == "N" or user_input == "n":
                print("Okay, no problem")
                break
            else:
                print("Please try again - enter Y for Yes and N for No!")
        break
    elif user_input == "N" or user_input == "n":
        print("Okay! Catch you next time, {}".format(name))
        break
    else:
        print("Please try again - enter Y for Yes and N for No!")

