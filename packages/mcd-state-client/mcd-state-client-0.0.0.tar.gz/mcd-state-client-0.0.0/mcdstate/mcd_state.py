import requests


class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r


class Operator:
    def __init__(self, operator, dimension, value) -> None:
        self.__value = value
        self.__dimension = dimension
        self.__operator = operator

    def value(self) -> str:
        return self.__value

    def key(self) -> str:
        return "{}[{}]".format(self.__dimension, self.__operator)


class GT(Operator):
    def __init__(self, dimension, value) -> None:
        super().__init__("gt", dimension, value)


class EQ(Operator):
    def __init__(self, dimension, value) -> None:
        super().__init__("eq", dimension, value)


class Client:
    def __init__(self, bearer_token):
        self.__auth = BearerAuth(bearer_token)
        self.__url = "http://www.mcdstate.info/api/"

    def vaults_list(self, **kwargs):
        path = self.__url + "vaults_list"
        params = {}

        if "operators" in kwargs:
            for operator in kwargs["operators"]:
                params[operator.key()] = operator.value()

        return requests.get(path, params, auth=self.__auth).json()["Message"]
