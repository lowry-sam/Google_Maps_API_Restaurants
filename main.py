import gspread
import oauth2client
import requests
import smtplib
import googlemaps
from datetime import datetime
from tkinter import *
from tkinter import messagebox
import tkintermapview
from pprint import pprint
from tkinter import ttk
from google.oauth2.service_account import Credentials
import time

colors = ["red", "orange", "yellow", "green", "blue", "purple", "pink", "brown", "black", "gray"]
startingLocation = "Cloud Gate"
current_location = ""
current_coordinates = ""

class Worksheet:
    def __init__(self):
        self.worksheet = ""
        self.zoom_level = 10
    def set_worksheet(self,name):
        self.worksheet = name
    def set_zoom(self,zoom):
        if zoom >= 10 and zoom <=15:
            self.zoom_level=zoom
            map_widget.set_zoom(zoom)
            my_slider.config(value=zoom)
        else: 
            zoom = 10
            map_widget.set_zoom(10)
            my_slider.config(value=10)
    def print_worksheet(self):
        print(self.worksheet, self.zoom_level)
    def get_worksheet(self):
        return self.worksheet
    def get_zoom(self):
        return self.zoom_level


def lookup(coords): 
    map_widget.delete_all_path()
    been_to.grid_forget()

    if (coords != ""):
        rev_geocode_result = maps.reverse_geocode(coords)
        current_location = rev_geocode_result[0]['formatted_address']
        my_entry.delete(0, 'end')
        my_entry.insert(0, coords)
    else:
        current_location = my_entry.get()
    if (current_location == ""):
        current_location = "Cloud Gate"
    response_geocode = maps.geocode(current_location)
    if response_geocode != []:
        if len(markers) > 0:
            for m in range(len(markers)):
                if markers[m] != False:
                    markers[m].delete()
        inChicago = False
        m = 0
        for m in range(len(response_geocode[0]['address_components'])):
            if response_geocode[0]['address_components'][m]['long_name'] == "Chicago":
                inChicago = True
        if inChicago:
            lat = (response_geocode[0]['geometry']['location']['lat'])
            lng = (response_geocode[0]['geometry']['location']['lng'])
            map_widget.set_address(lat,lng)
            map_widget.set_position(lat, lng)
            
            
            marker_1 = map_widget.set_address(current_location, text="You are here!", marker=True, marker_color_outside="black")
            if (marker_1 == False):
                marker_1 = map_widget.set_address(response_geocode[0]['formatted_address'], text="You are here!", marker=True, marker_color_outside="black")
            if (marker_1 == False):
                marker_1 = map_widget.set_address("The Bean", text="You are here!", marker=True, marker_color_outside="black")
                my_entry.delete(0, 'end')
                my_entry.insert(0, "The Bean")
            markers[0] = marker_1

            worksheet_object.set_zoom(14)

            second_plus_third.pack_forget()
            in_between.pack_forget()
            second_frame.pack_forget()
            third_frame.pack_forget() 
            fourth_plus_fifth.pack_forget()
            fourth_frame.pack_forget()
            fifth_frame.pack_forget()
            sixth_frame.pack_forget()
            second_plus_third.pack()
            second_frame.pack(pady=0)
            in_between.pack()

            worksheet_list = list(map(lambda x: x.title, sheet.worksheets()))

            third_frame.pack(pady=0)
            buttons={}
            row_num = 0
            col_num = 0
            for i in range(1, len(list(worksheet_list))):
                buttons[i] = Button(third_frame, text=list(worksheet_list)[i], relief="raised", font=("Calibri", 15), activebackground="red", 
                                activeforeground="white",command=lambda x = i: set_worksheet(list(worksheet_list)[x]))
                buttons[i].grid(row=row_num, column=col_num, padx=10, pady=3)
                
                col_num = col_num + 1
                if col_num % 5 == 0:
                    row_num = row_num + 1
                    col_num = 0
        else: 
            messagebox.showerror("Error!", "That is not a valid location. \nPlease try again.")
            return
    else:
        messagebox.showerror("Error!", "That is not a valid location. \nPlease try again.")
        my_entry.delete(0, END)


def slide(e):
    map_widget.set_zoom(my_slider.get())

def set_worksheet(aWorksheet):
    map_widget.delete_all_path()
    if len(markers) > 0:
            for m in range(1, len(markers)):
                markers[m].delete()
    try: 
        worksheet_object.set_worksheet(aWorksheet)
        current_worksheet = sheet.worksheet(worksheet_object.get_worksheet())
        display_buttons(current_worksheet)
    except: messagebox.showerror("Error!", "Sheets API has failed. \nPlease try again.")

