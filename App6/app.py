from flask import Flask, render_template
import json
from collections import defaultdict

app = Flask(__name__)


# Load tirage data
with open('tirage.json', 'r') as file:
    data = json.load(file)  # Parse the JSON data

# Load logos data
with open('logos.json', 'r') as file:
    logos_data = json.load(file)

#club list
club_list = []
for team_name, team_data in data.items():
  club_list.append(team_name)

# function for pot_1_list, pot_2_list, pot_3_list, pot_4_list
def pot_list(pot_number):
  pot_list_ = []
  for club, club_data in data.items():
    if club_data[f"pot_{pot_number}"]["home"]["chapeau"] == pot_number or club_data[f"pot_{pot_number}"]["away"]["chapeau"] == pot_number:
      pot_list_.append(club_data[f"pot_{pot_number}"]["home"]["nom"])
  unique_list = list(set(pot_list_))
  return unique_list

pot_1_list = pot_list(1)
pot_2_list = pot_list(2)
pot_3_list = pot_list(3)
pot_4_list = pot_list(4)

list_pot = [pot_1_list, pot_2_list, pot_3_list, pot_4_list]

# function to choose element (name, logo,.. of opponent team) within a given pot list
def choose_elements(pot_list, element, index):
  
    if pot_list == pot_1_list:
      return data[pot_list[index]]["pot_1"]["home"][element], data[pot_list[index]]["pot_1"]["away"][element]
    elif pot_list == pot_2_list:
      return data[pot_list[index]]["pot_2"]["home"][element], data[pot_list[index]]["pot_2"]["away"][element]
    elif pot_list == pot_3_list:
      return data[pot_list[index]]["pot_3"]["home"][element], data[pot_list[index]]["pot_3"]["away"][element]
    elif pot_list == pot_4_list:
      return data[pot_list[index]]["pot_4"]["home"][element], data[pot_list[index]]["pot_4"]["away"][element]
    else:
      print('error')

#x_home, y_away=choose_elements(pot_1_list, "logo")
def add(a,b):
   return a+b
    
   
@app.route('/')
def display_element():
    
    
    return render_template('index.html', 
                           data = data, 
                           list_pot = list_pot,
                           logos_data = logos_data )

if __name__ == '__main__':
    app.run(debug=True)

