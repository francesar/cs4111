class User():
  def __init__(self, name, uid, username, email, zipcode, hid):
    self.name = name
    self.uid = uid
    self.username = username
    self.email = email 
    self.zipcode = zipcode
    self.hid = hid

  def get_id(self):
    return self.uid

class Representative(User):
  def __init__(self, phone_number, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.phone_number = phone_number

class Citizen(User):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)