def display_buttons(worksheet):
    map_widget.delete_all_path()
    reset_view()
    fourth_plus_fifth.pack_forget()
    fourth_frame.pack_forget()
    fourth_plus_fifth.pack(pady=0)
    fourth_frame.pack(pady=3)
    fourth_frame.config(text="Select a specific type:", font=("Calibri", 15, "bold"), fg="blue", pady=0, padx=10)
    marker_label_initial.grid_forget()
    been_to.grid_forget()

    if len(markers) > 0:
            for m in range(1, len(markers)):
                markers[m].delete()

    sixth_frame.pack_forget()
    fifth_frame.pack_forget()
    fifth_frame.pack(pady=0)
    type_list = list(worksheet.row_values(1))

    button_label.grid_forget()
    button_label.grid(column=1, row=1, pady=3)
    if buttons2 != {}:
        for l in range(0, len(buttons2) * 3):
            try: buttons2[l].grid_forget()
            except:
                l = l + 1

    row_num2 = 0
    col_num2 = 0 
    for i in range(0, len(type_list), 3):
        if type_list[i] == "":
            i = i + 1
        buttons2[i] = Button(button_label, text=type_list[i], relief="raised", font=("Calibri", 15), activebackground="blue", 
                                    activeforeground="white", command=lambda x = i: set_type(worksheet, type_list[x]))
        buttons2[i].grid(row=row_num2, column=col_num2, padx=10, pady=3)
        col_num2 = col_num2 + 1
        if col_num2 % 5 == 0:
            row_num2 = row_num2 + 1
            col_num2 = 0

