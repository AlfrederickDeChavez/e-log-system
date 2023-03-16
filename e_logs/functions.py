import time
from datetime import datetime, date, timedelta

def convert_time(value):

    """
      Converts 24-hour time format to 12 hour format.

      INPUT: '23:46'
      OUTPUT: '11:46 PM
      
    """

    time_split = value.split(":")
    label =  "PM" if int(time_split[0]) >= 12 else "AM"
    hours = int(time_split[0]) % 12 or 12

    return str(hours) + ":" + str(time_split[1]) + " " + label

def convert_str_to_time(time):

    """
      Convert string data type time value to time datatype
    """

    datetime_object = datetime.strptime(time, "%H:%M:%S")
    time = datetime_object.time()
    return time


def add_eight_hours(time):

    """
      Add eight hours to the input time.
      *** Python time is sometimes late by 8 hours.

      INPUT: '17:34:15'
      OUTPUT: '01:34:15'

    """
    time_split = time.split(":")
    hours = int(time_split[0]) % 24 if int(time_split[0]) + 8 >= 24 else int(time_split[0]) + 8

    return str(hours) + ":" + time_split[1] + ":" + time_split[2] 


def convert_task_time(time):
    
    """
      Use for old data. 
      Convert task data to 24-hour format.

      INPUT: '3:36 PM'
      OUTPUT: '15:36'
    """

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

def asset_status(asset):

    """
      Check the status of an asset to know if it is near expiration date.

      INPUT: '2023-03-31' -- March 31, 2023
      CURRENT DATE: '2023-03-09' -- March 09, 2023
      OUTPUT: 'danger'

      Asset is 22 days before expiration which is within 30 days. It is categorized as 'danger'.
    """

    today = date.today()

    datetime_object = datetime.strptime(str(asset.expiration), "%Y-%m-%d")
    expiration = datetime_object.date()

    if asset.schedule == 'Daily':
      return 'danger'

    elif asset.schedule == 'Weekly':
      if asset.current_tracking_date == today or (expiration - today).days <= 30 or (asset.next_tracking_date - today).days <= 1:
        return 'danger'
      elif (expiration - today).days <= 60 or (asset.next_tracking_date - today).days <= 2:
        return 'warning'
      elif (expiration - today).days <= 90 or (asset.next_tracking_date - today).days <= 3:
        return 'initial'
      else:
        return 'fresh'

    elif asset.schedule == 'Monthly':
      if asset.current_tracking_date == today or (expiration - today).days <= 30 or (asset.next_tracking_date - today).days <= 7:
        return 'danger'
      elif (expiration - today).days <= 60 or (asset.next_tracking_date - today).days <= 14:
        return 'warning'
      elif (expiration - today).days <= 90 or (asset.next_tracking_date - today).days <= 21:
        return 'initial'
      else:
        return 'fresh'

    elif asset.schedule == 'Yearly':
      if asset.current_tracking_date == today or (expiration - today).days <= 30 or (asset.next_tracking_date - today).days <= 30:
        return 'danger'
      elif (expiration - today).days <= 60 or (asset.next_tracking_date - today).days <= 60:
        return 'warning'
      elif (expiration - today).days <= 90 or (asset.next_tracking_date - today).days <= 90:
        return 'initial'
      else:
        return 'fresh'

    else:
      return 'fresh'

def print_all_asset(asset):
  for a in asset:
    print(a)


def is_leap(year):
  if year % 4 == 0:
    if year % 100 == 0:
      if year % 400 == 0:
        return True
    return True
  return False


def recur_asset(schedule):
  
    """
      This program returns a date to fill out the 'next_tracking_date' field of asset model.
    
      INPUT: Schedule --> 'Yearly', 'Monthly', 'Weekly', 'Daily'
      OUTPUT: Date --> 2023-03-14
    """

    if schedule =="Yearly":
      if is_leap(date.today().year): 
        next_tracking_date = date.today() + timedelta(days=366)
        return next_tracking_date
      else:
        next_tracking_date = date.today() + timedelta(days=365)
        return next_tracking_date

    elif schedule == "Monthly":
      next_tracking_date = date.today() + timedelta(days=30)
      return next_tracking_date

    elif schedule == "Weekly":
      next_tracking_date = date.today() + timedelta(days=7)
      return next_tracking_date

    elif schedule == "Daily":
      next_tracking_date = date.today() + timedelta(days=1)
      return next_tracking_date

    else:
      return date.today()


# UPDATE
def update_recur_asset(asset):

  """
    This program updates the asset model upon editing a specific record.
  
    INPUT: Schedule --> 'Yearly', 'Monthly', 'Weekly', 'Daily'
    OUTPUT: Date --> 2023-03-14 // Does not returns a value
  """

  if asset.schedule == "Yearly": 
    if is_leap(date.today().year): 
      asset.next_tracking_date = date.today() + timedelta(days=367)
      asset.save()
    else:
      asset.next_tracking_date = date.today() + timedelta(days=366)
      asset.save()

  elif asset.schedule == "Monthly":
    if date.today().month == 1 or date.today().month == 3 or date.today().month == 5 or date.today().month == 7 or date.today().month == 8 or date.today().month == 10 or date.today().month == 12:
      asset.next_tracking_date = date.today() + timedelta(days=31)
      asset.save()
    elif date.today().month == 2:
      if is_leap(date.today().year): 
        asset.next_tracking_date = date.today() + timedelta(days=29)
        asset.save()
      else:
        asset.next_tracking_date = date.today() + timedelta(days=28)
        asset.save()
    else:
      asset.next_tracking_date = date.today() + timedelta(days=30)
      asset.save()

  elif asset.schedule == "Weekly":
    asset.next_tracking_date = date.today() + timedelta(days=7)
    asset.save()

  elif asset.schedule == "Daily":
    asset.next_tracking_date = date.today() + timedelta(days=1)
    asset.save()

  else:
    return date.today()



def track_asset(asset):
  """
    This program is for updating the 'current_tracking_date' dynamically.

    If the 'current_tracking_date' is equal to date today, then the 'next_tracking_date' is updated 
    based on schedule. ('Yearly', 'Monthly', 'Weekly', 'Daily')

    If the 'current_tracking_date' is NOT equal today, then set the 'current_tracking_date' equal to 'next_tracking_date'.

  """
  if asset.current_tracking_date == date.today():
    update_recur_asset(asset)
  else:
    asset.current_tracking_date = asset.next_tracking_date
    asset.save()

def renew_asset(expiration):
  if is_leap(date.today().year):
    return expiration + timedelta(days=366)
  else:
    return expiration + timedelta(days=365)


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
       