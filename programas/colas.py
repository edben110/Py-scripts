airplanes={
    '1':'Sukoi 37',
    '2':'F18',
    '3':'Kfir',
    '4':'D Rafale'
}

class AirplaneCarrier:
    
    def __init__(self):
        self.refueling_Platform=[]
    
    def giveRefuelOrder(self):
        if len(self.refueling_Platform)>=2:
            print('the queue is full, please wait...')
            
        print('available planes to refuelin: ',airplanes)
        
        i=0
        aircraft_Permission=input('what aircraft must refuel?: ')
        
        while aircraft_Permission not in airplanes and i <2:
            print('that´s not a plane model sir, chose one again' )
            aircraft_Permission=input('what aircraf must refuel?: ')
        
        if aircraft_Permission in airplanes:
            self.refueling_Platform.append(airplanes[aircraft_Permission])
            print(self.refueling_Platform[-1],' landing...')
            i+=1
        
    def refuel(self):
        if self.refueling_Platform:
            refill = self.refueling_Platform.pop(0)
            print(f"the aircraft {refill} its full")
        else:
            print('there are not planes in the refueling platform')

titan = AirplaneCarrier()
titan.giveRefuelOrder()
titan.giveRefuelOrder()
titan.refuel()
titan.refuel()
            
        