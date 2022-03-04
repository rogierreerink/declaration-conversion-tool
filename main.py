from argparse import ArgumentParser
from argparse import FileType
from pandas import DataFrame, read_csv


class Converter:
    __input = None
    __input_df = None
    __input_cols = [
        'Datum', 'Check in', 'Vertrek', 'Check uit', 'Bestemming', 'Af', 'Bij',
        'Transactie', 'Kl', 'Product', 'Prive/ Zakelijk', 'Opmerking']

    __output = None
    __output_df = None
    __output_cols = [
        'Datum', 'Check-in', 'Vertrek', 'Check-uit', 'Bestemming', 'Bedrag',
        'Transactie', 'Klasse', 'Product', 'Opmerkingen', 'Naam', 'Kaartnummer']

    __column_mapping = {
        __input_cols[0]: __output_cols[0],  # Datum
        __input_cols[1]: __output_cols[1],  # Check-in
        __input_cols[2]: __output_cols[2],  # Vertrek
        __input_cols[3]: __output_cols[3],  # Check-uit
        __input_cols[4]: __output_cols[4],  # Bestemming
        __input_cols[5]: __output_cols[5],  # Af -> Bedrag
        __input_cols[7]: __output_cols[6],  # Transactie
        __input_cols[8]: __output_cols[7],  # Kl -> Klasse
        __input_cols[9]: __output_cols[8],  # Product
    }

    __name = None
    __card = None

    def __init__(self, input, output):
        self.__input = input
        self.__output = output

    def __convert(self):
        self.__input_df = read_csv(self.__input, encoding='utf-8')
        self.__input_df.rename(
            columns=self.__column_mapping, inplace=True)

        self.__output_df = DataFrame(
            self.__input_df, columns=self.__output_cols)
        self.__output_df.sort_values(by=[
            self.__output_cols[0],
            self.__output_cols[1],
        ], inplace=True)

        # Remove euro sign, transform string formatted costs into float
        self.__output_df['Bedrag'] = self.__output_df[self.__output_cols[5]].str.replace(
            'â‚¬', '').str.replace(',', '.').astype(float)

        if self.__name != None:
            self.__output_df[self.__output_cols[10]] = self.__name

        if self.__card != None:
            self.__output_df[self.__output_cols[11]] = self.__card

    def __save(self):
        self.__output_df.to_csv(
            self.__output, index=False, sep=';', decimal=',', quoting=1,
            line_terminator="\n")

    def setName(self, name):
        self.__name = name

    def setCard(self, card):
        self.__card = card

    def run(self):
        self.__convert()
        self.__save()


if __name__ == '__main__':

    args = ArgumentParser()
    args.add_argument(
        'in', help='the source declaration file (NS CSV)', type=FileType('r'))
    args.add_argument(
        'out', help='the output declaration file (OV-Chipkaart CSV)', type=FileType('w'))
    args.add_argument(
        '--name', help='set the card holders name', nargs='?', type=str)
    args.add_argument(
        '--card', help='set the card number', nargs='?', type=str)
    args = vars(args.parse_args())

    conv = Converter(args["in"], args["out"])
    if "name" in args:
        conv.setName(args["name"])
    if "card" in args:
        conv.setCard(args["card"])
    conv.run()
