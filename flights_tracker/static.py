from enum import Enum


class SearchTypes(str, Enum):
    FLEXI = "flexi"


class UnknownParam(int, Enum):
    ZERO = 0


class IsOneway(str, Enum):
    NO = "return"


class PolishAirports(str, Enum):
    WMI = "WMI"
    WAW = "WAW"
    GDN = "GDN"
    BZG = "BZG"
    LCJ = "LCJ"
    LUZ = "LUZ"
    POZ = "POZ"
    KRK = "KRK"
    KTW = "KTW"
    RZE = "RZE"
    SZZ = "SZZ"
    WRO = "WRO"

    @classmethod
    def get_all_airports(cls):
        return [airport.value for airport in PolishAirports]

    @classmethod
    def get_srcap_parameter(cls):
        return "&".join([f"srcap{id_}={airport}" for id_, airport in enumerate(PolishAirports.get_all_airports())])


class CountryCodes(str, Enum):
    POLAND = "PL"


class AZairBool(str, Enum):
    TRUE = "true"
    FALSE = "false"


class Weekdays(str, Enum):
    MONDAY = "monday"
    TUESDAY = "tuesday"
    WEDNESDAY = "wednesday"
    THURSDAY = "thursday"
    FRIDAY = "friday"
    SATURDAY = "saturday"
    SUNDAY = "sunday"

    @classmethod
    def get_all_weekdays(cls):
        return [weekday.value for weekday in Weekdays]

    @classmethod
    def get_departure_for_all_days(cls):
        return "&".join([f"dep{id_}={AZairBool.TRUE}" for id_, _ in enumerate(Weekdays.get_all_weekdays())])

    @classmethod
    def get_arrival_for_all_days(cls):
        return "&".join([f"arr{id_}={AZairBool.TRUE}" for id_, _ in enumerate(Weekdays.get_all_weekdays())])


class Currency(str, Enum):
    EURO = "EUR"