def set_type(worksheet, aType):
    reset_view()
    for i in range(len(marker_label)):
        marker_label[i].grid_forget()
    
    marker_label_initial.grid_forget()
    been_to.grid_forget()
    stack = []

    try: 
        title = worksheet.find(aType)
        i = title.row + 4
        j = title.col

        # been_to_string = worksheet.find("Number Reviewed")
        # a = been_to_string.row+1
        # b = been_to_string.col
        # been_to_amt = worksheet.cell(a,b).value

        if aType == "ERRANDS":
            been_to_amt = worksheet.cell(i-2,j+2).value
        else: been_to_amt = worksheet.cell(i-2,j+1).value
    except: 
        messagebox.showerror("Error!", "That title was not found in the sheet.\nPlease try again.")
        return

    big_distance = 0.0
    mid_lat = 0.0
    mid_lng = 0.0
    
    if len(markers) > 0:
        for m in range(1, len(markers)):
            markers[m].delete()
            del markers[m]

    if len(things_list) > 0:
        for _ in range(len(things_list)):
            things_list.pop()

    if len(directions_list) > 0:
        for _ in range(len(directions_list)):
            directions_list.pop()
    
    not_in_chicago = []
    not_found = []
    k = 0
    marker_index = 1
    path_index = 1

    while i < 100:
        place_name = ""
        try: 
            
            if (aType == "CHRISTMAS SZN"):
                j = title.col
                place_name = worksheet.cell(i,j).value 
                j = j + 1
                cell_value = worksheet.cell(i,j).value 
            elif(aType == "ENTERTAINMENT"):
                j = title.col + 1
                cell_value = worksheet.cell(i,j).value 
            else: cell_value = worksheet.cell(i,j).value   
                  
        except: 
            messagebox.showerror("Warning!", "Google API limit exceeded.\nPlease try again in a bit.")
            cell_value = None
            
        if cell_value != None and cell_value != FALSE:
            if '$' in cell_value:
                cell_values = cell_value.split(" $ ")
                cell_value = cell_values[1]
                place_name = cell_values[0]

            response_geocode = maps.geocode(cell_value)
            if (response_geocode != []):
                inChicago = False

                # url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&"
                # req = requests.get(url+"origins="+currentSpot[0]['formatted_address']+"&destinations="+new_response_geocode[0]['formatted_address']+"&key="+api_key+"&mode=car")
                # try: 
                #     if req.json()["rows"][0]["elements"][0]["status"] != 'OK':
                #         not_in_chicago.append(cell_value)
                #         break
                #     req_string = req.json()["rows"][0]["elements"][0]["distance"]["text"]
                # except: 
                #     messagebox.showerror("Error!", "Google Maps API failed.\nPlease try again.")
                #     break
                
                m = 0
                for m in range(len(response_geocode[0]['address_components'])):
                    if response_geocode[0]['address_components'][m]['long_name'] == "Illinois" or \
                        response_geocode[0]['address_components'][m]['long_name'] == "Wisconsin" or \
                        response_geocode[0]['address_components'][m]['long_name'] == "Indiana":
                            inChicago = True
                            break
                lat = (response_geocode[0]['geometry']['location']['lat'])
                lng = (response_geocode[0]['geometry']['location']['lng'])

                # try: 
                    # directions_result = maps.directions((latCurr, lngCurr), (lat,lng), departure_time=now, mode="walking")
                    # req_string = directions_result[0]['legs'][0]['distance']['text']
                    # mode_string = req_string.split(" ")
                    # mode_string = mode_string[0].split(",")
                    # if len(mode_string) > 1:
                    #     mode_string[0] = mode_string[0] + mode_string[1]
                    # if float(mode_string[0]) < 50.0: inChicago = True
                    # if float(mode_string[0]) > big_distance and inChicago == True:
                    #     big_distance = float(mode_string[0])
                    #     # mid_lat = (latCurr + lat)/2.0
                    #     # mid_lng = (lngCurr + lng)/2.0
                # except:
                #     messagebox.showerror("Error!", "Google API has failed.\nPlease try again.")
                #     break
                
                if inChicago:
                    if k == len(colors):
                        k = 0
                    
                    if place_name == "":
                        place_name = cell_value
                    if ' - ' in cell_value:
                        cell_value_split = cell_value.split(' - ')
                        cell_value = cell_value_split[0]
                    if ' | ' in cell_value:
                        cell_value_split = cell_value.split(' | ')
                        cell_value = cell_value_split[0]
                    if '(' in cell_value:
                        cell_value_split = cell_value.split('(')
                        cell_value = cell_value_split[0]
                    if  ' : ' in cell_value:
                        cell_value_split = cell_value.split(' : ')
                        cell_value = cell_value_split[0]
                    if "Chicago" in cell_value:
                        cell_value_split = cell_value.split("Chicago")
                        cell_value = cell_value_split[0]
                    if ' - ' in place_name:
                        place_name_split = place_name.split(' - ')
                        place_name = place_name_split[0]
                    if ' | ' in place_name:
                        place_name_split = place_name.split(' | ')
                        place_name = place_name_split[0]
                    if '(' in place_name:
                        place_name_split = place_name.split('(')
                        place_name = place_name_split[0]
                    if ' : ' in place_name:
                        place_name_split = place_name.split(' : ')
                        place_name = place_name_split[0]
                    if "Chicago" in cell_value:
                        place_name_split = place_name.split("Chicago")
                        place_name = place_name_split[0]

                    markers[marker_index] = map_widget.set_marker(lat,lng, text=place_name, marker_color_outside=colors[k], marker_color_circle="white", command=print_marker)
                    
                    if markers[marker_index] != False:
                        if place_name == "": things_list.append(cell_value)
                        else: things_list.append(place_name)
                        
                        if (len(directions) > 0):
                            for _ in range(len(directions)):
                                directions.pop()

                        # directions.append((latCurr, lngCurr))
                        # for n in range(len(directions_result[0]['legs'][0]['steps'])):
                        #     dirLat = directions_result[0]['legs'][0]['steps'][n]['end_location']['lat']
                        #     dirLng = directions_result[0]['legs'][0]['steps'][n]['end_location']['lng']
                        #     directions.append((dirLat,dirLng))

                        stack = []
                        stack = stack[:] + directions
                        directions_list.append(stack)
                        
                        path_index = path_index + 1
                        marker_index = marker_index + 1
                        k = k + 1
                else: not_in_chicago.append(cell_value)
            else: not_found.append(cell_value)
            map_widget.config()
        else: i = 100
        i = i + 1
    print("places: ", list(things_list))
    print("Places not found:", list(not_found) )
    print("Places not in Chicago: ", list(not_in_chicago))

    # if big_distance <= 1.5: 
    #     worksheet_object.set_zoom(15)
    # elif big_distance <= 2.75: 
    #     worksheet_object.set_zoom(14)
    # elif big_distance <= 6.0: 
    #     worksheet_object.set_zoom(13)
    # else:
    #     worksheet_object.set_zoom(12)
    # print(big_distance)
    # print(worksheet_object.get_zoom())
    if mid_lng != 0.0 and mid_lat != 0.0:
        map_widget.set_position(mid_lat, mid_lng)
    worksheet_object.set_zoom(12)
    # else: map_widget.set_position(latCurr, lngCurr)
    # map_widget.set_zoom(12)
    # my_slider.config(value=12)

    sixth_frame.pack_forget()
    sixth_frame.configure(width=100)
    sixth_frame.pack(pady=10)

    stats_label.grid_forget()
    stats_label2.grid_forget()

    if len(markers) == 2:
        if been_to_amt == 0:
            stats_label.config(text=f"For {aType}, there is {len(markers) - 1} marker on the map! You have NOT been to it.")
        else:
            stats_label.config(text=f"For {aType}, there is {len(markers) - 1} marker on the map! You have been to it.")
        stats_label2.config( text="Click on it for more details. Or, choose a different category!")
    elif len(markers) == 1:
        stats_label.config(text=f"For {aType}, there are no markers on the map.")
        stats_label2.config(text="Please choose a different category.")
    else: 
        stats_label.config(text=f"For {aType}, there are {len(markers) - 1} markers on the map, and you have been to {been_to_amt} of them!")
        stats_label2.config(text="Click on one for more details. Or, choose a different category!")
    stats_label.grid(row=1, column=1)
    stats_label2.grid(row=2, column=1)
    

