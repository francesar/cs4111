import jsonpickle

class Comment():
  def __init__(self, comment, uid, topic_id, comment_id, sentiment):
    self.comment = comment
    self.uid = uid
    self.topic_id = topic_id
    self.comment_id = comment_id
    self.sentiment = sentiment
    
  @staticmethod
  def toDict(self):
    return {'comment':self.comment, 'uid':self.uid, 'topic_id':self.topic_id, 'comment_id':self.comment_id, 'sentiment':self.sentiment}