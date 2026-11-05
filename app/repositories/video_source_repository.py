from dotenv import load_dotenv
from typing import List
from repositories.base_repository import BaseRepository
from video_source import VideoSource


class VideoSourceRepository(BaseRepository):
    def insert_video_source(self, video_source: VideoSource) -> None:
        query_city = """
            insert into raw.cities (name)
            values (%s)
            on conflict (name) do update set name = excluded.name
            returning id
        """
        query_street = """
            insert into raw.streets (city_id, name)
            values (%s, %s)
            on conflict (city_id, name) do update set city_id = excluded.city_id, name = excluded.name
            returning id
        """
        query_video = """
            insert into raw.video_sources (street_id, url)
            values (%s, %s)
            on conflict (url) do nothing
        """
        try:
            with self.CONNECTION.cursor() as cursor:
                cursor.execute(query_city, (video_source.city, ))
                city_id = cursor.fetchone()[0]

                cursor.execute(query_street, (city_id, video_source.street))
                street_id = cursor.fetchone()[0]

                cursor.execute(query_video, (street_id, video_source.url))

                self.CONNECTION.commit()
        except psycopg2.Error as ex:
            self.CONNECTION.rollback()
            raise ex

    def get_video_sources(self, video_id : int | None = None) -> List[tuple] | tuple:
        base_query = """
            select v.id, v.status, c.name, s.name, v.url
            from raw.video_sources AS v
            join raw.streets AS s ON v.street_id = s.id
            join raw.cities AS c ON c.id = s.city_id
        """

        with self.CONNECTION.cursor() as cursor:
            if video_id is None:
                cursor.execute(base_query)
                return cursor.fetchall()

            query = base_query + " where v.id = %s"
            cursor.execute(query, (video_id, ))
            return cursor.fetchone()

    def check_source_exists(self, url: str) -> bool:
        query = "select 1 from raw.video_sources where url = %s"
        with self.CONNECTION.cursor() as cursor:
            cursor.execute(query, (url, ))
            is_source_exists = cursor.fetchone() is not  None
            return is_source_exists
