from grunnlag.gql.sample import CREATE_SAMPLE, FILTER_SAMPLE, GET_SAMPLE
from grunnlag.gql.representation import CREATE_REPRESENTATION, GET_REPRESENTATION, UPDATE_REPRESENTATION, FILTER_REPRESENTATION
from grunnlag.managers import RepresentationManager
from typing import ForwardRef, List, Optional
from bergen.types.model import ArnheimModel
from bergen.schema import User
from grunnlag.extenders import Array, RepresentationPrettifier

Representation = ForwardRef("Representation")


class Representation(RepresentationPrettifier, Array, ArnheimModel):
    id: Optional[int]
    name: Optional[str]
    package: Optional[str]
    store: Optional[str]
    shape: Optional[List[int]]
    image: Optional[str]
    unique: Optional[str]

    objects = RepresentationManager()

    class Meta:
        identifier = "representation"
        get = GET_REPRESENTATION
        create = CREATE_REPRESENTATION
        update = UPDATE_REPRESENTATION
        filter = FILTER_REPRESENTATION


class Sample(ArnheimModel):
    id: Optional[int]
    representations: Optional[List[Representation]]
    creator: Optional[User]

    class Meta:
        identifier = "sample"
        get = GET_SAMPLE
        filter = FILTER_SAMPLE
        create = CREATE_SAMPLE





Representation.update_forward_refs()

