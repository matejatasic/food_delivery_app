from django.core.exceptions import BadRequest
from http import HTTPStatus
from requests import Response, get

from ..dtos import MapsResponseResourcesDto
from ..exceptions import Unauthorized, InternalServerError
from food_delivery_app.settings import BING_MAPS_API_KEY


class MapsService:
    location_by_query_url: str = "http://dev.virtualearth.net/REST/v1/Locations"

    def get_location_by_query(self, query: str) -> list[MapsResponseResourcesDto]:
        response: Response = self.send_request(query)

        if response.status_code == HTTPStatus.BAD_REQUEST:
            raise BadRequest(
                f"Response Headers: {response.headers}, Response: {response.json()}"
            )
        if response.status_code == HTTPStatus.UNAUTHORIZED:
            raise Unauthorized
        if response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
            raise InternalServerError

        resources = response.json()["resourceSets"][0]["resources"]
        resources_dtos: list[MapsResponseResourcesDto] = [
            MapsResponseResourcesDto(resource["bbox"], resource["address"])
            for resource in resources
        ]

        return resources_dtos

    def send_request(self, query: str) -> Response:
        query_parameters: str = (
            f"query={query}&include=queryParse&key={BING_MAPS_API_KEY}"
        )

        return get(f"{self.location_by_query_url}?{query_parameters}")
