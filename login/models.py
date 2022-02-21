from django.db import models

# Create your models here.
class event:
    ev_id=None
    ev_name=None
    date=None
    time=None
    seats_req=None
    org_by=None
    price=None
    seat=None

class department:
    Dname=None
    mgrname=None
    phone=None
    mail=None