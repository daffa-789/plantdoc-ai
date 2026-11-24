from fasthtml.common import serve

from backend.config import HOST, PORT


if __name__ == "__main__":
    serve(appname="backend.app", host=HOST, port=PORT, reload=False)
