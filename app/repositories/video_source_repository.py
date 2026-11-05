from typing import List
from repositories.base_repository import BaseRepository
from video_source import VideoSource


class VideoSourceRepository(BaseRepository):
    async def insert_video_source(self, video_source: VideoSource) -> None:
        query_city = """
            insert into raw.cities (name)
            values ($1)
            on conflict (name) do update set name = excluded.name
            returning id
        """
        query_street = """
            insert into raw.streets (city_id, name)
            values ($1, $2)
            on conflict (city_id, name) do update set city_id = excluded.city_id, name = excluded.name
            returning id
        """
        query_video = """
            insert into raw.video_sources (street_id, url)
            values ($1, $2)
            on conflict (url) do nothing
        """

        async with self.pool.acquire() as connection:
            async with connection.transaction():
                city_id = await connection.fetchval(query_city, video_source.city)

                street_id = await connection.fetchval(query_street, city_id, video_source.street)

                await connection.execute(query_video, street_id, video_source.url)


    async def get_video_sources(self, video_id : int | None = None) -> List[tuple] | tuple:
        base_query = """
            select v.id, v.status, c.name, s.name, v.url
            from raw.video_sources AS v
            join raw.streets AS s ON v.street_id = s.id
            join raw.cities AS c ON c.id = s.city_id
        """

        async with self.pool.acquire() as connection:
            async with connection.transaction():
                if video_id is None:
                    data = await connection.fetch(base_query)
                    return [tuple(row) for row in data]

                query = base_query + " where v.id = $1"
                data = await connection.fetchrow(query, video_id)
                return tuple(data)

    async def check_source_exists(self, url: str) -> bool:
        query = "select 1 from raw.video_sources where url = $1"
        async with self.pool.acquire() as connection:
            async with connection.transaction():
                row = await connection.fetchval(query, url)
                is_source_exists = row is None
                return is_source_exists
