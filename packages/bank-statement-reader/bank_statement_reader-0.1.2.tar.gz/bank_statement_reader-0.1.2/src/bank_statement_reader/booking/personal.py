from .booking_base import BookingBase


class Booking(BookingBase):
    def _set_payee(self, value: str):

        beginnings = [
            "TAZ",
            "POCO",
            "REWE",
            "Denns",
            "DEBEKA",
            "Allianz",
            "IKK",
            "Hemio",
            "OBI ",
            "DB ",
            "Rossmann",
            "Thalia",
            "Combi ",
            "Veggiemaid",
            "Die Speiche",
            "Vosgerau",
            "JunepA",
            "ADFC",
            "Casablanca",
            "BERLINER VERKEHRSBETRIEBE",
            "AMAZON",
            "Pollin",
            "Reichelt",
            "AKTIV UND IRMA",
            "KFW",
            "Thalia",
            "Willers",
            "ALFRED VOGT",
            "Fahrradstation",
            "FAHRRADZENTRUM",
        ]

        contains = {
            "SATURN": "Saturn",
            "FRISCHEMARKT": "EDEKA",
            "EDEKA": "EDEKA",
            "LIDL": "LIDL",
            "OLDENBLOC": "Oldenbloc",
            "VERKEHR + WASSER GMBH": "VWG",
            "SUPERBIOMARKT": "Superbiomarkt",
            "SHALIMAR GIR 69179274//BREMEN/DE": "InderBremen",
        }

        paypals = {
            "spotify": "Spotify",
            "MUDJEANS": "Mudjeans",
            "TAZ": "TAZ",
            "GANDI": "Gandi",
            "STIFTUNGWAR": "Stiftung Warentest",
            "KINOHELD.DE": "Kinoheld.de",
        }

        if self._wrong_type is not None:
            print("Assuming the invalid booking type is payee")
            self.comment = f"{value} {self.comment}".strip()
            value = self._wrong_type
            self._type = "Überweisung"

        for beginn in beginnings:
            if value.lower().strip().startswith(beginn.lower()):
                self._payee = beginn.strip()
                return

        for key, val in contains.items():
            if key.lower() in value.lower():
                self._payee = val
                return

        if value.startswith("PayPal"):
            # Set Booking Type correctly
            self._type = "PayPal"
            self._payee = None
            for key, val in paypals.items():
                if key.lower() in self.comment.lower():
                    self._payee = val
                    break
            if self._payee is None:
                self._payee = "PayPal"
        elif value.upper().startswith("DM FIL"):
            self._payee = "DM"
        elif "ingenico" in value.lower() and "ross" in self.comment.lower():
            self._payee = "Rossmann"
        elif "westermann+nordbro" in value.lower() and "REWE" in self.comment.upper():
            self._payee = "REWE"
        elif (
            value.startswith("CITY PIZZA") and "oldenburg" in value.lower()
        ) or value.startswith("ADNAN BALASINI"):
            self._payee = "CityVegHouse"
        elif value.startswith("FAHRRADHAUS MUNDERLOH"):
            self._payee = "Munderloh"
        elif "BIKES" in value.upper() and "OLDENBURG" in value.upper():
            self._payee = "BIKES"
        elif value.startswith("Renald Orth"):
            self._payee = "Rechtshilfekonto RoWo"
        elif value.startswith("Deutscher Alpen"):
            self._payee = "DAV"
        elif value.lower().replace(" ", "").startswith("robinwood"):
            self._payee = "Robin Wood"
        elif "wardenburg" in value.lower() and "kletter" in value.lower():
            self._payee = "UP"
        elif value.startswith("IGM Leer") or value.startswith(
            "Industriegewerkschaft Metall"
        ):
            self._payee = "Industriegewerkschaft Metall"
        else:
            self._payee = value

    def _get_category(self):
        bikes_stores = [
            "Vosgerau",
            "Die Speiche",
            "Munderloh",
            "Call a Bike",
            "Fahrradstation",
            "BIKES",
            "FAHRRADZENTRUM",
        ]
        insurances = ["IKK", "Allianz", "DEBEKA"]
        newspaper = [
            "TAZ",
            "Stiftung Warentest",
        ]
        internet = ["EWE TEL GmbH", "Posteo"]
        grocery = [
            "Combi",
            "EDEKA",
            "AKTIV UND IRMA",
            "Combi",
            "REWE",
            "Denns",
            "Superbiomarkt",
            "LIDL",
        ]
        spenden = [
            "JunepA",
            "Rechtshilfekonto RoWo",
            "Wikimedia Foerdergesellschaft",
            "Keepass",
            "Hemio",
            "Riseup Networks",
        ]
        fast_food = ["Dominos Pizza", "CityVegHouse", "Veggiemaid"]
        restaurants = [
            "SCHMIEDESCHAENKE//DRESDEN/DE",
        ]
        server = ["Hetzner Online GmbH", "Gandi"]
        vereine = [
            "DAV",
            "ADFC",
        ]  # spenden an ADFC sind absetzbar nur nicht mit gemeinnützig
        vereine_gemein = [
            "Robin Wood",
        ]
        kinos = ["Kinoheld.de", "Casablanca"]
        klettern = ["UP", "Oldenbloc", "ALFRED VOGT"]
        einrichtung = [
            "POCO",
        ]
        oepnv = ["BERLINER VERKEHRSBETRIEBE", "VWG"]
        baumarkt = ["OBI", "Willers"]
        anschaffung_sonstig = ["PayPal", "AMAZON", "Pollin", "Saturn", "Reichelt"]
        if self.type == "Bargeldabhebung":
            return "Cash Withdrawal"
        elif self.type == "Kontogebühren":
            return "Financial expenses > Bank charges"
        elif "GLS Beitrag" in self.comment:
            self.type = "Kontogebühren"
            return "Financial expenses > Bank charges"
        elif self.type == "Gehalt":
            return "Einnahmen > Gehalt"
        elif self.payee.startswith("WRD Management Support"):
            return "Einnahmen > Belegausgleich"
        elif self.payee in insurances:
            return "Insurance"
        elif self.payee in fast_food:
            return "Nahrung > Fast Food"
        elif self.payee in grocery:
            return "Nahrung > Grocery"
        elif self.payee in baumarkt:
            return "Anschaffungen > Baumarkt"
        elif self.payee in einrichtung:
            return "Anschaffungen > Einrichtung"
        elif self.payee in anschaffung_sonstig:
            return "Anschaffungen > Sonstiges"
        elif self.payee == "KFW":
            return "Loan"
        elif self.payee in server:
            return "Kommunikation > Server"
        elif self.payee in internet:
            return "Kommunikation > Internet"
        elif "congstar" in self.payee:
            return "Kommunikation > Handy"
        elif self.payee == "DB":
            return "Transport > Train"
        elif self.payee in oepnv:
            return "Transport > ÖPNV"
        elif self.payee in bikes_stores:
            return "Transport > Bike"
        elif self.payee == "cambio Oldenburg":
            return "Transport > Car Sharing"
        elif self.comment.lower().strip().startswith("spende") or self.payee in spenden:
            return "Schenkungen > Spende"
        elif self.comment.lower().strip().startswith("fahrtkostenerstattung"):
            return "Transport > Fahrtkostenerstattung"
        elif self.payee == "Industriegewerkschaft Metall":
            return "Mitgliedschaften > Gewerkschaft"
        elif self.payee.startswith("SPD"):
            return "Mitgliedschaften > Parteien"
        elif self.payee in vereine:
            return "Mitgliedschaften > Vereine"
        elif self.payee in vereine_gemein:
            return "Mitgliedschaften > Gemeinützige Vereine"
        elif self.payee == "Spotify":
            return "Leisures > Music"
        elif self.payee == "Mudjeans":
            return "Care > Clothing"
        elif self.payee == "DM" or self.payee == "Rossmann":
            return "Care > Careproducts"
        elif "APOTHEKE" in self.payee.upper():
            return "Health > Chemist"
        elif self.payee in newspaper:
            return "Education > Newspaper"
        elif self.payee == "Thalia":
            return "Education > Books"
        elif self.payee.startswith("AMAZON INSTANT VIDEO") or self.payee.startswith(
            "Commdoo"
        ):
            return "Leisure > Video > Home"
        elif self.payee in kinos:
            return "Leisure > Video > Kino"
        elif self.payee in klettern:
            return "Sport > Klettern"
        elif (
            self.payee == "Norman Carl Freudenberg"
            and self.type == "Überweisung"
            or self.payee.startswith("SoWo Leipzig eG")
        ):
            return "Internal Transfer"
        elif "miete" in self.comment.lower():
            return "Miete"
        elif "Stefanie Rosemann" in self.payee:
            return "Health > Psychological"
        elif (
            "Inder" in self.payee
            and "Bremen" in self.payee
            or self.payee.strip() in restaurants
        ):
            return "Nahrung > Restaurant"
        elif "JET TANKSTELLEN DEUTSCHLAND" in self.payee and "OL" in self.comment:
            return "Leisures > Mate"
        elif "GC re study clever GmbH" in self.payee:
            return "Taxes"
        else:
            return ""
