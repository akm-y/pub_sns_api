from django.contrib import admin
from .models import User
from .models import Friend
from .models import Mediate
from .models import Team
from .models import Member
from .models import News
from .models import Entry
from .models import EntryCategory
from .models import TranLikes

# Register your models here.
admin.site.register(User)
admin.site.register(Friend)
admin.site.register(Mediate)
admin.site.register(Member)
admin.site.register(News)
admin.site.register(Entry)
admin.site.register(EntryCategory)
admin.site.register(TranLikes)
admin.site.register(Team)