def print_marker(marker):
    map_widget.delete_all_path()
    sixth_frame.pack_forget()
    sixth_frame.configure(width=100)
    sixth_frame.pack(pady=10)
    stats_label.grid_forget()
    stats_label2.grid_forget()

    # big_distance = 0.0

    for mark in range(1, len(markers)):
        markers[mark].set_text(things_list[mark-1])
   
        if marker.text != things_list[mark-1]:
            markers[mark].set_text("")
        else: 
            color_num = mark
            while color_num > 10:
                color_num = color_num - 10
            

    current_location = my_entry.get()
    if (current_location == ""):
        current_location = "The Bean"
    try: 
        response_geocode = maps.geocode(current_location)
        if (response_geocode != []):
            lat_curr = (response_geocode[0]['geometry']['location']['lat'])
            lng_curr = (response_geocode[0]['geometry']['location']['lng'])
            current_location = response_geocode[0]['formatted_address']
    except: 
        messagebox.showerror("Error!", "Google Maps API failed.\nPlease try again.")
        return

    try: 
        new_response_geocode = maps.geocode(marker.text)
        lat = (new_response_geocode[0]['geometry']['location']['lat'])
        lng = (new_response_geocode[0]['geometry']['location']['lng'])
    except: 
        messagebox.showerror("Error!", "Google Maps API failed.\nPlease try again.")
        return

    try: directions_result = maps.directions((lat_curr, lng_curr), (lat,lng), departure_time=now, mode="walking")
    except: 
        messagebox.showerror("Error!", "Google Maps API failed.\nPlease try again.")
        return

    # req_string = directions_result[0]['legs'][0]['distance']['text']
    # mode_string = req_string.split(" ")
    # mode_string = mode_string[0].split(",")
    # if len(mode_string) > 1:
    #     mode_string[0] = mode_string[0] + mode_string[1]
    # if float(mode_string[0]) > big_distance:
    #     big_distance = float(mode_string[0])
        # mid_lat = (latCurr + lat)/2.0
        # mid_lng = (lngCurr + lng)/2.0

    if len(directions):
        for _ in directions:
            directions.pop()

    directions.append((lat_curr, lng_curr))
    for n in range(len(directions_result[0]['legs'][0]['steps'])):
        dirLat = directions_result[0]['legs'][0]['steps'][n]['end_location']['lat']
        dirLng = directions_result[0]['legs'][0]['steps'][n]['end_location']['lng']
        directions.append((dirLat,dirLng))

    path_1 = map_widget.set_path(directions, color=colors[color_num-1])

    mid_lat = (lat_curr + marker.position[0])/2.0
    mid_lng = (lng_curr + marker.position[1])/2.0
    map_widget.set_position(mid_lat, mid_lng)
    #worksheet_object.set_zoom(13)

    pos = ','.join(str(val) for val in marker.position)
    new_url = "https://maps.googleapis.com/maps/api/geocode/json?" 
    
    try: 
        r = requests.get(new_url+"latlng="+pos+"&key="+api_key)
        desired_location = r.json()
    except: 
        messagebox.showerror("Error!", "Google Maps API failed.\nPlease try again.")
        return

    url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&"
    mode = ["car", "transit", "biking", "walking"]
    
    for i in range(len(marker_label)):
        marker_label[i].grid_forget()
    
    marker_label_initial.grid_forget()
    marker_label_initial.config(bg="white", text="For " + marker.text + ", here's how far it is away:", pady=5, padx=5, font=("Calibri", 15), fg="green")
    marker_label_initial.grid(column=1, row=1)

    for i in range(len(mode)):
        req = requests.get(url+"origins="+current_location+"&destinations="+desired_location['results'][0]['formatted_address']+"&key="+api_key+"&mode="+mode[i])
        try: 
            req_string = "By " + mode[i] + " it is " + req.json()["rows"][0]["elements"][0]["duration"]["text"]
            marker_label[i] = Label(sixth_frame, text = req_string, font=("Calibri", 15), bg="white")
            marker_label[i].grid(column=1, row = i + 2)
            if mode[i] == "car":
                mode_string = req.json()["rows"][0]["elements"][0]["distance"]["text"].split(" ")
                if float(mode_string[0]) <= 1.5: 
                    map_widget.set_zoom(15)
                    my_slider.config(value=15)
                elif float(mode_string[0]) <= 0.5: 
                    map_widget.set_zoom(16)
                    my_slider.config(value=16)
                elif float(mode_string[0]) <= 2.5: 
                    map_widget.set_zoom(14)
                    my_slider.config(value=14)
                elif float(mode_string[0]) <= 6.0: 
                    map_widget.set_zoom(13)
                    my_slider.config(value=13)
                else:
                    map_widget.set_zoom(12)
                    my_slider.config(value=12)
        except IndexError:
            messagebox.showerror("Error!", "Google Maps API failed.\nPlease try again.")
            return
        except: 
            messagebox.showerror("Error!", "Google API quota exceeded.\nPlease try again.")
            return
        
    try:
        been_to_string = ""
        worksheet = worksheet_object.get_worksheet()
        current_worksheet = sheet.worksheet(worksheet)
        place = current_worksheet.find(marker.text)
        i = place.row
        j = place.col

        if worksheet == "Entertainment" or worksheet == "Sightseeing":
            if current_worksheet.cell(i,j+3).value == "TRUE":
                been_to_string = "You have been here before."
            else: been_to_string = "You have not been here yet!" 
        else:
            if current_worksheet.cell(i,j+2).value == "TRUE":
                been_to_string = "You have been here before."
            else: been_to_string = "You have not been here yet!" 
    except:
        messagebox.showerror("Error!", "Google API quota limit reached.\nPlease wait and try again.")
        return
    
    been_to.grid_forget()
    been_to.config(text = been_to_string, font=("Calibri", 15, "italic"), bg="white")    
    been_to.grid(column=1, row=6)

