import functools
import os
import time
import typing
from datetime import date, datetime
from uuid import uuid4

import dectate
import morepath
import morpfw
import reg
from a_un import load_license, validate_license
from more.chameleon import ChameleonApp
from morepath.publish import resolve_model
from morpcc.authz.policy import MorpCCAuthzPolicy
from morpfw.app import DBSessionRequest
from morpfw.authn.pas.policy import DefaultAuthnPolicy
from morpfw.authz.pas import DefaultAuthzPolicy
from morpfw.main import create_app
from morpfw.request import ESCapableRequest
from webob.exc import HTTPException

from . import directive
from .authn import IdentityPolicy


class WebAppRequest(ESCapableRequest):
    def notify(self, category, title, message):
        session = self.session
        session.setdefault("messages", [])
        session["messages"].append(
            {"category": category, "title": title, "message": message}
        )
        session.save()

    def messages(self):
        session = self.session
        result = session.get("messages", [])
        session["messages"] = []
        session.save()
        return result

    def get_license(self) -> typing.Optional[dict]:
        cert = self.app.get_license_cert(self)
        key = self.app.get_license_key(self)
        license = None
        license_expired = False
        if key:
            license = load_license(key)
            if license:
                license["created"] = datetime.fromtimestamp(
                    license["created"], tz=self.timezone()
                )
                license["start"] = datetime.fromtimestamp(
                    license["start"], tz=self.timezone()
                )
                license["end"] = datetime.fromtimestamp(
                    license["end"], tz=self.timezone()
                )
        if key and cert:
            valid_license = validate_license(cert, key)
            if not validate_license:
                license = None

            else:
                if time.time() > valid_license["end"]:
                    license_expired = True
        if license:
            license["expired"] = license_expired
            return license
        return None


class App(ChameleonApp, morpfw.SQLApp, MorpCCAuthzPolicy):

    request_class = WebAppRequest

    portlet = dectate.directive(directive.PortletFactoryAction)
    portletprovider = dectate.directive(directive.PortletProviderFactoryAction)
    contextportletprovider = dectate.directive(
        directive.ContextPortletProviderFactoryAction
    )
    structure_column = dectate.directive(directive.StructureColumnAction)
    schemaextender = dectate.directive(directive.SchemaExtenderAction)
    messagingprovider = dectate.directive(directive.MessagingProviderAction)
    vocabulary = dectate.directive(directive.VocabularyAction)
    indexer = dectate.directive(directive.IndexerAction)
    indexresolver = dectate.directive(directive.IndexResolverAction)
    behavior = dectate.directive(directive.BehaviorAction)
    application_behavior = dectate.directive(directive.ApplicationBehaviorAction)
    default_factory = dectate.directive(directive.DefaultFactoryAction)
    restricted_module = dectate.directive(directive.RestrictedModuleAction)
    breadcrumb = dectate.directive(directive.BreadcrumbAction)
    setting_page = dectate.directive(directive.SettingPageAction)
    setting_modules = dectate.directive(directive.SettingModuleAction)
    license_cert = dectate.directive(directive.LicenseCertAction)
    license_key = dectate.directive(directive.LicenseKeyAction)
    copyright_notice = dectate.directive(directive.CopyrightNoticeAction)
    datasource = dectate.directive(directive.DataSourceAction)
    permission_resolver = dectate.directive(directive.PermissionResolverAction)

    @reg.dispatch_method(reg.match_instance("model"), reg.match_key("name"))
    def get_indexer(self, model, name):
        return None

    @reg.dispatch_method(
        reg.match_instance("model"),
        reg.match_instance("request"),
        reg.match_key("name"),
    )
    def get_structure_column(self, model, request, name):
        raise NotImplementedError(
            "Get structure columns for %s structure:%s" % (model, name)
        )

    def get_portletprovider(self, name):
        return self.config.portletprovider_registry.get_provider(name)

    @reg.dispatch_method(reg.match_instance("model"), reg.match_key("name"))
    def get_contextportletprovider(self, model, name):
        return None

    @reg.dispatch_method(reg.match_class("schema"))
    def get_schemaextender(self, schema):
        return schema

    @reg.dispatch_method(reg.match_instance("request"), reg.match_key("name"))
    def get_messagingprovider(self, request, name):
        raise NotImplementedError("Messaging provider %s is not available" % name)

    @reg.dispatch_method(reg.match_instance("request"), reg.match_key("name"))
    def get_vocabulary(self, request, name):
        return None

    @reg.dispatch_method(reg.match_key("name"))
    def get_behavior_factory(self, name):
        raise NotImplementedError

    @reg.dispatch_method(reg.match_key("name"))
    def get_application_behavior_factory(self, name):
        raise NotImplementedError

    @reg.dispatch_method(reg.match_key("name"))
    def get_default_factory(self, name):
        raise NotImplementedError

    @reg.dispatch_method(reg.match_key("name"))
    def get_index_resolver(self, name):
        raise NotImplementedError

    @reg.dispatch_method(reg.match_key("name"))
    def get_restricted_module(self, name):
        raise ImportError(
            "Module {} is not allowed to be imported in this context".format(name)
        )

    @reg.dispatch_method(
        reg.match_instance("model"), reg.match_instance("request"),
    )
    def get_breadcrumb(self, model, request):
        return []

    @reg.dispatch_method(reg.match_instance("request"))
    def get_license_cert(self, request):
        return None

    @reg.dispatch_method(reg.match_instance("request"))
    def get_license_key(self, request):
        return None

    @reg.dispatch_method(reg.match_instance("request"))
    def get_copyright_notice(self, request):
        dt = date.today()
        return (
            "Morp Control Center. &copy; 2018-%s Mohd Izhar Firdaus Bin Ismail"
            % dt.year
        )

    @reg.dispatch_method(reg.match_key("name"))
    def get_datasource_factory(self, name):
        raise NotImplementedError()

    def get_datasource(self, name, request):
        return self.config.datasource_registry.get(name=name, request=request)

    def resolve_permissionassignment(self, request, model, permission, identity):
        return self.config.permissionresolver_registry.resolve(
            request, model, permission, identity
        )

    def render_view(self, context, request, name=""):
        lookup = self.get_view.by_predicates(model=context.__class__, name=name)
        if lookup and lookup.component:
            try:
                return lookup.component(obj=context, request=request, app=self)
            except HTTPException as e:
                return None
        return None


class AuthnPolicy(DefaultAuthnPolicy):
    def get_identity_policy(self, settings):
        config = settings.configuration.__dict__
        if config.get("app.development_mode", True):
            secure = False
        else:
            secure = True

        master_secret = config.get("morpfw.security.jwt", {}).get(
            "master_secret", uuid4().hex
        )

        jwt_settings = config.get("morpfw.security.jwt").copy()
        if not "master_secret" in jwt_settings:
            jwt_settings["master_secret"] = master_secret

        itsdangerous_settings = {"secure": secure, "secret": master_secret}

        return IdentityPolicy(
            jwt_settings=jwt_settings,
            itsdangerous_settings=itsdangerous_settings,
            api_root="/api",
            development_mode=config.get("app.development_mode", True),
        )


App.hook_auth_models(prefix="/api/v1/auth")

create_morpcc_app = create_app
