from fastapi import HTTPException, status

credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

host_already_has_room_exception = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="This host already has a room created"
    )

no_such_room_exception = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Cant destroy a room that doesnt exist"
    )