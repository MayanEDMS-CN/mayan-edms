from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import requests


class Command(BaseCommand):
    help = "与C4C同步用户"

    def add_arguments(self, parser):
        parser.add_argument("host", type=str)               # my500248
        parser.add_argument("username", type=str)           # ZSKZSK7000055
        parser.add_argument("password", type=str)           # Welcome1

    def handle(self, *args, **options):
        host = options["host"]
        username = options["username"]
        password = options["password"]
        url = "https://%s:%s@%s.c4c.saphybriscloud.cn/sap/c4c/odata/v1/c4codata/EmployeeCollection?$format=json" % (
            username, password, host
        )
        result = requests.get(url).json()
        for item in result["d"]["results"]:
            firstname = item["FirstName"]
            lastname = item["LastName"]
            userid = item["UserID"]
            token = item["ObjectID"]
            if len(userid) > 0:
                userid = userid.upper()
                user = User.objects.filter(username=userid).first()
                if user is not None:
                    if not user.check_password(token):
                        user.set_password(token)
                        print("user [%s] password updated." % user.username)
                else:
                    user  = User.objects.create_user(userid, password=token)
                    user.first_name = firstname
                    user.last_name = lastname
                    user.save()
                    print("user [%s] created." % userid)