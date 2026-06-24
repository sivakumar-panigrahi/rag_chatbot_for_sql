from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.services.conversation_service import ConversationService
from src.application.services.message_service import MessageService
from src.infrastructure.database.session import get_db
from src.presentation.schemas.conversation import ConversationResponse, MessageResponse

router = APIRouter(
    prefix="/conversations",
    tags=["Conversations"],
)


@router.get("", response_model=list[ConversationResponse])
async def list_conversations(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
):
    """
    List all conversations ordered by updated_at descending.
    """
    service = ConversationService(db)
    conversations = await service.list_conversations(skip=skip, limit=limit)
    return conversations


@router.get("/{conversation_id}/messages", response_model=list[MessageResponse])
async def get_conversation_messages(
    conversation_id: int,
    db: AsyncSession = Depends(get_db),
):
    """
    Get all messages for a specific conversation.
    """
    conv_service = ConversationService(db)
    conversation = await conv_service.get_conversation(conversation_id)
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found",
        )

    msg_service = MessageService(db)
    messages = await msg_service.get_messages_by_conversation(conversation_id)
    return messages


@router.delete("/{conversation_id}", response_model=ConversationResponse)
async def delete_conversation(
    conversation_id: int,
    db: AsyncSession = Depends(get_db),
):
    """
    Delete a conversation and all its associated messages.
    """
    service = ConversationService(db)
    conversation = await service.get_conversation(conversation_id)
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found",
        )

    await service.delete_conversation(conversation_id)
    return conversation
