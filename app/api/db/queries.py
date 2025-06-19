from app.api.db import async_session
from sqlalchemy import text

class User:

    @staticmethod
    async def select_user(email: str):
        async with async_session() as session:

            query = """
                    SELECT email, attrs
                    FROM users
                    WHERE 
                        email=:email;
                    """
            result = await session.execute(text(query), {'email': email})
            user = result.mappings().first()
            return user
