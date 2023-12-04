import requests

class API:
    def __init__(self):
        CITY = "Santiago de cali"
        URL = f"https://es.wttr.in/{CITY}?format=j1"
        
        try:
            self.response = requests.get(URL).json()
        except requests.exceptions.ConnectionError:
            print("Error al conectar con a API")

    # Imprime los dias con su horas.
    def dias_horas(self):
        for j in range(0,3):
            try:
                date = self.response["weather"][j]["date"]
            except:
                date = '-'
            print(date)
            print(f"******************** Dia {j} ********************\n")
            for i in range(3,8):
                try:
                    temp = self.response["weather"][j]["hourly"][i]
                except:
                    temp = 'Null'
                if i != 5:
                    print(f"============================ Hora {i} ============================")
                    print(temp)
                    print()
    
    # Retorna el pronostico de los dias con sus horas.
    def pronostico_dia(self, dia, hora):

        try:
            codigo = int(self.response["weather"][dia]["hourly"][hora]["weatherCode"])
            tiempo = int(self.response["weather"][dia]["hourly"][hora]["time"])
            if tiempo >= 1200:
                tiempo = f"{tiempo // 100 - 10}:00 PM"
            else:
                tiempo = f"{tiempo // 100}:00 AM"

            temp = self.response["weather"][dia]["hourly"][hora]["tempC"]
            temp_se_siente = self.response["weather"][dia]["hourly"][hora]["FeelsLikeC"]
            if temp_se_siente == temp:
                temp_se_siente = ""
            else:
                temp_se_siente = f"({temp_se_siente})"

            descripcion = str(self.response["weather"][dia]["hourly"][hora]["lang_es"][0]["value"])
            descripcion.capitalize

            precipitaciones = self.response["weather"][dia]["hourly"][hora]["precipInches"]
            humedad = self.response["weather"][dia]["hourly"][hora]["humidity"]
        except:
            codigo = 0
            pronostico = 'Null'
            return pronostico, codigo
        
        pronostico = f"{tiempo} \n{temp}{temp_se_siente} °C \n{descripcion} \nH.{humedad}% | P.{precipitaciones}%"

        return pronostico, codigo

    # Retorna el pronostico actual.
    def pronostico_actual(self):

        try:
            codigo = self.response["current_condition"][0]["weatherCode"]
            temp = self.response["current_condition"][0]["temp_C"]
            temp_se_siente = self.response["current_condition"][0]["FeelsLikeC"]
            if temp_se_siente == temp:
                temp_se_siente = ""
            else:
                temp_se_siente = f"({temp_se_siente})"

            descripcion = str(self.response["current_condition"][0]["lang_es"][0]["value"])
            descripcion.capitalize

            precipitaciones = self.response["current_condition"][0]["precipInches"]
            humedad = self.response["current_condition"][0]["humidity"]
        except:
            codigo = 0
            pronostico = 'Null'
            return pronostico, codigo

        pronostico = f"{temp}{temp_se_siente} °C \n{descripcion} \nH.{humedad}% | P.{precipitaciones}%"

        return pronostico, codigo

    # Hace el cambio de fecha.
    def fecha(self, dia=-1):

        def cambiar_mes(mes) :

            mes = int(mes)

            if int(mes) == 1:
                return "Enero"
            elif int(mes) == 2:
                return "Febrero"
            elif int(mes) == 3:
                return "Marzo"
            elif int(mes) == 4:
                return "Abril"
            elif int(mes) == 5:
                return "Mayo"
            elif int(mes) == 6:
                return "Junio"
            elif int(mes) == 7:
                return "Julio"
            elif int(mes) == 8:
                return "Agosto"
            elif int(mes) == 9:
                return "Septiembre"
            elif int(mes) == 10:
                return "Octubre"
            elif int(mes) == 11:
                return "Noviembre"
            else:
                return "Diciembre"

        try:
            if dia == -1:
                fecha = self.response["current_condition"][0]["localObsDateTime"].split("-")
                fecha[2] = fecha[2].split(" ")

                aux = fecha[2]
                fecha[2] = fecha[2][0]
                aux.pop(0)
                fecha[0] = f"{fecha[0]} - {aux[0]} {aux[1]}"
            else:
                fecha = self.response["weather"][dia]["date"].split("-")
                fecha[2] = int(fecha[2])
        except:
            return f"- / - / -"

        fecha_actual = f"{cambiar_mes(fecha[1])} / {fecha[2]} / {fecha[0]}"
        
        return fecha_actual