ammoType = {
    '1': 'Piercing',
    '2': 'Explosive',
    '3': 'AT'
}

class Artillery:
    def __init__(self):
        self.charger = []
        self.max_capacity = 3

    def reload(self):
        if len(self.charger) >= self.max_capacity:
            print("The charger is full! Can't load more ammo.")
            return
        
        print("Available ammo types:", ammoType)
        
        i = 0
        bulletType = input("Select a bullet type: ")
        
        while bulletType not in ammoType and i < 4:
            print("That's not a bullet type soldier, try again.")
            bulletType = input("Select a bullet type: ")
            i += 1
        
        if bulletType in ammoType:
            self.charger.append(ammoType[bulletType])
            print("Loading:", self.charger)
        else:
            print("You failed to select a valid bullet after 3 tries!")

    def shoot(self):
        if self.charger:
            bullet = self.charger.pop()
            print(f"You have shot a {bullet} bullet!")
        else:
            print("There is no ammo in the charger.")

APA = Artillery()
APA.reload()
APA.reload()
APA.reload()
APA.shoot()
APA.shoot()
APA.shoot()