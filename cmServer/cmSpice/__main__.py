# from cmSpice.apiServer import run


# local modules
import cmSpice.apiServer.init as initialization
import cmSpice.apiServer.server as apiServer
from cmSpice.utils.dataLoader import DataLoader



# For now, we are not using it
# removeData()
# importData()

# To prepare things
# clearDatabase()
# initializeDatabase()
# importDatabase()

DataLoader.init(__file__)

# init db/cm
initialization.clearDatabase()

# run
apiServer.run()
