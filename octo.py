import requests
import time

class Octoprint:

    def __init__(self, host='http://192.168.86.73', api_key='2F1129DB154543BAB9E4453057B6DD07'):
        self.base_url = host
        self.api_key = api_key
        self.printhead = self.base_url + '/api/printer/printhead'
        self.extruder = self.base_url + '/api/printer/tool'
        self.headers = { 'Content-Type': 'application/json', 'X-Api-Key': self.api_key}

    def home(self):
        command = {'command': 'jog',
                'x': 250,
                'y': 220,
                'z': 90,
                'speed': 20000,
                'absolute': True }
        r = requests.post(self.printhead, headers=self.headers, json=command)

        print('sent homing command')
        

    def move(self, old_x, old_y, new_x, new_y):
        command = {'command': 'jog',
                    'x': old_x,
                    'y': old_y,
                    'z': 60,
                    'speed': 20000,
                    'absolute': True }
        r = requests.post(self.printhead, headers=self.headers, json=command)

        command = {
            'command': 'jog',
            'z': 50,
            'speed': 50000,
            'absolute': True
        }
        r = requests.post(self.printhead, headers=self.headers, json=command)

        command = {'command': 'extrude', 'amount': 22}
        r = requests.post(self.extruder, headers=self.headers, json=command)

        command = {
            'command': 'jog',
            'z': 60,
            'speed': 50000,
            'absolute': True
        }
        r = requests.post(self.printhead, headers=self.headers, json=command)

        command = {'command': 'jog',
                    'x': new_x,
                    'y': new_y,
                    'z': 60,
                    'speed': 20000,
                    'absolute': True }
        r = requests.post(self.printhead, headers=self.headers, json=command)

        command = {
            'command': 'jog',
            'z': 50,
            'speed': 50000,
            'absolute': True
        }
        r = requests.post(self.printhead, headers=self.headers, json=command)

        command = {'command': 'extrude', 'amount': -22}
        r = requests.post(self.extruder, headers=self.headers, json=command)

        command = {
            'command': 'jog',
            'z': 60,
            'speed': 50000,
            'absolute': True
        }
        r = requests.post(self.printhead, headers=self.headers, json=command)

        self.home()

    def remove(self, old_x, old_y, new_x, new_y):
        command = {'command': 'jog',
                'x': old_x,
                'y': old_y,
                'z': 60,
                'speed': 20000,
                'absolute': True }
        r = requests.post(self.printhead, headers=self.headers, json=command)

        command = {
            'command': 'jog',
            'z': 50,
            'speed': 50000,
            'absolute': True
        }
        r = requests.post(self.printhead, headers=self.headers, json=command)

        command = {'command': 'extrude', 'amount': 22}
        r = requests.post(self.extruder, headers=self.headers, json=command)

        command = {
            'command': 'jog',
            'z': 60,
            'speed': 50000,
            'absolute': True
        }
        r = requests.post(self.printhead, headers=self.headers, json=command)

        command = {'command': 'jog',
                'x': 230,
                'y': 220,
                'z': 60,
                'speed': 20000,
                'absolute': True }
        r = requests.post(self.printhead, headers=self.headers, json=command)

        command = {'command': 'extrude', 'amount': -22}
        r = requests.post(self.extruder, headers=self.headers, json=command)

        command = {'command': 'jog',
            'x': new_x,
            'y': new_y,
            'z': 60,
            'speed': 20000,
            'absolute': True }
        r = requests.post(self.printhead, headers=self.headers, json=command)

        command = {
            'command': 'jog',
            'z': 50,
            'speed': 50000,
            'absolute': True
        }
        r = requests.post(self.printhead, headers=self.headers, json=command)

        command = {'command': 'extrude', 'amount': 22}
        r = requests.post(self.extruder, headers=self.headers, json=command)

        command = {
            'command': 'jog',
            'z': 60,
            'speed': 50000,
            'absolute': True
        }
        r = requests.post(self.printhead, headers=self.headers, json=command)

        command = {'command': 'jog',
            'x': old_x,
            'y': old_y,
            'z': 60,
            'speed': 20000,
            'absolute': True }
        r = requests.post(self.printhead, headers=self.headers, json=command)

        command = {
            'command': 'jog',
            'z': 50,
            'speed': 50000,
            'absolute': True
        }
        r = requests.post(self.printhead, headers=self.headers, json=command)

        command = {'command': 'extrude', 'amount': -22}
        r = requests.post(self.extruder, headers=self.headers, json=command)

        command = {'command': 'jog',
            'z': 60,
            'speed': 20000,
            'absolute': True }
        r = requests.post(self.printhead, headers=self.headers, json=command)

        self.home()
    
    def test(self):
        command = {'command': 'extrude', 'amount': -22}
        r = requests.post(self.extruder, headers=self.headers, json=command)
        # command = {'command': 'extrude', 'amount': dis}
        # r = requests.post(self.extruder, headers=self.headers, json=command)
        # command = {'command': 'jog',
        #     'x': 200,
        #     'y': 200,
        #     'z': 45,
        #     'speed': 200,
        #     'absolute': True }
        r = requests.post(self.printhead, headers=self.headers, json=command)




    
 
if __name__ == '__main__':

    o = Octoprint()
    