class radheefException(Exception):
# base exception class

    pass

class NotFound(radheefException):
# when the meaning for a word could not be found

	pass

class EmptyArgument(radheefException):
# when an invalid station name is passed in 

    pass
