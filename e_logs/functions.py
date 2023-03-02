import time



# Convert 24-hour time format to 12-hour format
def convert_time(value):
    time_split = value.split(":")
    label =  "PM" if int(time_split[0]) >= 12 else "AM"
    hours = int(time_split[0]) % 12 or 12

    return str(hours) + ":" + str(time_split[1]) + " " + label



# Convert string to time data object
def convert_str_to_time(time):
    datetime_object = datetime.strptime(time, "%H:%M:%S")
    time = datetime_object.time()
    return time




# Add 8 hours to Python Default Time which is 8 hours late
def add_eight_hours(time):
  time_split = time.split(":")
  hours = int(time_split[0]) % 24 if int(time_split[0]) + 8 >= 24 else int(time_split[0]) + 8

  return str(hours) + ":" + time_split[1] + ":" + time_split[2] 
# print(add_eight_hours(time.strftime("%H:%M:%S", time.localtime())))




# Iterate on a dataframe to change the string object (mm/dd/yy) to date object
# for index, row in df.iterrows():
#     datetime_object = datetime.strptime(row.date, "%m/%d/%y")
#     row.date = datetime_object.date()