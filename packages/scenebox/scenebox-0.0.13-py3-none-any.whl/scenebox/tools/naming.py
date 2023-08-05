from typing import Tuple

from . import misc
from .logger import get_logger, log_with_exc_info

logger = get_logger(__name__)

# Cache for storing standardized names
standardized_name_cache = {}


def get_auto_generated_indexing_set_name(session_name: str):
    return "auto-generated extraction set {} for {}".format(
        misc.get_truncated_uid(), session_name)


def get_auto_generated_enrichment_set_name(
        session_uid: str, enrichment_provider: str, unique: bool = True):
    if unique:
        return "auto-generated enrichment set {} for {} from provider {}"\
            .format(misc.get_truncated_uid(), session_uid, enrichment_provider)
    else:
        return "auto-generated enrichment set for {} from provider {}"\
            .format(session_uid, enrichment_provider)


def get_compressed_file_id(filename: str, thumbnail_tag: str):
    try:
        splits = str(filename).split('.')
        filename = splits[0]
        extension = '.'.join(splits[1:])
        compressed_file_id = "{}_{}.{}".format(
            filename, thumbnail_tag, extension)
        return compressed_file_id
    except Exception as e:
        log_with_exc_info(logger,
                          "get_compressed_file_id::: {}, {}, {}".format(
                              filename, type(filename), e))
        raise e


def get_compressed_file_tag(resolution_shape: Tuple[int, ...]):
    return '_'.join([str(i) for i in resolution_shape])


def standardize_name(
        name: str,
        replace_symbol: str = '_') -> str:
    if not name:
        raise ValueError(
            'Session name must be provided, got: `{}`'.format(name))

    if name in standardized_name_cache:
        return standardized_name_cache[name]
    else:
        original_name = name
        for symbol in [",", "*", "\\", "<", "|", ">", "/", "?",
                       ' ', '{', '}', '$', '^', '%', '(', ')', ':', '+', ]:
            name = name.replace(symbol, replace_symbol)

        name = name.lower()
        standardized_name_cache[original_name] = name
        return name


def replace_all_symbols(s: str, replace_symbol: str = '_') -> str:
    for symbol in [
        ",", "*", "\\", "<", "|", ">", "/", "?",
        ' ', '{', '}', '$', '^', '%', '(', ')', ':', '+',
        '@', '!', '#', '&', '\'', '\"', '^', '`', '~', '.'
    ]:
        s = s.replace(symbol, replace_symbol)
    return s


def session_status_key(session_uid: str):
    if not session_uid:
        raise ValueError(
            'Session uid must be provided, got: `{}`'.format(session_uid))
    return "status_{}".format(session_uid)
