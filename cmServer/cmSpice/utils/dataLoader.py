import os
import __main__

class CDataLoader():
    """Methods for loading data and define routes for package resources
    By defaul, all package resources are under 'data' folder in the package.
    DataLoader must be initialized before its first use.
    DO NOT USE THIS CLASS. Instead, use the Global Object called DataLoader
    """    
    def __init__(self):
        self.initialized = False
    
    def init(self, root, resourceFolderName = "data"):
        """Initializes the folder to look for resources
        """
        self.rootPath = os.path.join(os.path.dirname(root), resourceFolderName)
        self.initialized = True

    def fileRoute(self,filename):
        """Returns the absolute path to the filename in the resources folder
        It returns None if the resource route does not exist
        """
        assert(self.initialized), "DataLoader not initialized"
        route = os.path.normpath(os.path.join(self.rootPath, filename))
        return route if os.path.exists(route) else None

# Global Object for accessing resources
DataLoader = CDataLoader()