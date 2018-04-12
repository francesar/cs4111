class Comment():
  def __init__(self, comment, uid, 
    topic_id, comment_id, 
    sentiment, topic_name, 
    username, vote_count,
    zipcode, date_posted, address="Dont Worry About It"):
    self.comment = comment
    self.uid = uid
    self.topic_id = topic_id
    self.comment_id = comment_id
    self.sentiment = sentiment
    self.topic_name = topic_name
    self.username = username
    self.vote_count = vote_count
    self.zipcode = zipcode
    self.date_posted = date_posted
    self.address = address
    
  @staticmethod
  def toDict(self):
    return {
      'comment':self.comment, 
      'uid':self.uid, 
      'topic_id':self.topic_id, 
      'comment_id':self.comment_id, 
      'sentiment':self.sentiment,
      'topic_name': self.topic_name,
      'username': self.username,
      'vote_count': self.vote_count,
      'zipcode': self.zipcode,
      'date_posted': self.date_posted,
      'address': self.address
    }