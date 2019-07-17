from ..helpers import enums, vars


class UploadTypes(enums.MetaEnum):
    """Enum: photo, audio, video, file"""
    photo = vars.Var()
    audio = vars.Var()
    video = vars.Var()
    file = vars.Var()
