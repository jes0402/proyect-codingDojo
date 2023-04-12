import decimal



def getPriceSize(size):
    pequena = decimal.Decimal(10.00)
    mediana = decimal.Decimal(13.00)
    grande = decimal.Decimal(15.00)

    if size == "Small":
        return pequena
    if size == "Medium":
        return mediana
    if size == "Large":
        return grande
    return 0
        
def getPriceCrust(crust):
    thick = decimal.Decimal(1.5)
    thin = decimal.Decimal(0.5)   
    if crust == "Thick Crust":
            return thick
    if crust == "Thin Crust":
            return thin
    return 0

usd = 800