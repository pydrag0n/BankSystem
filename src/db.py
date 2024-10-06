from peewee import *
from auth import User, Card

db = SqliteDatabase('sqlite.db')

class BaseModel(Model):
    class Meta:
        database = db

class UserModel(BaseModel):
    ID = AutoField()
    name = TextField(null=False, unique=False)

    card_num = TextField(null=True)
    card_cid = TextField(null=True)
    card_sid = TextField(null=True)
    card_cash = FloatField(null=True, default=0.0)

# Create the tables
db.create_tables([UserModel])

# Add records
# User.create(username='john', email='john@example.com')
# User.create(username='jane', email='jane@example.com')

# Update a record
# user = User.get(User.id == 1)
# user.username = 'new_username'
# user.save() This will update the existing record

# Retrieve records
# users = User.select()
# for user in users:
#     print(user.username, user.email)


# Delete a record
# User.delete().where(User.username == 'jane').execute()

# Close the database connection
# db.close()


def create_new_user(user: User):
    try:
        # Extract card details if available
        card_num = user.card.num if user.card else None
        card_cid = user.card.cid if user.card else None
        card_sid = user.card.sid if user.card else None
        card_cash = user.card.cash if user.card else None

        # Create a new user
        new_user = UserModel.create(
            ID=user.ID,
            name=user.name,
            card_num=card_num,
            card_cid=card_cid,
            card_sid=card_sid,
            card_cash=card_cash
        )
        new_user.save()
        print(f"User {user.name} created successfully.")
    except ValueError as e:
        print(f"Validation error: {e}")
    except IntegrityError as e:
        print(f"Database integrity error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

def card_is_exist(card_num: str):
    card = UserModel.select().where(UserModel.card_num == card_num)

    if card.exists():
        return True

    else: 
        return False

def update_card(user: User, new_card: Card):
    userM = UserModel.select().where(UserModel.card_num == user.card.num)
    if userM.exists():
        userM.card_num = new_card.num
        userM.card_cid = new_card.cid
        userM.card_sid = new_card.sid
        userM.card_cash = new_card.cash
        
        print("card updated...")
    else:
        print("card not found...")


def update_card_cash(user: User, new_cash: float):
    if card_is_exist(card_num=user.card.num):
        user_card = UserModel.get(UserModel.card_num == user.card.num)
        user_card.cash = new_cash
        print("card cash updated...")
    else:
        print("card not found")

