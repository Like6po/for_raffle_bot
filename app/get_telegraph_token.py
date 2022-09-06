from asyncio import run

from aiograph import Telegraph


async def main():
    telegraph = Telegraph()
    print((await telegraph.create_account(short_name='raffle')).access_token)
    await telegraph.close()

if __name__ == "__main__":
    run(main())
