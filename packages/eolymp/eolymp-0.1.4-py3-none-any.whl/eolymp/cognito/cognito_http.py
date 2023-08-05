# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler. DO NOT EDIT!
# See https://github.com/eolymp/contracts/tree/main/cmd/protoc-gen-python-eolymp for more details.
"""Generated protocol buffer code."""

from google.protobuf import symbol_database as _symbol_database

_sym_db = _symbol_database.Default()


class CognitoClient:
    def __init__(self, transport):
        self.transport = transport

    def CreateToken(self, request, **kwargs):
        return self.transport.request(
            url="eolymp.cognito.Cognito/CreateToken",
            request=request,
            response_obj=_sym_db.GetSymbol("eolymp.cognito.CreateTokenOutput"),
            **kwargs,
        )

    def IntrospectToken(self, request, **kwargs):
        return self.transport.request(
            url="eolymp.cognito.Cognito/IntrospectToken",
            request=request,
            response_obj=_sym_db.GetSymbol("eolymp.cognito.IntrospectTokenOutput"),
            **kwargs,
        )

    def CreateAuthorization(self, request, **kwargs):
        return self.transport.request(
            url="eolymp.cognito.Cognito/CreateAuthorization",
            request=request,
            response_obj=_sym_db.GetSymbol("eolymp.cognito.CreateAuthorizationOutput"),
            **kwargs,
        )

    def CreateUser(self, request, **kwargs):
        return self.transport.request(
            url="eolymp.cognito.Cognito/CreateUser",
            request=request,
            response_obj=_sym_db.GetSymbol("eolymp.cognito.CreateUserOutput"),
            **kwargs,
        )

    def NotifyUser(self, request, **kwargs):
        return self.transport.request(
            url="eolymp.cognito.Cognito/NotifyUser",
            request=request,
            response_obj=_sym_db.GetSymbol("eolymp.cognito.NotifyUserOutput"),
            **kwargs,
        )

    def VerifyEmail(self, request, **kwargs):
        return self.transport.request(
            url="eolymp.cognito.Cognito/VerifyEmail",
            request=request,
            response_obj=_sym_db.GetSymbol("eolymp.cognito.VerifyEmailOutput"),
            **kwargs,
        )

    def UpdateEmail(self, request, **kwargs):
        return self.transport.request(
            url="eolymp.cognito.Cognito/UpdateEmail",
            request=request,
            response_obj=_sym_db.GetSymbol("eolymp.cognito.UpdateEmailOutput"),
            **kwargs,
        )

    def StartRecovery(self, request, **kwargs):
        return self.transport.request(
            url="eolymp.cognito.Cognito/StartRecovery",
            request=request,
            response_obj=_sym_db.GetSymbol("eolymp.cognito.StartRecoveryOutput"),
            **kwargs,
        )

    def CompleteRecovery(self, request, **kwargs):
        return self.transport.request(
            url="eolymp.cognito.Cognito/CompleteRecovery",
            request=request,
            response_obj=_sym_db.GetSymbol("eolymp.cognito.CompleteRecoverOutput"),
            **kwargs,
        )

    def IntrospectUser(self, request, **kwargs):
        return self.transport.request(
            url="eolymp.cognito.Cognito/IntrospectUser",
            request=request,
            response_obj=_sym_db.GetSymbol("eolymp.cognito.IntrospectUserOutput"),
            **kwargs,
        )

    def DescribeUser(self, request, **kwargs):
        return self.transport.request(
            url="eolymp.cognito.Cognito/DescribeUser",
            request=request,
            response_obj=_sym_db.GetSymbol("eolymp.cognito.DescribeUserOutput"),
            **kwargs,
        )

    def IntrospectQuota(self, request, **kwargs):
        return self.transport.request(
            url="eolymp.cognito.Cognito/IntrospectQuota",
            request=request,
            response_obj=_sym_db.GetSymbol("eolymp.cognito.IntrospectQuotaOutput"),
            **kwargs,
        )

