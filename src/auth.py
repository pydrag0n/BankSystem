import db

class Card:
    def __init__(self, num: str, cid: str, sid: str, cash: float=0.0):

        if not self.validate_card_number(num):
            raise ValueError("Invalid card number format")
        if not self.validate_cid(cid):
            raise ValueError("Invalid CID format")
        if not self.validate_sid(sid):
            raise ValueError("Invalid SID format")
        if not self.validate_cash(cash):
            raise ValueError("Invalid CASH format")

        self.__num = num
        self.__cid = cid
        self.__sid = sid
        self.__cash = cash


    def validate_card_number(self, num: str):
        # Remove any non-digit characters
        num = ''.join(filter(str.isdigit, num))

        # Check length
        if len(num) < 13 or len(num) > 16:
            return False

        # Apply Luhn algorithm
        def luhn_check(card_number):
            def digits_of(n):
                return [int(d) for d in str(n)]
            digits = digits_of(card_number)
            odd_digits = digits[-1::-2]
            even_digits = digits[-2::-2]
            checksum = sum(odd_digits)
            for d in even_digits:
                checksum += sum(digits_of(d*2))
            return checksum % 10 == 0

        return luhn_check(num)

    def validate_cid(self, cid: str):
        # Example validation: 3 digits
        return len(cid) == 3 and cid.isdigit()

    def validate_sid(self, sid: str):
        # Example validation: 3 digits
        return len(sid) == 3 and sid.isdigit()

    def validate_cash(self, cash: float):

        if cash >= 0.0:
            return True
        else:
            return False

    @property
    def num(self):
        return self.__num

    @property
    def cid(self):
        return self.__cid

    @property
    def sid(self):
        return self.__sid

    @property
    def cash(self):
        return self.__cash


class User:
    def __init__(self, name: str, password: str, card: Card=None):
        # self.ID = ID
        self.name = name
        self.password = password
        self.card = card


class UserManager:
    def register(self, user: User, confirm_password: str):
        if user.password != confirm_password:
            return "IncorrectPasswords", False
        if db.user_is_exists(user.name):
            return "UserAlreadyExists", False
        else:
            db.create_new_user(user)
            return "Registered", True

    def authenticate(self, user: User,):
        if db.user_is_exists(user.name):
            
            if db.get_user_password(user.name) == user.password:
                return "Authenticated", True
            else:
                return "IncorrectPassword", False
        else:
            print(user.name)
            print(db.user_is_exists(user.name))
            return "IncorrectUsernameOrPassword", False
