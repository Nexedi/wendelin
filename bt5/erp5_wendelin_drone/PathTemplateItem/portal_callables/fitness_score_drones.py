import math
import pandas as pd
import numpy as np
import re


R = 6371e3


def mean_operation(data):
  return float(sum(data)/len(data))


def distance(lat1, lon1, lat2, lon2):
    lat1_rad = lat1 * math.pi / 180
    lat2_rad = lat2 * math.pi / 180
    lon1_rad = lon1 * math.pi / 180
    lon2_rad = lon2 * math.pi / 180
    haversine_phi = math.sin((lat2_rad - lat1_rad) / 2) ** 2
    sin_lon = math.sin((lon2_rad - lon1_rad) / 2)
    h = haversine_phi + math.cos(lat1_rad) * math.cos(lat2_rad) * sin_lon * sin_lon
    return 2 * R * math.sin(math.sqrt(h))

def rated_value(next_value, previous_value, rate):
    if rate > 0.5:
        return next_value - (next_value - previous_value) * (1 - rate)
    else:
        return previous_value + (next_value - previous_value) * rate




def create_scorelist(scores):
    answer = []
    for i in scores:
        index = i[0]
        input_string = simulated_flights_value_dict_list[index]["name"]
        pattern = r'\((.*?)\)'

        match = re.search(pattern, input_string)
        if match:
            values_str = match.group(1)
            values = [float(val.strip()) for val in values_str.split(',')]
            answer.append([index, input_string, values, i[1]])
    return answer



def create_score_dataframe(scores, mean_lists, iteration=0):
    #df = pd.DataFrame(columns=['Iteration', 'Sim Name', 'Parameters', 'Score', 'Distance mean', 'ASML mean', 'Ground Speed mean', 'Climb Rate mean'])
    df = pd.DataFrame(columns=['Iteration', 'Parameters1', 'Parameters2', 'Score', 'Distance mean', 'ASML mean', 'Ground Speed mean', 'Climb Rate mean'])
    for score in scores:
        row=[int(iteration)]
        row.extend([score[2][0],score[2][1], int(score[3])])
        for data in mean_lists:
            for i in data:
                #print(i)
                if i[1] == score[0]:
                    row.append(i[0])
                    break
        context.log(row)
        new_row = pd.DataFrame([row], columns=df.columns)
        df = pd.concat([df, new_row], ignore_index=True)
    return df


real_array = input_array_real["Data Array"]
sim_array = input_array_sim["Data Array"]



real_flight_names = list(real_array)
sim_flight_names = list(sim_array)

nparray = real_array.get(real_flight_names[0])

nparray_real = nparray.getArray()
real_flight = pd.DataFrame(data=nparray_real, columns=["timestamp (ms)","latitude ()","longitude ()","AMSL (m)","rel altitude (m)","yaw ()","ground speed (m/s)","climb rate (m/s)"])



progress_indicator_sim = input_array_sim["Progress Indicator"]

start = progress_indicator_sim.getIntOffsetIndex()
# Probably should use array.getSize()
end = len(sim_flight_names)

if end <= start:
  return 0

