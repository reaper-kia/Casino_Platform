from datetime import UTC, datetime

from casino_service.application.read_models.rooms import (
    CasinoPlayerReadModel,
    ParticipantReadModel,
    RoomReadModel,
)
from casino_service.domain.entities import CasinoPlayer, ProcessedCommand, Room
from casino_service.infra.database.models.casino_player import CasinoPlayerModel
from casino_service.infra.database.models.processed_command import ProcessedCommandModel
from casino_service.infra.database.models.room import RoomModel
from casino_service.infra.database.models.room_participant import RoomParticipantModel


def room_model_to_domain(model: RoomModel) -> Room:
    return Room(
        id=model.id,
        name=model.name,
        game_type=model.game_type,
        visibility=model.visibility,
        capacity=model.capacity,
        owner_player_id=model.owner_player_id,
        status=model.status,
        is_system=model.is_system,
        revision=model.revision,
        invite_token_hash=model.invite_token_hash,
        created_at=model.created_at,
        updated_at=model.updated_at,
        closed_at=model.closed_at,
    )


def room_domain_to_model(room: Room) -> RoomModel:
    return RoomModel(
        id=room.id,
        name=room.name,
        game_type=room.game_type,
        visibility=room.visibility,
        capacity=room.capacity,
        owner_player_id=room.owner_player_id,
        status=room.status,
        is_system=room.is_system,
        revision=room.revision,
        invite_token_hash=room.invite_token_hash,
        created_at=room.created_at,
        updated_at=room.updated_at,
        closed_at=room.closed_at,
    )


def casino_player_model_to_domain(model: CasinoPlayerModel) -> CasinoPlayer:
    return CasinoPlayer(
        id=model.id,
        identity_user_id=model.identity_user_id,
        nickname=model.nickname,
        avatar_url=model.avatar_url,
        status=model.status,
        created_at=model.created_at,
        updated_at=model.updated_at,
    )


def processed_command_model_to_domain(model: ProcessedCommandModel) -> ProcessedCommand:
    return ProcessedCommand(
        key=model.key,
        actor_identity_user_id=model.actor_identity_user_id,
        command_name=model.command_name,
        payload_hash=model.payload_hash,
        result_room_id=model.result_room_id,
        created_at=model.created_at,
    )


def processed_command_domain_to_model(cmd: ProcessedCommand) -> ProcessedCommandModel:
    return ProcessedCommandModel(
        key=cmd.key,
        payload_hash=cmd.payload_hash,
        result_room_id=cmd.result_room_id,
        created_at=cmd.created_at or datetime.now(UTC),
    )


def room_model_to_read_model(model: RoomModel, participants_count: int = 0) -> RoomReadModel:
    return RoomReadModel(
        id=model.id,
        name=model.name,
        game_type=model.game_type,
        visibility=model.visibility,
        capacity=model.capacity,
        owner_player_id=model.owner_player_id,
        status=model.status,
        is_system=model.is_system,
        revision=model.revision,
        created_at=model.created_at,
        updated_at=model.updated_at,
        closed_at=model.closed_at,
        participants_count=participants_count,
    )


def participant_model_to_read_model(
    participant_model: RoomParticipantModel,
    player_model: CasinoPlayerModel,
) -> ParticipantReadModel:
    player_read = CasinoPlayerReadModel(
        id=player_model.id,
        identity_user_id=player_model.identity_user_id,
        nickname=player_model.nickname,
        avatar_url=player_model.avatar_url,
        status=player_model.status,
        created_at=player_model.created_at,
        updated_at=player_model.updated_at,
    )
    return ParticipantReadModel(
        id=participant_model.id,
        room_id=participant_model.room_id,
        player_id=participant_model.player_id,
        player=player_read,
        seat=participant_model.seat,
        membership_status=participant_model.membership_status,
        connection_status=participant_model.connection_status,
        joined_at=participant_model.joined_at,
        disconnected_at=participant_model.disconnected_at,
        reconnect_deadline=participant_model.reconnect_deadline,
        left_at=participant_model.left_at,
    )