def reset_view():
    map_widget.delete_all_path()
    worksheet_object.set_zoom(13)
    current_location = my_entry.get()
    if (current_location == ""):
        current_location = "The Bean"
    try:
        response_geocode = maps.geocode(current_location)
        lat = (response_geocode[0]['geometry']['location']['lat'])
        lng = (response_geocode[0]['geometry']['location']['lng'])
        map_widget.set_position(lat,lng)
    except: 
        messagebox.showerror("Error!", "Google Maps API failed.\nPlease try again.")
        return

    for mark in range(1, len(markers)):
        markers[mark].set_text(things_list[mark-1])

def reset_map():
    map_widget.set_position(start_lat,start_lng)
    worksheet_object.set_zoom(worksheet_object.get_zoom())
    map_widget.delete_all_path()
    for i in range(len(marker_label)):
        marker_label[i].grid_forget()
    
    marker_label_initial.grid_forget()
    if len(markers) > 0:
        for m in range(len(markers)):
            if markers[m] != False:
                markers[m].delete()
    marker_1 = map_widget.set_address(startingLocation, marker=False, marker_color_outside="black")

    second_frame.pack_forget()
    third_frame.pack_forget()
    fourth_frame.pack_forget()
    fifth_frame.pack_forget()
    sixth_frame.pack_forget()

def set_current_location_click(coordinates_tuple):
    current_coordinates = coordinates_tuple
    lookup(coordinates_tuple)

window = Tk()
window.title("Google Maps API")
window.geometry("1030x900")
window.configure(bg="black")

