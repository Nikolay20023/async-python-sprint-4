import secrets
import string


async def create_random_key(lenght: int = 5) -> str:
    chars = string.ascii_uppercase + string.digits
    return "".join(secrets.choice(chars) for _ in range(lenght))
