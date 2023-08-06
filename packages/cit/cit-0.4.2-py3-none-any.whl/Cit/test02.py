import toml
config = toml.load('/home/kali/Documents/python/cit/pyproject.toml')
print(config['tool']['poetry']['version'])