scopes = [
    "https://www.googleapis.com/auth/spreadsheets"
]
creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
client = gspread.authorize(creds)

sheet_file = open("a-sheet-id.txt", "r")
sheet_id = sheet_file.read()
sheet = client.open_by_key(sheet_id)
worksheet_object = Worksheet()

api_file = open("api-key.txt", "r")
api_key = api_file.read()
maps = googlemaps.Client(key=api_key)

now = datetime.now()

directions = [20]

response_geocode = maps.geocode(startingLocation)
start_lat = (response_geocode[0]['geometry']['location']['lat'])
start_lng = (response_geocode[0]['geometry']['location']['lng'])

canvas = Canvas(window)
canvas.pack(side=LEFT, fill=BOTH, expand=True)

scrollbar = Scrollbar(window,orient=VERTICAL, command=canvas.yview)
scrollbar.pack(side=RIGHT, fill=Y)

canvas.configure(yscrollcommand=scrollbar.set, relief="flat")
my_frame = Frame(canvas)

canvas.create_window((0,0), window=my_frame, anchor="nw")
my_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

credit_frame = LabelFrame(my_frame, relief="flat", pady=10)
credit_frame.pack()

credit_label = Label(credit_frame, font=("Calibri", 18, "bold"), width=77, pady=0, text="Welcome to the Chicago Google API & Python Maps Application!")
credit_label.pack()
credit_label2 = Label(credit_frame, font=("Calibri", 12),  pady=0, text="An application created by Sam Lowry, 2026", fg="red")
credit_label2.pack()

my_label = LabelFrame(my_frame, relief="solid")
my_label.pack()

map_widget = tkintermapview.TkinterMapView(my_label, width=800, height=600, corner_radius=5, )
map_widget.pack()

sixth_frame=LabelFrame(my_frame, pady=15, padx = 5, relief="ridge", bg="white")
sixth_frame.pack()

starting_label = LabelFrame(my_frame, bg="white")
starting_label.pack(pady=20, padx=30)

my_entry = Entry(starting_label, font=("Comic Sans", 20), bg="white", fg="black", relief="solid")
my_entry.grid(row=0, column=0, padx=20, pady=20)

my_button = Button(starting_label, text="Set Current Position", relief="solid", activebackground="blue", 
            activeforeground="white",font=("Comic Sans", 15), command=lambda: lookup(""))
my_button.grid(row=0,column=1, padx=10)

reset_button = Button(starting_label,text="Reset View", relief="solid", font=("Comic Sans", 15), activebackground="blue", 
                            activeforeground="white", command=reset_view)
reset_button.grid(row=0,column=3, padx=10)

my_slider = ttk.Scale(starting_label, from_=10, to=16, orient=HORIZONTAL, command=slide, value = 11, length=220)
my_slider.grid(row = 0, column=2, padx=10)

second_plus_third = LabelFrame(my_frame, pady=10, relief="ridge", bg="white", width=400, )
second_frame = Label(second_plus_third, pady=3, padx=10, text="What kind of thing are you interested in?", font=("Calibri", 15, "bold"), fg="red", relief="flat", bg="white")
third_frame = Label(second_plus_third, pady=3, relief="flat", bg="white")

in_between = LabelFrame(my_frame, relief="flat", text="", height=10)

fourth_plus_fifth = LabelFrame(my_frame, pady=10, relief="ridge", bg="white")
fourth_frame = Label(fourth_plus_fifth, text="", pady=3, fg="blue", relief="flat", bg="white")
fifth_frame=Label(fourth_plus_fifth, pady=0, relief="flat", bg="white")

seventh_frame=LabelFrame(my_frame, width=200, text="", relief="flat")
marker_label_initial = Label(sixth_frame)
been_to = Label(sixth_frame)
stats_label = Label(sixth_frame, font=("Calibri", 15, "bold"), bg="white")
stats_label2 = Label(sixth_frame, font=("Calibri", 15), fg = "green", bg="white")
button_label = Label(fifth_frame, width=50,  relief="flat", bg="white")
buttons2={}
markers={}
marker_label = {}
directions_list = []
directions = []
path_list = {}
things_list = []
k = 0

marker_1 = map_widget.set_address(startingLocation, marker=False, marker_color_outside="black")
map_widget.set_position(start_lat,start_lng)
worksheet_object.set_zoom(12)

map_widget.add_right_click_menu_command(label="Set Current Location", command=set_current_location_click, pass_coords=True)

window.mainloop()