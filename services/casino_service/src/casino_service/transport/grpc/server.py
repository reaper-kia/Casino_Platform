from grpc import aio
from grpc_health.v1 import health, health_pb2, health_pb2_grpc

async def create_server(address: str = "[::]:50051") -> tuple[aio.Server, int]: 
    server = aio.server() 

    health_service = health.aio.HealthServicer()
    health_pb2_grpc.add_HealthServicer_to_server(health_service, server)

    await health_service.set(
        "",
        health_pb2.HealthCheckResponse.SERVING,
    )

    port = server.add_insecure_port(address)

    if port == 0:
        raise RuntimeError(f"Cannot bind gRPC server to {address}")

    return server, port

async def serve() -> None:
    server, _ = await create_server()
    await server.start()

    try:
        await server.wait_for_termination()
    finally:
        await server.stop(grace=5)