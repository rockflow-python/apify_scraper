import os
import dotenv
import asyncio
import json
import aiohttp
# import setting
dotenv.load_dotenv()


async def run_task(task_id: str, payload: dict) -> str:
    api_token = os.getenv("APIFY_TOKEN")
    url = f'https://api.apify.com/v2/actor-tasks/{task_id}/runs?token={api_token}'
    print(url)

    id = None  # 初始化 id

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as response:
            if response.status:
                print('Task 启动成功')
                response_data = await response.json()
                print(response_data)
                id = response_data['data']['id']
                print(id)
            else:
                error_message = await response.text()
                print(f'Task 启动失败: {error_message}')
                return None  # 或返回错误信息

    return id  # 返回 id 或 None


async def get_news_url():
    symbol = 'MSFT'
    payload = {
        'startUrls': [{'url': f"https://longportapp.com/zh-CN/quote/{symbol}.US/news"}]
    }
    return await run_task('rockflow~news-url-scraper', payload=payload)

async def get_news_content():
   payload = {
        'startUrls': [{'url': "https://longportapp.com/en/news/102293009?channel=n102293009"}]
    }
   return await run_task('rockflow~get-news-context', payload=payload)

if __name__ == "__main__":
    result = asyncio.run(get_news_content())
    print(result)



