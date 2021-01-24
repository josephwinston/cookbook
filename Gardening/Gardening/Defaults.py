
from Gardening.DataClass import Context, Platform, DataLake
from Gardening.DataClass import User
from Gardening.DataClass import IFracFileHandle
from Gardening.DataClass import Azure
from Gardening.DataClass import ADLGen2

user: User = User(name="Power User", email="power.user@company.com")
platform: Platform = Azure()
context: Context = Context(user=user, platform=platform)
datalake: DataLake = ADLGen2()
ifracFileHandle: IFracFileHandle = IFracFileHandle(name="dummy.ifrac", lake=datalake)
