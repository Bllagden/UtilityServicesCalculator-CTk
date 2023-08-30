from typing import List, Tuple, Optional


class ConverterTariffs:
    """
    Class for converting tariffs before passing them between 'Model' and 'View'
    """

    @staticmethod
    def str_to_float(tariff_value: str) -> float:
        """
        input options:   '5' | '5.0' | '5.32' | '5,0' | '5,32'
        return options:  5.0 |  5.0  |  5.32  |  5.0  |  5.32
        """
        new_value = tariff_value
        if "," in new_value:
            new_value = new_value.replace(",", ".")

        if new_value[-1] == ".":
            new_value = "".join((new_value, "0"))

        return float(new_value)

    @staticmethod
    def strs_to_floats_or_none(tariffs: List[str]) -> List[Optional[float]]:
        """
        input options:   ['3,28', '', '', ...]
        return options:  [3.28, None, None, ...]
        """
        new_tariffs = []
        for tar in tariffs:
            if tar == "":
                new_tariffs.append(None)
            else:
                replace_tar = tar.replace(",", ".")
                new_tariffs.append(float(replace_tar))
        return new_tariffs

    @staticmethod
    def floats_to_strs(tariffs: List[float]) -> List[str]:
        """
        input options:   [5.32, 5.0, 0.0]        |  [0.0]
        return options:  ['5,32', '5,0', '0,0']  |  ['0,0']
        """
        new_tariffs = list(map(str, tariffs))
        new_tariffs = [tar.replace(".", ",") for tar in new_tariffs]
        return new_tariffs

    @staticmethod
    def floats_to_strs_in_tuples(data: List[Tuple[str, float]]) \
            -> List[Tuple[str, str]]:
        """
        input options:   [('elec', 4.0), ('wat', 3.28)]
        return options:  [('elec', '4,0'), ('wat', '3,28')]
        """
        new_data = []
        for row in data:
            tariff_type: str
            tariff_value: float
            tariff_type, tariff_value = row

            new_value = str(tariff_value).replace(".", ",")
            new_data.append((tariff_type, new_value))

        return new_data
