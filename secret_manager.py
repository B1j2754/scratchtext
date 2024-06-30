def get_key(key):
    with open('SECRETS.txt','r') as file:
        for line in file:
            if line.startswith(key):
                return line.split('=',1)[1]
    return None