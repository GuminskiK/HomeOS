import argparse
from app.models.APIKeys import APIKey
from app.models.Users import UserUpdate
from app.core.db import db_deps, redis_pure
from app.services.users_service import update_user
from app.services.two_fa_service import verify_and_disable
from app.utils.users_utils import get_user_by_username
from app.core.exceptions import UserNotFoundException
from common.users import CurrentUserContext
import asyncio

async def reset_password(args):

    if args.command == "reset-password":
        userUpdate = UserUpdate(
            username = args.username,
            plain_password= args.new_password
        )

        AsyncSessionLocal = db_deps.AsyncSessionLocal()

        async with AsyncSessionLocal as session:
            user = await get_user_by_username(session, args.username)

            if not user:
                raise UserNotFoundException()

            
            context = CurrentUserContext(
                session_id="reset-password-session",
                user_id=user.id,
                username=args.username,
                is_superuser=False,
                is_totp_enabled=False
            )

            await update_user(
                redis_pure,
                session,
                userUpdate,
                user.id
            )

            user.is_totp_enabled = False
            session.add(user)
            await session.commit()

        print(f"Password for user '{args.username}' has been reset successfully.")

        if hasattr(redis_pure, "aclose"):
            await redis_pure.aclose()
        else:
            await redis_pure.close()

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Zarządzanie aplikacją HomeOS")
    subparsers = parser.add_subparsers(dest="command")

    # Rejestracja podkomendy reset-password
    reset_parser = subparsers.add_parser("reset-password")
    reset_parser.add_argument("--username", required=True, help="Nazwa użytkownika")
    reset_parser.add_argument("--new-password", required=True, help="Nowe hasło")

    args = parser.parse_args()
    asyncio.run(reset_password(args))