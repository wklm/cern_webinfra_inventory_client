from .inventory import Inventory
from .property import Property
from .model import Model

a = Inventory().add_instance("sharepoint", {})
quota = Inventory().deserialize_property(a['expiration_date'])
p = Property(quota)
import pdb
pdb.set_trace()

