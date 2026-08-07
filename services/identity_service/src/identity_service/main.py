import asyncio

from identity_service.transport.grpc.server import serve


def main() -> None:
    asyncio.run(serve())


if __name__ == "__main__":
    main()