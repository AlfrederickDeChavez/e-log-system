import time
from datetime import datetime


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


# Convert task time to 24-hour format
def convert_task_time(time):
    if 'PM' in time:
      time_split = time.split(":")
      hour = "00" if (int(time_split[0]) + 12) == 24 else int(time_split[0]) + 12
      sec = time_split[2][:-2]
      return str(hour) + ":" + time_split[1] + ":" + sec.strip()

    elif 'AM' in time:
      time_split = time.split(":")
      hour = '00' if time_split[0] == "12" else time_split[0]

      return hour + ":" + time_split[1] + ":" + time_split[2].strip()[:-2].strip()

    else:
      return "00:00:00"


# Iterate on a dataframe to change the string object (mm/dd/yy) to date object
# for index, row in df.iterrows():
#     datetime_object = datetime.strptime(row.date, "%m/%d/%y")
#     row.date = datetime_object.date()


# Migrate evening task dataset
# df = pd.read_csv('e_logs\dataset\e_logs_evening_task.csv')
# for index, row in df.iterrows():
#     datetime_object = datetime.strptime(row.pldate, "%m/%d/%y")
#     row.pldate = datetime_object.date()

#     EveningTask.objects.create(
#         date = row.pldate,
#         time = convert_str_to_time(convert_task_time(row.pltime)),
#         checked_by = row.plname,
#         t_dsob = convert_str_to_time(convert_task_time(row.pcirsstm)),
#         r_dsob = row.dcirsstm,
#         t_ceu = convert_str_to_time(convert_task_time(row.pceu)),
#         r_ceu = row.dceu,
#         t_cass = convert_str_to_time(convert_task_time(row.pcass)),
#         r_cass = row.dcass,
#         t_uebu = convert_str_to_time(convert_task_time(row.puebu)),
#         r_uebu = row.duebu,
#         t_alicbu = convert_str_to_time(convert_task_time(row.pcgsist)),
#         r_alicbu = row.dcgsist,
#         t_ciss = convert_str_to_time(convert_task_time(row.pciss)),
#         r_ciss = row.dciss,
#         t_cpss = convert_str_to_time(convert_task_time(row.pcpss)),
#         r_cpss = row.dcpss,
#         t_ccrgt = convert_str_to_time(convert_task_time(row.pccrlst)),
#         r_ccrgt = row.dccrlst,
#         t_cvti = convert_str_to_time(convert_task_time(row.pcvic)),
#         r_cvti = row.dcvic,
#         t_ltos = convert_str_to_time(convert_task_time(row.plogout)),
#         r_ltos = row.plogout,
#     )


# Migrate evening task dataset
 # for index, row in df.iterrows():
        #     datetime_object = datetime.strptime(str(row.aldate), "%m/%d/%y")
        #     row.aldate = datetime_object.date()

        #     try:
        #         MorningTask.objects.create(
        #             date = row.aldate,
        #             time = convert_str_to_time(convert_task_time(row.altime)),
        #             checked_by = row.alname,
        #             t_lits = convert_str_to_time(convert_task_time(row.altis)),
        #             r_lits = row.bltis,
        #             t_ciss = convert_str_to_time(convert_task_time(row.aciss)),
        #             r_ciss = row.bciss,
        #             t_cass = convert_str_to_time(convert_task_time(row.acass)),
        #             r_cass = row.bcass,
        #             t_cebu = convert_str_to_time(convert_task_time(row.acebu)),
        #             r_cebu = row.bcebu,
        #             t_boas = convert_str_to_time(convert_task_time(row.aboas)),
        #             r_boas = row.bboas,
        #             t_cwrge = convert_str_to_time(convert_task_time(row.acwrg)),
        #             r_cwrge = row.bcwrg,
        #             t_utbeb = convert_str_to_time(convert_task_time(row.arpmp)),
        #             r_utbeb = row.brpmp,
        #             t_alicbu = convert_str_to_time(convert_task_time(row.acirsstm)),
        #             r_alicbu = row.bcirsstm,
        #             t_ceu = convert_str_to_time(convert_task_time(row.aceu)),
        #             r_ceu = row.bceu,
        #             t_cdl = convert_str_to_time(convert_task_time(row.acdml)),
        #             r_cdl = row.bcdml,
        #             t_cvti = convert_str_to_time(convert_task_time(row.acvic)),
        #             r_cvti = row.bcvic,
        #             t_cppc = convert_str_to_time(convert_task_time(row.acppc)),
        #             r_cppc = row.bcppc,
        #             t_ccrgt = convert_str_to_time(convert_task_time(row.acrlst)),
        #             r_ccrgt = row.bcrist,
        #         )

        #     except: 
        #         print(index)
        #         break
       