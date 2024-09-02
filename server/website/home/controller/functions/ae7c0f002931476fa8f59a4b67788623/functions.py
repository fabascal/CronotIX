class Functions:
    
    def get_company_data(company: str):
        data = {
            "razon social": "Combu-Express",
            "nombre comercial": "Ener",
            "grupo": "Enersi",
            "descripcion":"Combu Express es un grupo gasolinero 100% mexicano el cual se constituye el 21 de septiembre de 1998, en Guadalajara, Jalisco.",
            "mision":"Satisfacer las necesidades cotidianas de productos y servicios gasolineros de nuestros clientes de una manera amable, rápida, práctica y confiable. Estar siempre cuidadosos del medio ambiente, la seguridad y la limpieza; Promoviendo el desarrollo integral de nuestros empleados y la comunicación abierta a todos los niveles de la organización.",
            "vision":"Ser el Grupo Gasolinero líder a nivel nacional en materia de control en el consumo de combustible, ofreciendo diferentes ubicaciones estratégicas con la más alta tecnología implementada en beneficios de nuestros clientes.",
            "valores":{
                "HONESTIDAD":"Ser SIEMPRE honestos con nuestros clientes dándoles un trato justo y procurando el cuidado de sus autos y de su economía en cada visita.",
                "RAPIDEZ":"Estamos conscientes de que el tiempo es MUY valioso para nuestros clientes, por lo que SIEMPRE los atendemos de inmediato al llegar y procuramos que NUNCA pierdan tiempo innecesariamente.",
                "DISPONIBILIDAD":"Estamos al pendiente de nuestros clientes en todo momento y NUNCA los dejamos de atender mientras estén en nuestras estaciones.",
                "AMABILIDAD":"SIEMPRE somos corteses con nuestros clientes; SIEMPRE los saludamos amablemente al llegar, los atendemos con gusto y los despedimos amablemente al retirarse."
                },
            "SERVICIOS":"TIENDA DE CONVENIENCIA, BAÑOS PÚBLICOS, FACTURACIÓN ELÉCTRONICA, PAGO CON TARJETA BANCARIA, Venta y asesoría de aditivos y aceites, Personal capacitado para dar la atención al cliente mas ágil y completa, Dispensadores de Aire y Agua",
            "TERMINALES PUNTO DE VENTA":"Ticket Car, Accor, Efectivale, CGI",
            "contactos":{
                "zona bajio":{
                    "calle":"Av. Constituyentes N° 296 Col. Jacarandas Celaya-Guanajuato C.P. 38090",
                    "telefono": "4613778867"
                },
                "zona occidente":{
                    "calle":"Carretera Guadalajara-Nogales N° 6755 Zapopan, Jalisco C.P. 45010",
                    "telefono": "3316010433"
                },
                "zona occidente sur":{
                    "calle":"Av. Gobernador Alberto Cárdenas Jiménez N° 692 Col. Centro CD. Guzmán Jalisco C.P. 49000",
                    "telefono": "3411657487"
                },
                "Mayoreo Enersi":{
                    "calle":"Carretera Ixpata-Las Juntas KM 1.8 Puerto Vallarta, Jalisco C.P. 48280",
                    "telefono": "(33) 3121-2120"
                },
            }
            
        }
        return data
            
    def get_address_data(startLat: str, startLong: str):
        data = {
            "rancho": {
                "lat": "20.718072",
                "long": "-103.483769",
                "state": "Jalisco",
                "municipality": "Zapopan",
                "direccion":{
                    "estado": "Jalisco",
                    "municipio": "Zapopan",
                    "calle": "Carretera Guadalajara-Nogales",
                    "numero":"6755",
                    "cp": "45010"},
                },
            "central": {
                "lat": "20.617247",
                "long": "-103.254364",
                "state": "Jalisco",
                "municipality": "Guadalajara",
                "direccion":{
                    "estado": "Jalisco",
                    "municipio": "Guadalajara",
                    "calle": "Av. tonala",
                    "numero":"2055",
                    "colonia": "Cd. Aztlan Tonala",
                    "cp": "45410"},
            },
            "mega": {
                "lat": "19.682963",
                "long": "-103.486692",
                "state": "Jalisco",
                "municipality": "Zapotlan el grande",
                "direccion":{
                    "estado": "Jalisco",
                    "municipio": "Zapotlan el grande",
                    "calle": "Libramiento Carretero Sur Pte.",
                    "numero":"143",
                    "colonia":"CD. Guzmán",
                    "cp": "45010"},
            },
            "la laja": {
                "lat": "20.524713",
                "long": "-100.815324",
                "state": "Celaya",
                "municipality": "Celaya",
                "direccion":{
                    "estado": "Celaya",
                    "municipio": "Celaya",
                    "calle": "Carretera Panamericana Querétaro-Celaya Km. 47",
                    "numero":"S/N",
                    "colonia":"Rancho Nuevo ",
                    "cp": "38160"},
            }
        }               
        return data
        
    def get_product_price(product: str):
        data = {
                "rancho":{
                "Gasolina menor a 92 octanos": 8.95,
                "Gasolina mayor a 92 octanos": 9.95,
                "Diesel": 7.95
                },
                "central":{
                "Gasolina menor a 92 octanos": 9.95,
                "Gasolina mayor a 92 octanos": 10.95,
                "Diesel": 8.95
                },
                "mega":{
                "Gasolina menor a 92 octanos": 10.95,
                "Gasolina mayor a 92 octanos": 11.95,
                "Diesel": 9.95
                },
                "la laja":{
                "Gasolina menor a 92 octanos": 10.95,
                "Gasolina mayor a 92 octanos": 11.95,
                "Diesel": 9.95
                },
            }
        return data

    def get_credit(razon_social:str):
        data = {
            "razon social": razon_social,
            "monto": 85000,
            "plazo": 1,
            "tasa": 10,
            "pago": 1000
        }
        return data
    
    def get_last_ticket(razon_social:str):
        data = {
            "razon social": razon_social,
            "tickets" : [
                {
                    "folio": 1234,
                    "fecha": "2021-08-01",
                    "hora": "12:00",
                    "total": 1000
                },
                {
                    "folio": 1235,
                    "fecha": "2021-08-02",
                    "hora": "12:00",
                    "total": 2000
                },
                {
                    "folio": 1236,
                    "fecha": "2021-08-03",
                    "hora": "12:00",
                    "total": 3000
                }
            ],
            "granTotal": 6000
        }
        return data
    
    def get_cfdi(rfc:str, razon_social:str, codigo_postal:str, regimen:str, uso_cfdi:str, metodo_pago:str, email:str):
        
        data = {
            "rfc": rfc,
            "razon social": razon_social,
            "codigo postal": codigo_postal,
            "regimen": regimen,
            "uso cfdi": uso_cfdi,
            "metodo de pago": metodo_pago,
            "email": email,
            "uuid": str(uuid.uuid4())
        }
        return data
