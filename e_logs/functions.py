from models import Guest

def set_record_to_date(model):
    from datetime import datetime
    formatter_string = "%m/%d/%y" 
    for rec in model:
        datetime_object = datetime.strptime(rec.date, "%m/%d/%y")
        rec.date = datetime_object.date()

def convert_str_to_date():
    pass

def delete_table_records(model):
    for record in model:
        record.delete()


guests = Guest.objects.all()
delete_table_records(guests)