from ._controller import Controller, ControllerError


def controller_setup(app: object, root_urls: str, cors: bool = False):
    Controller.entry_point(root_urls)
    if cors:
        import aiohttp_cors

        cors = aiohttp_cors.setup(
            app,
            defaults={
                "*": aiohttp_cors.ResourceOptions(
                    allow_credentials=True,
                    expose_headers="*",
                    allow_headers="*",
                    max_age=3600,
                )
            },
        )
        for route in Controller.urls():
            resource = cors.add(app.router.add_resource(route.path, name=route.name))
            cors.add(resource.add_route("GET", route.handler))
            cors.add(resource.add_route("PUT", route.handler))
            cors.add(resource.add_route("POST", route.handler))
            cors.add(resource.add_route("PATCH", route.handler))
            cors.add(resource.add_route("DELETE", route.handler))
        return
    for route in Controller.urls():
        app.router.add_route("*", route.path, route.handler, name=route.name)
