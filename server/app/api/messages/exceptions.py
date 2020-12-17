# server/app/api/messages/exceptions.py


class TopicNotFound(Exception):
    """
    Raised when the topic_id provided does not exists in the database
    """
    pass
