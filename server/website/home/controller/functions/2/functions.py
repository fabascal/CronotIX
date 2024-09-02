class Functions:
    def get_product_price(product: str):
        data = {
                "rancho":{
                "Gasolina menor a 92 octanos": 18.95,
                "Gasolina mayor a 92 octanos": 19.95,
                "Diesel": 17.95
                },
                "central":{
                "Gasolina menor a 92 octanos": 19.95,
                "Gasolina mayor a 92 octanos": 110.95,
                "Diesel": 18.95
                },
                "mega":{
                "Gasolina menor a 92 octanos": 110.95,
                "Gasolina mayor a 92 octanos": 111.95,
                "Diesel": 19.95
                },
                "la laja":{
                "Gasolina menor a 92 octanos": 110.95,
                "Gasolina mayor a 92 octanos": 111.95,
                "Diesel": 19.95
                },
            }
        return data