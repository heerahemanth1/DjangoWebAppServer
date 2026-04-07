# -*- coding: utf-8 -*-


class WebAuthenticationError(Exception):
    def __init__(self, message, description):
        self.message = message
        self.description = description

    def __str__(self):
        return f"{self.__class__.__name__}: {self.message} \n{self.description}"


class MaxTriesReachedError(WebAuthenticationError):
    def __init__(self, message, description):
        super().__init__(message, description)


class AuthorizationCodeGenerationError(WebAuthenticationError):
    def __init__(self, message, description):
        super().__init__(message, description)


class AuthenticationError(WebAuthenticationError):
    def __init__(self, message, description):
        super().__init__(message, description)

