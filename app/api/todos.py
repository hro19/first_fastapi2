from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_
from typing import List, Optional
from app.core.database import get_db
from app.models.todo import Todo
from app.schemas.todo import TodoCreate, TodoUpdate, TodoResponse, TodoListResponse
from app.utils.datetime_utils import get_jst_now, format_jst

router = APIRouter()


def format_todo_response(todo: Todo) -> TodoResponse:
    """Todoモデルをレスポンススキーマに変換し、日本時間の文字列を追加"""
    todo_dict = {
        "id": todo.id,
        "title": todo.title,
        "description": todo.description,
        "completed": todo.completed,
        "priority": todo.priority,
        "created_at": todo.created_at,
        "updated_at": todo.updated_at,
        "completed_at": todo.completed_at,
        "deleted_at": todo.deleted_at,
        # 日本時間でフォーマット
        "created_at_jst": format_jst(todo.created_at),
        "updated_at_jst": format_jst(todo.updated_at),
        "completed_at_jst": format_jst(todo.completed_at),
        "deleted_at_jst": format_jst(todo.deleted_at),
    }
    return TodoResponse(**todo_dict)


@router.get("/", response_model=TodoListResponse)
async def get_todos(
    skip: int = Query(0, ge=0, description="スキップする件数"),
    limit: int = Query(100, ge=1, le=1000, description="取得する最大件数"),
    include_deleted: bool = Query(False, description="論理削除されたアイテムを含むか"),
    completed: Optional[bool] = Query(None, description="完了状態でフィルタ"),
    priority: Optional[int] = Query(None, ge=0, le=2, description="優先度でフィルタ"),
    db: AsyncSession = Depends(get_db)
):
    """Todo一覧を取得"""
    query = select(Todo)
    
    # 論理削除されていないものだけを取得（デフォルト）
    if not include_deleted:
        query = query.where(Todo.deleted_at.is_(None))
    
    # 完了状態でフィルタ
    if completed is not None:
        query = query.where(Todo.completed == completed)
    
    # 優先度でフィルタ
    if priority is not None:
        query = query.where(Todo.priority == priority)
    
    # 作成日時の降順でソート
    query = query.order_by(Todo.created_at.desc())
    
    # ページネーション
    query = query.offset(skip).limit(limit)
    
    result = await db.execute(query)
    todos = result.scalars().all()
    
    # 総件数を取得
    count_query = select(Todo)
    if not include_deleted:
        count_query = count_query.where(Todo.deleted_at.is_(None))
    if completed is not None:
        count_query = count_query.where(Todo.completed == completed)
    if priority is not None:
        count_query = count_query.where(Todo.priority == priority)
    
    count_result = await db.execute(count_query)
    total = len(count_result.scalars().all())
    
    return TodoListResponse(
        total=total,
        items=[format_todo_response(todo) for todo in todos]
    )


@router.get("/{todo_id}", response_model=TodoResponse)
async def get_todo(
    todo_id: int,
    include_deleted: bool = Query(False, description="論理削除されたアイテムも取得するか"),
    db: AsyncSession = Depends(get_db)
):
    """特定のTodoを取得"""
    query = select(Todo).where(Todo.id == todo_id)
    
    if not include_deleted:
        query = query.where(Todo.deleted_at.is_(None))
    
    result = await db.execute(query)
    todo = result.scalar_one_or_none()
    
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    return format_todo_response(todo)


@router.post("/", response_model=TodoResponse)
async def create_todo(
    todo: TodoCreate,
    db: AsyncSession = Depends(get_db)
):
    """新しいTodoを作成"""
    db_todo = Todo(**todo.model_dump())
    db.add(db_todo)
    await db.commit()
    await db.refresh(db_todo)
    
    return format_todo_response(db_todo)


@router.patch("/{todo_id}", response_model=TodoResponse)
async def update_todo(
    todo_id: int,
    todo_update: TodoUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Todoを更新"""
    # 論理削除されていないもののみ更新可能
    result = await db.execute(
        select(Todo).where(
            and_(
                Todo.id == todo_id,
                Todo.deleted_at.is_(None)
            )
        )
    )
    todo = result.scalar_one_or_none()
    
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    # 更新するフィールドだけを更新
    update_data = todo_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(todo, field, value)
    
    # completedがTrueになった場合、completed_atを設定
    if "completed" in update_data and update_data["completed"]:
        todo.completed_at = get_jst_now()
    elif "completed" in update_data and not update_data["completed"]:
        todo.completed_at = None
    
    todo.updated_at = get_jst_now()
    
    await db.commit()
    await db.refresh(todo)
    
    return format_todo_response(todo)


@router.delete("/{todo_id}", response_model=TodoResponse)
async def delete_todo(
    todo_id: int,
    permanent: bool = Query(False, description="物理削除するか（True）、論理削除するか（False）"),
    db: AsyncSession = Depends(get_db)
):
    """Todoを削除（デフォルトは論理削除）"""
    result = await db.execute(
        select(Todo).where(Todo.id == todo_id)
    )
    todo = result.scalar_one_or_none()
    
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    if permanent:
        # 物理削除
        await db.delete(todo)
    else:
        # 論理削除
        todo.soft_delete()
    
    await db.commit()
    
    if not permanent:
        await db.refresh(todo)
        return format_todo_response(todo)
    else:
        # 物理削除の場合は削除前のデータを返す
        return format_todo_response(todo)


@router.post("/{todo_id}/restore", response_model=TodoResponse)
async def restore_todo(
    todo_id: int,
    db: AsyncSession = Depends(get_db)
):
    """論理削除されたTodoを復元"""
    result = await db.execute(
        select(Todo).where(
            and_(
                Todo.id == todo_id,
                Todo.deleted_at.is_not(None)
            )
        )
    )
    todo = result.scalar_one_or_none()
    
    if todo is None:
        raise HTTPException(status_code=404, detail="Deleted todo not found")
    
    todo.restore()
    todo.updated_at = get_jst_now()
    
    await db.commit()
    await db.refresh(todo)
    
    return format_todo_response(todo)


@router.post("/{todo_id}/complete", response_model=TodoResponse)
async def complete_todo(
    todo_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Todoを完了にする"""
    result = await db.execute(
        select(Todo).where(
            and_(
                Todo.id == todo_id,
                Todo.deleted_at.is_(None)
            )
        )
    )
    todo = result.scalar_one_or_none()
    
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    todo.completed = True
    todo.completed_at = get_jst_now()
    todo.updated_at = get_jst_now()
    
    await db.commit()
    await db.refresh(todo)
    
    return format_todo_response(todo)