simulated_flight_list = []
simulated_flights_value_dict_list = []
for name in sim_flight_names[start:end]:
  if name[:14] == 'simulation_log':
    splitted_filename = name[:-4].split('_')
    distance_list_tuple = ([],[], [], [], []) 
    nparray = sim_array.get(name)
    nparray_sim = nparray.getArray()
    simulated_flight = pd.DataFrame(data=nparray_sim, columns=["timestamp (ms)","latitude ()","longitude ()","AMSL (m)","rel altitude (m)","yaw ()","ground speed (m/s)","climb rate (m/s)"])
    simulated_flight = simulated_flight.applymap(lambda value: np.format_float_scientific(float(value)) if isinstance(value, str) and 'e' in value else value)
    simulated_flight_list.append(simulated_flight)
        
    max_simulator_timestamp = simulated_flight["timestamp (ms)"].max()

    for idx, row in real_flight.iterrows():
        if max_simulator_timestamp < row["timestamp (ms)"]:
            break
        over_timestamp = simulated_flight[simulated_flight["timestamp (ms)"] > row["timestamp (ms)"]].head(1)
        under_timestamp = simulated_flight[simulated_flight["timestamp (ms)"] < row["timestamp (ms)"]].tail(1)       
        rate = (float(over_timestamp["timestamp (ms)"]) - row["timestamp (ms)"])/(float(over_timestamp["timestamp (ms)"]) - float(under_timestamp["timestamp (ms)"]))
        

        for index, value in enumerate((
                row["timestamp (ms)"] / 1000,
                distance(
                    row["latitude ()"],
                    row["longitude ()"],
                    rated_value(float(over_timestamp["latitude ()"]), float(under_timestamp["latitude ()"]), rate),
                    rated_value(float(over_timestamp["longitude ()"]), float(under_timestamp["longitude ()"]), rate),
                ),
                rated_value(float(over_timestamp["AMSL (m)"]), float(under_timestamp["AMSL (m)"]), rate) - row["AMSL (m)"],
                rated_value(float(over_timestamp["ground speed (m/s)"]), float(under_timestamp["ground speed (m/s)"]), rate) - row["ground speed (m/s)"],
                rated_value(float(over_timestamp["climb rate (m/s)"]), float(under_timestamp["climb rate (m/s)"]), rate) - row["climb rate (m/s)"]
            )):
                distance_list_tuple[index].append(value)
    # If we have at least 100 entries (timestamps) analysed, add the filename to the list
    if len(distance_list_tuple[0]) > 100:
        # Add it to the dictionary
        simulated_flights_value_dict_list.append({
            "name": name,
            "timestamp": distance_list_tuple[0],
            "distance": distance_list_tuple[1],
            "ASML" : distance_list_tuple[2],
            "ground speed" : distance_list_tuple[3],
            "climb rate" : distance_list_tuple[4]
        })



mean_list_list = []

for figure_index, (distance_list_list, limit_tuple) in enumerate((
    ([x["distance"] for x in simulated_flights_value_dict_list], (500, 600, 650)), #Distances
    ([x["ASML"] for x in simulated_flights_value_dict_list], (12.5, 14.5, 16)), #ASML
    ([x["ground speed"] for x in simulated_flights_value_dict_list], (3.1, 3.15, 3.25)), #ground speed
    ([x["climb rate"] for x in simulated_flights_value_dict_list], (0.75, 0.8, 0.85)), #climb rate
)):
    mean_list_list.append([])
    sizes = [0, 0, 0, 0]
    # For each line of the analysed sim thing we take the absolute mean of the values (distances, asml, ground speed, climb rate)
    # the figure index 
    for distance_list_index, distance_list in enumerate(distance_list_list):
        mean = mean_operation(map(abs, distance_list))
        mean_list_list[figure_index].append((mean, distance_list_index))
        if mean >= limit_tuple[-1]:
            sizes[-1] = sizes [-1] + 1
        else:
            for index, limit in enumerate(limit_tuple):
                if mean < limit:
                    sizes[index] = sizes[index] + 1


    mean_list_list[figure_index].sort()


score_dict = {}

for mean_list in mean_list_list:
    for index, (_, simulation_index) in enumerate(mean_list):
        if not simulation_index in score_dict:
            score_dict[simulation_index] = index
        else:
            score_dict[simulation_index] = score_dict[simulation_index] + index
sorted_score_list = sorted(score_dict.items(), key=lambda item: item[1])

to_plot_index = sorted_score_list[0][0]
timestamp_list = simulated_flights_value_dict_list[to_plot_index]["timestamp"]

score_list2 = create_scorelist(sorted_score_list)




zbigarray = out_array_scores["Data Array"].getArray()

if zbigarray is None:
  iteration = 1
else:
  try:
    iteration = zbigarray[-1][1] + 1 # Look at the last iteration number
  except:
    iteration = 1


df = create_score_dataframe(score_list2, mean_list_list, iteration)
dtypes = {'index': 'i8', 'Iteration': 'i8', 'Parameters1': 'f8', 'Parameters2': 'f8',
          'Score': 'f8', 'Distance_mean': 'f8', 'ASML_mean': 'f8',
          'Ground_Speed_mean': 'f8', 'Climb_Rate_mean': 'f8'}

ndarray = df.to_records(column_dtypes=dtypes, index = False)

#Uncomment this to set the array to empty
#out_array_scores["Data Array"] = out_array_scores["Data Array"].initArray(shape=(0,), dtype=ndarray.dtype.fields)

if zbigarray is None:
  zbigarray = out_array_scores["Data Array"].initArray(shape=(0,), dtype=ndarray.dtype.fields)


zbigarray.append(ndarray)


if end > start:
  progress_indicator_sim.setIntOffsetIndex(end)

if end < len(sim_flight_names):
  return 1
