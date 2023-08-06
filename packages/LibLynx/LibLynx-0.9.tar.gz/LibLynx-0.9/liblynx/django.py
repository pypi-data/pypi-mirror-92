import logging
import liblynx
from django.conf import settings
from django.http import HttpResponseRedirect


class LibLynxAuthMiddleware:
    def __init__(self, get_response):
        self.ll = liblynx.Connect()
        self.get_response = get_response
        self.product_cache = {}

    def authenticate(self, request):
        # If the request has a _ll_ignore_host parameter, ignore the host, thus forcing a WAYF identification
        # This enables us to allow anonynous access for users who do no wish to authenticate,
        # but still allow a "Login" button
        if "_ll_ignore_host" in request.GET:
            host = "127.0.0.127"  # we do need to supply a valid IP address to the API
        else:
            host = request.get_host()

        identification = self.ll.new_identification(
            host,
            request.build_absolute_uri(),
            request.headers.get("User-Agent", "<unknown>"),
        )
        logging.debug(identification)
        if identification["status"] == "wayf":  # Needs a redirect to authenticate
            return HttpResponseRedirect(identification["_links"]["wayf"]["href"])

        if identification["status"] == "identified":
            request.session["LIBLYNX_ACCOUNT"] = identification["account"][
                "account_name"
            ]
            request.session["LIBLYNX_ACCOUNT_ID"] = identification["account"]["id"]

            # Get the account information, so that we can retrieve the subscriptions
            account = self.ll.api(
                "account", identification["account"]["_links"]["self"]["href"],
            )

            # Fetch the products for this user, if configured
            if settings.LIBLYNX_FETCH_PRODUCTS:
                subs = self.ll.api("subs", account["_links"]["account_subs"]["href"])

                products = []
                for sub in subs["subscriptions"]:
                    sub_link = sub["_links"]["subscription_units"]["href"]
                    if sub_link not in self.product_cache:
                        self.product_cache[sub_link] = self.ll.api("sub", sub_link)
                    for unit in self.product_cache[sub_link]["units"]:
                        products.append(unit["unit_code"])

                request.session["LIBLYNX_PRODUCTS"] = products

    def __call__(self, request):
        if "_ll_ignore_host" in request.GET and "LIBLYNX_ACCOUNT" in request.session:
            del request.session["LIBLYNX_ACCOUNT"]
        if "LIBLYNX_ACCOUNT" not in request.session:
            response = self.authenticate(request)
            if response is not None:
                return response

        response = self.get_response(request)

        return response
