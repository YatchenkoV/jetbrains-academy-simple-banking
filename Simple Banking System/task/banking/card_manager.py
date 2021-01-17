import random
import string


class CreditCardManager:
    IIN = '400000'

    @classmethod
    def generate_credit_card(cls) -> tuple:
        return cls._generate_card_number(), cls._generate_pin()

    @staticmethod
    def _generate_pin() -> str:
        return ''.join(random.choices(string.digits, k=4))

    @classmethod
    def _generate_card_number(cls) -> str:
        generated_number = cls.IIN + ''.join(random.choices(string.digits, k=9))
        return generated_number + str(cls._get_checksum(generated_number))

    @classmethod
    def check_card_number_validity(cls, card_number: str):
        checksum: int = cls._get_checksum(card_number[:-1])
        return checksum == int(card_number[-1])

    @staticmethod
    def _get_checksum(code: str) -> int:
        """
        Counts checksum for card number using Lunh algorithm
        :param code:
        :return:
        """
        total = 0

        for index, digit in enumerate(code):
            digit = int(digit)
            if (index + 1) % 2 != 0:
                digit *= 2
                if digit > 9:
                    digit -= 9
            total += digit

        checksum = 10 - total % 10

        return checksum if checksum != 10 else 0

