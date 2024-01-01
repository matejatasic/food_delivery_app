from django.contrib.auth.models import User

from factory import Factory, SubFactory, LazyAttribute, DictFactory, Trait  # type: ignore
from factory.django import DjangoModelFactory  # type: ignore
from json import dumps

from .base import faker  # type: ignore
from ..forms import LoginForm
from ..models import Address, Restaurant, RestaurantCategory, RestaurantLike


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    id = LazyAttribute(lambda _: faker.random_number())
    username = LazyAttribute(lambda _: faker.profile(fields=["username"])["username"])
    password = LazyAttribute(lambda _: faker.pystr(max_chars=10))
    email = LazyAttribute(lambda _: faker.email())


class AddressFactory(Factory):
    class Meta:
        model = Address

    latitude = LazyAttribute(lambda _: float(faker.latitude()))
    longitude = LazyAttribute(lambda _: float(faker.longitude()))
    raw = LazyAttribute(lambda _: faker.address())
    address_line = LazyAttribute(lambda _self: _self.raw)
    district_1 = LazyAttribute(lambda _: faker.country_code())
    district_2 = LazyAttribute(lambda _: faker.country_code())
    country = LazyAttribute(lambda _: faker.country())
    locality = LazyAttribute(lambda _: faker.city())
    postal_code = LazyAttribute(lambda _: faker.postcode())
    user = SubFactory(UserFactory)


class RestaurantCategoryFactory(DjangoModelFactory):
    class Meta:
        model = RestaurantCategory

    name = LazyAttribute(lambda _: faker.pystr())


class RestaurantFactory(DjangoModelFactory):
    class Meta:
        model = Restaurant

    id = LazyAttribute(lambda _: faker.random_number())
    name = LazyAttribute(lambda _: faker.pystr())
    description = LazyAttribute(lambda _: faker.pystr())
    category = SubFactory(RestaurantCategoryFactory)


class RestaurantLikeFactory(Factory):
    class Meta:
        model = RestaurantLike

    restaurant = SubFactory(RestaurantFactory)
    user = SubFactory(UserFactory)


class MapsResponseBboxFactory(DictFactory):
    bbox = LazyAttribute(lambda _: [float(faker.latitude()), float(faker.longitude())])


class MapsResponseAddressFactory(DictFactory):
    formattedAddress = LazyAttribute(lambda _: faker.address())
    addressLine = LazyAttribute(lambda _self: _self.formattedAddress)
    adminDistrict = LazyAttribute(lambda _: faker.country_code())
    adminDistrict2 = LazyAttribute(lambda _: faker.country_code())
    countryRegion = LazyAttribute(lambda _: faker.country())
    locality = LazyAttribute(lambda _: faker.city())
    postalCode = LazyAttribute(lambda _: faker.postcode())


class MapsResponseFactory(DictFactory):
    response = LazyAttribute(
        lambda _: {
            "resourceSets": [
                {
                    "resources": [
                        {
                            "bbox": MapsResponseBboxFactory()["bbox"],
                            "address": MapsResponseAddressFactory(),
                        }
                    ]
                }
            ]
        }
    )


class LoginFormDataFactory(DictFactory):
    username = LazyAttribute(lambda _: faker.profile(fields=["username"])["username"])
    password = LazyAttribute(lambda _: faker.password())

    class Params:
        is_invalid_input = Trait(
            username=LazyAttribute(
                lambda _: faker.pystr(
                    min_chars=LoginForm.base_fields["username"].max_length + 1,  # type: ignore
                    max_chars=LoginForm.base_fields["username"].max_length + 2,  # type: ignore
                )
            ),
            password=LazyAttribute(
                lambda _: faker.pystr(
                    min_chars=LoginForm.base_fields["password"].max_length + 1,  # type: ignore
                    max_chars=LoginForm.base_fields["password"].max_length + 2,  # type: ignore
                )
            ),
        )


class AddressFieldsFactory(DictFactory):
    latitude = LazyAttribute(lambda _: float(faker.latitude()))
    longitude = LazyAttribute(lambda _: float(faker.longitude()))
    raw = LazyAttribute(lambda _: faker.address())
    address_line = LazyAttribute(lambda _self: _self.raw)
    district_1 = LazyAttribute(lambda _: faker.country_code())
    district_2 = LazyAttribute(lambda _: faker.country_code())
    country = LazyAttribute(lambda _: faker.country())
    locality = LazyAttribute(lambda _: faker.city())
    postal_code = LazyAttribute(lambda _: faker.postcode())


class RegisterFormDataFactory(DictFactory):
    username = LazyAttribute(lambda _: faker.profile(fields=["username"])["username"])
    password1 = LazyAttribute(lambda _: faker.password())
    first_name = LazyAttribute(lambda _: faker.first_name())
    last_name = LazyAttribute(lambda _: faker.last_name())
    email = LazyAttribute(lambda _: faker.email())
    address = LazyAttribute(lambda _: dumps([{"fields": AddressFieldsFactory()}]))

    class Params:
        has_password_confirmation = Trait(
            password2=LazyAttribute(lambda _self: _self.password1)
        )
        has_invalid_email = Trait(email="Invalid email")


class UserServiceCreateParametersFactory(DictFactory):
    username = LazyAttribute(lambda _: faker.profile(fields=["username"])["username"])
    password = LazyAttribute(lambda _: faker.password())
    first_name = LazyAttribute(lambda _: faker.first_name())
    last_name = LazyAttribute(lambda _: faker.last_name())
    email = LazyAttribute(lambda _: faker.email())
    address = LazyAttribute(lambda _: AddressFieldsFactory())
