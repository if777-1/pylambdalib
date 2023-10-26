class LambdaError(Exception):
    pass
class ValuesInConflictError(LambdaError):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f'You cannot add a value that gets in conflict with another already added: {self.value}'

class ElementNotInGroupError(LambdaError):
    pass

class EnviromentVariableNotFoundError(LambdaError):
    def __init__(self, variable):
        self.variable = variable
    def __str__(self):
        return f'Enviroment variable "{self.variable}" not found.'

class IncorrectRedisUserOrPassword(LambdaError):

    def __str__(self):
        return 'Incorrect redis user or password, please change the .env file.'

class NoPermissionForRedisUser(LambdaError):
    def __init__(self, user):
        self.user = user
    def __str__(self):
        return f'User "{self.user}" has no permission to use the command.'