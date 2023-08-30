from typing import List, Tuple, Union, Optional


class ConverterReadings:
    """
    Class for converting readings before passing them between 'Model' and 'View'
    """

    @staticmethod
    def strs_to_ints_or_none(readings: List[str]) -> List[Optional[int]]:
        """
        input options:   ['156', '', '', ...]
        return options:  [156, None, None, ...]
        """
        new_readings = []
        for read in readings:
            if read == "":
                new_readings.append(None)
            else:
                new_readings.append(int(read))
        return new_readings

    @staticmethod
    def elec_wat_gas(values: List[Tuple]) -> List[Tuple]:
        """From the DB table to the interface table.

        input options:   [(1, 36, 17, 5.0, 85.0),
                          (2, 52, 16, 5.0, 80.0),
                          (3, 14, 'X', 5.0, 'X'), ...]

        return options:  [(1, 36, 17, '5,0', '85,00'),
                          (2, 52, 16, '5,0', '80,00'),
                          (3, 14, 'X', '5,0', 'X'), ...]
        """

        new_values = []
        for i, row in enumerate(values):
            num: int
            readings: int
            consumption: Union[int, str]
            tariff: float
            price: Union[float, str]
            num, readings, consumption, tariff, price = row

            new_tariff = str(tariff).replace(".", ",")
            new_price = str(price).replace(".", ",")
            if (new_price != "X") and (new_price[-2] == ","):
                new_price = "".join((new_price, "0",))

            new_row = (num, readings, consumption, new_tariff, new_price)
            new_values.append(new_row)

        return new_values

    @staticmethod
    def garb(values: List[Tuple]) -> List[Tuple]:
        """From the DB table to the interface table.

        input options:   [(1, 44.0), (2, 44.0), (3, 'X'), ...]
        return options:  [(1, '44,0'), (2, '44,0'), (3, 'X'), ...]
        """
        new_values = []
        for i, row in enumerate(values):
            num: int
            tariff_price: float
            num, tariff_price = row

            new_tariff_price = str(tariff_price).replace(".", ",")
            new_row = (i + 1, new_tariff_price)
            new_values.append(new_row)

        return new_values
