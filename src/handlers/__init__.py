def register_all():
    for module in ("errors", "users", "groups", "channels"):
        __import__(f"src.handlers.{module}")
