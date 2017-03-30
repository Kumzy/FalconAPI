# -*- coding: utf-8 -*-

import falcon
import sqlalchemy.orm.scoping as scoping
from sqlalchemy.exc import SQLAlchemyError


from app import config



class DatabaseSessionManager(object):
    def __init__(self, db_session):
        self._session_factory = db_session
        self._scoped = isinstance(db_session, scoping.ScopedSession)

    def process_request(self, req, resp):
        """Process the request before routing it.

        Args:
            req: Request object that will eventually be
                routed to an on_* responder method.
            resp: Response object that will be routed to
                the on_* responder.
        """
        req.context['session'] = self._session_factory

    def process_resource(self, req, resp, resource, params):
        """Process the request and resource *after* routing.

        Note:
            This method is only called when the request matches
            a route to a resource.

        Args:
            req: Request object that will be passed to the
                routed responder.
            resp: Response object that will be passed to the
                responder.
            resource: Resource object to which the request was
                routed. May be None if no route was found for
                the request.
            params: A dict-like object representing any
                additional params derived from the route's URI
                template fields, that will be passed to the
                resource's responder method as keyword
                arguments.
        """

    def process_response(self, req, resp, resource, req_succeeded):
        """Post-processing of the response (after routing).

        Args:
            req: Request object.
            resp: Response object.
            resource: Resource object to which the request was
                routed. May be None if no route was found
                for the request.
            req_succeeded: True if no exceptions were raised
                while the framework processed and routed the
                request; otherwise False.
        """
        session = req.context['session']

        if config.DB_AUTOCOMMIT:
            try:
                session.commit()
            except SQLAlchemyError as ex:
                session.rollback()

        if self._scoped:
            # remove any database-loaded state from all current objects
            # so that the next access of any attribute, or any query execution will retrieve new state
            self._session_factory.remove()
            #session.remove()
        else:
            session.close()
