import servers
import re

products = [servers.Product('P12', 1), servers.Product('PP234', 2), servers.Product('PP235', 1)]
serv = servers.MapServer(products)
m = serv.get_entries(2)
print(m)